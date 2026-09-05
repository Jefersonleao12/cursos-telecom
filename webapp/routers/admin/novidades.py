"""Admin — Novidades (o mural técnico da equipe, ver webapp/routers/novidades.py)."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import (
    buscar_novidade,
    categorias_novidades,
    criar_novidade,
    definir_novidade_ativa,
    editar_novidade,
    excluir_novidade,
    listar_novidades,
)
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.services.video import info_embed_video
from webapp.templating import templates

router = APIRouter()

CATEGORIAS_SUGERIDAS = [
    "Configuração",
    "Solução rápida",
    "Procedimento",
    "Equipamento",
    "Aviso técnico",
    "Geral",
]

_NOVA_CATEGORIA = "+ Nova categoria..."


def _renderizar(request: Request, aluno: dict, editando_id: int = None, excluindo_id: int = None, **extra):
    itens = [dict(n, embed=info_embed_video(n.get("video_url"))) for n in listar_novidades(True)]
    # As sugeridas sempre aparecem; as que o admin já criou entram junto,
    # sem repetir, pra ele não precisar redigitar uma categoria própria.
    categorias = CATEGORIAS_SUGERIDAS + [c for c in categorias_novidades() if c not in CATEGORIAS_SUGERIDAS]
    return templates.TemplateResponse(
        request,
        "admin/novidades.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "novidades": itens,
            "categorias": categorias,
            "nova_categoria_opcao": _NOVA_CATEGORIA,
            "editando_id": editando_id,
            "excluindo_id": excluindo_id,
            **extra,
        },
    )


def _categoria_final(categoria_opcao: str, nova_categoria: str) -> str:
    if categoria_opcao == _NOVA_CATEGORIA:
        return nova_categoria.strip()
    return categoria_opcao.strip()


def _erro_de_validacao(titulo: str, categoria: str, video_url: str, conteudo: str):
    """Devolve a mensagem de erro, ou None se estiver tudo certo."""
    if not titulo.strip():
        return "Escreva um título para a novidade."
    if not categoria:
        return "Escolha (ou digite) uma categoria."
    if not conteudo.strip() and not video_url.strip():
        return "Uma novidade precisa de um texto, um vídeo, ou os dois."
    if video_url.strip() and not video_url.strip().lower().startswith(("http://", "https://")):
        return "O link do vídeo precisa começar com http:// ou https://"
    return None


@router.get("/admin/novidades")
def novidades(request: Request, editar: int = 0, excluir: int = 0, aluno: dict = Depends(exigir_admin)):
    return _renderizar(request, aluno, editando_id=editar or None, excluindo_id=excluir or None)


@router.post("/admin/novidades")
def criar(
    request: Request,
    titulo: str = Form(""),
    conteudo: str = Form(""),
    video_url: str = Form(""),
    categoria_opcao: str = Form("Geral"),
    nova_categoria: str = Form(""),
    autor: str = Form(""),
    fixada: str = Form(""),
    aluno: dict = Depends(exigir_admin),
):
    categoria = _categoria_final(categoria_opcao, nova_categoria)
    erro = _erro_de_validacao(titulo, categoria, video_url, conteudo)
    if erro:
        return _renderizar(request, aluno, erro_cadastro=erro)

    criar_novidade(titulo, conteudo, video_url, categoria, autor or aluno["nome_completo"], bool(fixada))
    return RedirectResponse("/admin/novidades", status_code=303)


@router.post("/admin/novidades/{novidade_id}/editar")
def editar(
    request: Request,
    novidade_id: int,
    titulo: str = Form(""),
    conteudo: str = Form(""),
    video_url: str = Form(""),
    categoria_opcao: str = Form("Geral"),
    nova_categoria: str = Form(""),
    autor: str = Form(""),
    fixada: str = Form(""),
    aluno: dict = Depends(exigir_admin),
):
    categoria = _categoria_final(categoria_opcao, nova_categoria)
    erro = _erro_de_validacao(titulo, categoria, video_url, conteudo)
    if erro:
        return _renderizar(request, aluno, editando_id=novidade_id, erro_edicao=erro)

    editar_novidade(novidade_id, titulo, conteudo, video_url, categoria, autor, bool(fixada))
    return RedirectResponse("/admin/novidades", status_code=303)


@router.post("/admin/novidades/{novidade_id}/alternar")
def alternar(novidade_id: int, aluno: dict = Depends(exigir_admin)):
    """Publica ou tira do ar sem apagar — o histórico do que a equipe já
    compartilhou continua guardado."""
    atual = buscar_novidade(novidade_id)
    if atual:
        definir_novidade_ativa(novidade_id, not atual.get("ativa", True))
    return RedirectResponse("/admin/novidades", status_code=303)


@router.post("/admin/novidades/{novidade_id}/excluir")
def excluir(novidade_id: int, aluno: dict = Depends(exigir_admin)):
    excluir_novidade(novidade_id)
    return RedirectResponse("/admin/novidades", status_code=303)
