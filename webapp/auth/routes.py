"""
Rotas de autenticação: login/logout por CPF, "esqueci minha senha" e as
duas telas obrigatórias (troca de senha temporária, foto de perfil no
primeiro acesso). Portado de modules/auth.py — mesmas regras de negócio,
persistência da sessão por cookie httponly em vez de URL/localStorage.
"""
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool

from database.repositorio import (
    ImagemInvalidaError,
    atualizar_foto_perfil,
    buscar_aluno_por_cpf,
    desmarcar_definir_foto,
    solicitar_redefinicao_senha,
    trocar_senha_aluno,
)
from webapp.integrations.whatsapp import notificar_pedido_redefinicao_senha
from utils.helpers import somente_digitos
from webapp.auth.cookies import definir_cookie_sessao, limpar_cookie_sessao
from webapp.auth.security import (
    consumir_tempo_de_senha,
    erro_de_politica_de_senha,
    gerar_hash_senha,
    gerar_token_sessao,
    verificar_senha,
)
from webapp.deps import obter_aluno_atual
from webapp.seguranca.cliente import ip_do_cliente
from webapp.seguranca.upload import ArquivoGrandeDemaisError, ler_upload_limitado
from webapp.seguranca.limite_taxa import (
    login_por_cpf,
    login_por_ip,
    redefinicao_por_cpf,
    redefinicao_por_ip,
    texto_de_espera,
)
from webapp.templating import templates

router = APIRouter()

registro = logging.getLogger("cursos_telecom.acesso")

# Uma única mensagem para "CPF não cadastrado" e "senha errada". Mensagens
# diferentes contam a quem está tentando adivinhar quais CPFs existem na
# plataforma — e o CPF é justamente o nome de usuário aqui. A dica sobre acesso
# desativado vai junto para que o aluno bloqueado saiba o que fazer sem que a
# tela precise confirmar que aquele CPF tem cadastro.
_ERRO_CREDENCIAL = (
    "CPF ou senha incorretos. Se o seu acesso foi desativado, "
    "fale com o administrador da plataforma."
)


def _mensagem_de_bloqueio(segundos: int) -> str:
    return (
        f"Muitas tentativas seguidas. Aguarde {texto_de_espera(segundos)} "
        "antes de tentar de novo, ou fale com o administrador."
    )


@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(request, "auth/login.html", {})


@router.post("/login")
def fazer_login(request: Request, cpf: str = Form(...), senha: str = Form(...)):
    cpf_normalizado = somente_digitos(cpf)
    origem = ip_do_cliente(request)

    def recusar(erro: str, status: int = 400):
        return templates.TemplateResponse(
            request, "auth/login.html", {"erro": erro}, status_code=status
        )

    # O bloqueio é conferido antes de qualquer consulta ou verificação de senha:
    # é isso que impede tanto a força bruta quanto o uso da própria tela de login
    # como oráculo para descobrir CPFs cadastrados.
    espera = max(
        login_por_ip.segundos_de_bloqueio(origem),
        login_por_cpf.segundos_de_bloqueio(cpf_normalizado),
    )
    if espera:
        return recusar(_mensagem_de_bloqueio(espera), status=429)

    if len(cpf_normalizado) != 11:
        # Formato inválido não chega a ser tentativa de adivinhação, mas conta
        # no limite por origem para que um script não use este caminho como
        # atalho sem custo.
        login_por_ip.registrar_falha(origem)
        return recusar("Digite um CPF válido (11 números).")

    aluno = buscar_aluno_por_cpf(cpf_normalizado)
    autenticado = (
        aluno is not None
        and aluno.get("ativo", True)
        and verificar_senha(senha, aluno["senha_hash"])
    )
    if aluno is None:
        # Sem isso, a resposta para um CPF inexistente volta em milissegundos
        # (não roda bcrypt) e a demora do login vira um detector de quais CPFs
        # estão cadastrados. Gastar o mesmo tempo iguala os dois caminhos.
        consumir_tempo_de_senha(senha)

    if not autenticado:
        bloqueio = max(
            login_por_cpf.registrar_falha(cpf_normalizado),
            login_por_ip.registrar_falha(origem),
        )
        registro.warning(
            "login recusado cpf=***%s origem=%s bloqueado_por=%ss",
            cpf_normalizado[-2:], origem, bloqueio,
        )
        if bloqueio:
            return recusar(_mensagem_de_bloqueio(bloqueio), status=429)
        return recusar(_ERRO_CREDENCIAL)

    login_por_cpf.registrar_sucesso(cpf_normalizado)
    login_por_ip.registrar_sucesso(origem)
    registro.info("login aceito aluno=%s origem=%s", aluno["id"], origem)

    token = gerar_token_sessao(aluno["id"], aluno["senha_hash"])
    resposta = RedirectResponse("/", status_code=303)
    definir_cookie_sessao(resposta, token)
    return resposta


