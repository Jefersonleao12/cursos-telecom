"""'Meu Perfil' — porta modules/perfil.py: dados de contato, troca de
senha (confere a senha atual antes) e histórico de progresso do aluno."""
from fastapi import APIRouter, Depends, Form, Request, UploadFile

from database.repositorio import (
    ImagemInvalidaError,
    atualizar_foto_perfil,
    atualizar_perfil_aluno,
    buscar_prova_do_modulo,
    calcular_progresso_curso,
    jogo_campo_obter_progresso,
    listar_cursos,
    listar_modulos_do_curso,
    melhor_resultado,
    nota_final_curso,
    obter_tempos_curso,
    trocar_senha_aluno,
)
from utils.helpers import FILIAIS
from webapp.auth.security import gerar_hash_senha, verificar_senha
from webapp.deps import obter_aluno_atual
from webapp.services.jogo_campo import selos_conquistados
from webapp.templating import templates

router = APIRouter()


def _formatar_duracao(segundos) -> str:
    """Converte segundos em um texto curto tipo '2d 3h', '4h 12min' ou '18min'."""
    if not segundos:
        return "-"
    segundos = int(segundos)
    dias, resto = divmod(segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, _ = divmod(resto, 60)
    if dias > 0:
        return f"{dias}d {horas}h"
    if horas > 0:
        return f"{horas}h {minutos}min"
    return f"{minutos}min"


def _historico(aluno_id: str) -> list[dict]:
    from datetime import datetime

    itens = []
    for curso in listar_cursos():
        progresso = calcular_progresso_curso(aluno_id, curso["id"])
        tempos = obter_tempos_curso(aluno_id, curso["id"])
        if progresso <= 0 and not tempos:
            continue

        tempo_conclusao = None
        if tempos and tempos.get("finalizado_em"):
            inicio = datetime.fromisoformat(tempos["iniciado_em"].replace("Z", "+00:00"))
            fim = datetime.fromisoformat(tempos["finalizado_em"].replace("Z", "+00:00"))
            tempo_conclusao = _formatar_duracao((fim - inicio).total_seconds())

        prova_ids = [
            p["id"] for p in (buscar_prova_do_modulo(m["id"]) for m in listar_modulos_do_curso(curso["id"]))
            if p
        ]
        nota_media = nota_final_curso(aluno_id, curso["id"])
        tempo_total_provas = sum(
            (melhor_resultado(aluno_id, pid) or {}).get("tempo_gasto_segundos") or 0
            for pid in prova_ids
        )

        itens.append(
            {
                "curso": curso,
                "progresso_pct": int(progresso * 100),
                "tempo_conclusao": tempo_conclusao,
                "nota_media": nota_media,
                "tempo_total_provas": _formatar_duracao(tempo_total_provas) if tempo_total_provas else None,
            }
        )
    return itens


def _renderizar(request: Request, aluno: dict, **extra):
    progresso_jogo = jogo_campo_obter_progresso(aluno["id"])
    return templates.TemplateResponse(
        request,
        "perfil.html",
        {
            "aluno": aluno,
            "filiais": FILIAIS,
            "historico": _historico(aluno["id"]),
            "selos_jogo": selos_conquistados(progresso_jogo["missoes_completadas"]),
            **extra,
        },
    )


@router.get("/perfil")
def perfil(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    return _renderizar(request, aluno)


@router.post("/perfil/dados")
def salvar_dados(
    request: Request,
    empresa: str = Form(""),
    cargo: str = Form(""),
    filial: str = Form(""),
    telefone: str = Form(""),
    aluno: dict = Depends(obter_aluno_atual),
):
    atualizar_perfil_aluno(aluno["id"], empresa, cargo, filial, telefone)
    aluno = dict(aluno, empresa=empresa, cargo=cargo, filial=filial, telefone=telefone)
    return _renderizar(request, aluno, aba_ativa="dados", sucesso_dados="Dados atualizados com sucesso!")


@router.post("/perfil/senha")
def trocar_senha(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    confirmar: str = Form(...),
    aluno: dict = Depends(obter_aluno_atual),
):
    if not verificar_senha(senha_atual, aluno["senha_hash"]):
        erro = "Senha atual incorreta."
    elif len(nova_senha) < 6:
        erro = "A nova senha deve ter pelo menos 6 caracteres."
    elif nova_senha != confirmar:
        erro = "As senhas não coincidem."
    else:
        trocar_senha_aluno(aluno["id"], gerar_hash_senha(nova_senha))
        return _renderizar(request, aluno, aba_ativa="senha", sucesso_senha="Senha alterada com sucesso!")

    return _renderizar(request, aluno, aba_ativa="senha", erro_senha=erro)


@router.post("/perfil/foto")
async def salvar_foto(request: Request, foto: UploadFile, aluno: dict = Depends(obter_aluno_atual)):
    conteudo = await foto.read()
    if conteudo:
        try:
            nova_url = atualizar_foto_perfil(aluno["id"], conteudo)
        except ImagemInvalidaError as erro:
            return _renderizar(request, aluno, aba_ativa="dados", erro_dados=str(erro))
        aluno = dict(aluno, foto_url=nova_url)
        return _renderizar(request, aluno, aba_ativa="dados", sucesso_dados="Foto atualizada com sucesso!")

    return _renderizar(request, aluno, aba_ativa="dados", erro_dados="Escolha uma foto antes de salvar.")
