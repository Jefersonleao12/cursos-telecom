"""Novidades — o mural técnico da equipe.

É o lugar de publicar o que é RECENTE: uma configuração nova, uma solução
rápida que alguém descobriu, um procedimento que mudou. Por isso a tela
lista da mais nova pra mais antiga (e o admin pode fixar uma no topo).

Não se confunde com Materiais, que é acervo permanente de consulta: lá o
aluno vai procurar um manual quando precisa; aqui ele vem ver o que mudou.
"""
from fastapi import APIRouter, Depends, Request

from database.repositorio import categorias_novidades, listar_novidades
from webapp.deps import obter_aluno_atual
from webapp.services.video import info_embed_video
from webapp.templating import templates

router = APIRouter()

_TODAS_CATEGORIAS = "Todas as categorias"


@router.get("/novidades")
def novidades(
    request: Request,
    q: str = "",
    categoria: str = _TODAS_CATEGORIAS,
    aluno: dict = Depends(obter_aluno_atual),
):
    todas = listar_novidades()
    itens = todas

    if categoria != _TODAS_CATEGORIAS:
        itens = [n for n in itens if n.get("categoria") == categoria]

    termo = q.lower().strip()
    if termo:
        itens = [
            n for n in itens
            if termo in (n.get("titulo") or "").lower()
            or termo in (n.get("conteudo") or "").lower()
        ]

    # Prepara o vídeo aqui e não no template: a mesma função que monta o
    # player das aulas dos cursos (YouTube, Drive ou link direto).
    itens = [dict(n, embed=info_embed_video(n.get("video_url"))) for n in itens]

    return templates.TemplateResponse(
        request,
        "novidades.html",
        {
            "aluno": aluno,
            "itens": itens,
            "categorias": categorias_novidades(),
            "categoria_escolhida": categoria,
            "todas_categorias": _TODAS_CATEGORIAS,
            "termo_busca": q,
            "tem_novidades": bool(todas),
        },
    )