@router.post("/logout")
def fazer_logout():
    resposta = RedirectResponse("/login", status_code=303)
    limpar_cookie_sessao(resposta)
    return resposta


@router.post("/esqueci-senha")
def esqueci_senha(request: Request, background_tasks: BackgroundTasks, cpf: str = Form(...)):
    cpf_normalizado = somente_digitos(cpf)
    origem = ip_do_cliente(request)

    # Cada pedido aceito dispara um WhatsApp para o administrador. Sem limite,
    # dá pra inundar o telefone dele e queimar a cota da API a partir de uma
    # única aba do navegador.
    espera = max(
        redefinicao_por_ip.segundos_de_bloqueio(origem),
        redefinicao_por_cpf.segundos_de_bloqueio(cpf_normalizado),
    )
    if espera:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"erro": _mensagem_de_bloqueio(espera)},
            status_code=429,
        )
    redefinicao_por_cpf.registrar_falha(cpf_normalizado)
    redefinicao_por_ip.registrar_falha(origem)

    aluno_encontrado = solicitar_redefinicao_senha(cpf)
    if aluno_encontrado:
        # Roda depois de responder — não faz sentido a pessoa esperar o
        # WhatsApp do admin pra ver a mensagem de confirmação na tela.
        background_tasks.add_task(
            notificar_pedido_redefinicao_senha,
            aluno_encontrado["nome_completo"], aluno_encontrado["email"],
        )
    # Mesma mensagem independente de o CPF existir ou não, para não revelar
    # quais CPFs têm cadastro na plataforma.
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {
            "sucesso": (
                "Se este CPF estiver cadastrado, o pedido foi enviado. "
                "Aguarde o administrador entrar em contato com sua nova senha."
            )
        },
    )


@router.get("/trocar-senha-obrigatoria")
def tela_trocar_senha_obrigatoria(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    return templates.TemplateResponse(request, "auth/trocar_senha.html", {})


@router.post("/trocar-senha-obrigatoria")
def trocar_senha_obrigatoria(
    request: Request,
    nova_senha: str = Form(...),
    confirmar: str = Form(...),
    aluno: dict = Depends(obter_aluno_atual),
):
    erro = erro_de_politica_de_senha(
        nova_senha, cpf=aluno.get("cpf", ""), nome=aluno.get("nome_completo", "")
    )
    if not erro and nova_senha != confirmar:
        erro = "As senhas não coincidem."
    if erro:
        return templates.TemplateResponse(
            request, "auth/trocar_senha.html", {"erro": erro}, status_code=400,
        )

    novo_hash = gerar_hash_senha(nova_senha)
    trocar_senha_aluno(aluno["id"], novo_hash)

    # Trocar a senha invalida todos os cookies emitidos com a senha antiga
    # (ver marca_de_senha em webapp/auth/security.py) — inclusive o desta aba.
    # Emitir um cookie novo aqui mantém o aluno logado e, ao mesmo tempo,
    # expulsa qualquer outra sessão que estivesse aberta com a senha anterior.
    resposta = RedirectResponse("/", status_code=303)
    definir_cookie_sessao(resposta, gerar_token_sessao(aluno["id"], novo_hash))
    return resposta


@router.get("/definir-foto-obrigatoria")
def tela_definir_foto_obrigatoria(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    return templates.TemplateResponse(request, "auth/definir_foto.html", {})


@router.post("/definir-foto-obrigatoria")
async def definir_foto_obrigatoria(
    request: Request,
    foto: UploadFile,
    aluno: dict = Depends(obter_aluno_atual),
):
    try:
        conteudo = await ler_upload_limitado(foto)
    except ArquivoGrandeDemaisError as erro:
        return templates.TemplateResponse(
            request, "auth/definir_foto.html", {"erro": str(erro)}, status_code=400,
        )
    if not conteudo:
        return templates.TemplateResponse(
            request,
            "auth/definir_foto.html",
            {"erro": "Escolha uma foto antes de continuar."},
            status_code=400,
        )

    try:
        # Processa a imagem (Pillow) e envia pro Storage do Supabase numa
        # thread separada, pra não travar o event loop de todo mundo.
        await run_in_threadpool(atualizar_foto_perfil, aluno["id"], conteudo)
    except ImagemInvalidaError as erro:
        return templates.TemplateResponse(
            request, "auth/definir_foto.html", {"erro": str(erro)}, status_code=400,
        )

    desmarcar_definir_foto(aluno["id"])
    return RedirectResponse("/", status_code=303)
