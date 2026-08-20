"""
Rotas de autenticação: login/logout por CPF, "esqueci minha senha" e as
duas telas obrigatórias (troca de senha temporária, foto de perfil no
primeiro acesso). Portado de modules/auth.py — mesmas regras de negócio,
persistência da sessão por cookie httponly em vez de URL/localStorage.
"""
from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.responses import RedirectResponse

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
from webapp.auth.security import gerar_hash_senha, gerar_token_sessao, verificar_senha
from webapp.deps import obter_aluno_atual
from webapp.templating import templates

router = APIRouter()


@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(request, "auth/login.html", {})


@router.post("/login")
def fazer_login(request: Request, cpf: str = Form(...), senha: str = Form(...)):
    cpf_normalizado = somente_digitos(cpf)
    erro = None

    if len(cpf_normalizado) != 11:
        erro = "Digite um CPF válido (11 números)."
    else:
        aluno = buscar_aluno_por_cpf(cpf_normalizado)
        if aluno is None:
            erro = "CPF não encontrado. Confira o número ou fale com o administrador."
        elif not aluno.get("ativo", True):
            erro = "Este acesso foi desativado. Entre em contato com o administrador da plataforma."
        elif not verificar_senha(senha, aluno["senha_hash"]):
            erro = "Senha incorreta. Tente novamente."

    if erro:
        return templates.TemplateResponse(
            request, "auth/login.html", {"erro": erro}, status_code=400
        )

    token = gerar_token_sessao(aluno["id"])
    resposta = RedirectResponse("/", status_code=303)
    definir_cookie_sessao(resposta, token)
    return resposta


@router.post("/logout")
def fazer_logout():
    resposta = RedirectResponse("/login", status_code=303)
    limpar_cookie_sessao(resposta)
    return resposta


@router.post("/esqueci-senha")
def esqueci_senha(request: Request, cpf: str = Form(...)):
    aluno_encontrado = solicitar_redefinicao_senha(cpf)
    if aluno_encontrado:
        notificar_pedido_redefinicao_senha(
            aluno_encontrado["nome_completo"], aluno_encontrado["email"]
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
    if len(nova_senha) < 6:
        return templates.TemplateResponse(
            request,
            "auth/trocar_senha.html",
            {"erro": "A senha deve ter pelo menos 6 caracteres."},
            status_code=400,
        )
    if nova_senha != confirmar:
        return templates.TemplateResponse(
            request,
            "auth/trocar_senha.html",
            {"erro": "As senhas não coincidem."},
            status_code=400,
        )

    trocar_senha_aluno(aluno["id"], gerar_hash_senha(nova_senha))
    return RedirectResponse("/", status_code=303)


@router.get("/definir-foto-obrigatoria")
def tela_definir_foto_obrigatoria(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    return templates.TemplateResponse(request, "auth/definir_foto.html", {})


@router.post("/definir-foto-obrigatoria")
async def definir_foto_obrigatoria(
    request: Request,
    foto: UploadFile,
    aluno: dict = Depends(obter_aluno_atual),
):
    conteudo = await foto.read()
    if not conteudo:
        return templates.TemplateResponse(
            request,
            "auth/definir_foto.html",
            {"erro": "Escolha uma foto antes de continuar."},
            status_code=400,
        )

    try:
        atualizar_foto_perfil(aluno["id"], conteudo)
    except ImagemInvalidaError as erro:
        return templates.TemplateResponse(
            request, "auth/definir_foto.html", {"erro": str(erro)}, status_code=400,
        )

    desmarcar_definir_foto(aluno["id"])
    return RedirectResponse("/", status_code=303)
