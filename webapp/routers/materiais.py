"""Links/pastas disponibilizados pela empresa — porta modules/materiais.py."""
from fastapi import APIRouter, Depends, Request

from database.repositorio import listar_categorias_materiais, listar_materiais
from webapp.deps import obter_aluno_atual
from webapp.templating import templates

router = APIRouter()

_TODAS_CATEGORIAS = "Todas as categorias"


@router.get("/materiais")
def materiais(
    request: Request,
    q: str = "",
    categoria: str = _TODAS_CATEGORIAS,
    aluno: dict = Depends(obter_aluno_atual),
):
    itens = listar_materiais()
    categorias = listar_categorias_materiais()

    if categoria != _TODAS_CATEGORIAS:
        itens = [m for m in itens if m.get("categoria") == categoria]

    termo = q.lower().strip()
    if termo:
        itens = [
            m for m in itens
            if termo in (m.get("titulo") or "").lower()
            or termo in (m.get("descricao") or "").lower()
        ]

    agrupado: dict[str, list] = {}
    for item in itens:
        agrupado.setdefault(item.get("categoria") or "Outros", []).append(item)

    return templates.TemplateResponse(
        request,
        "materiais.html",
        {
            "aluno": aluno,
            "agrupado": agrupado,
            "categorias": categorias,
            "categoria_escolhida": categoria,
            "todas_categorias": _TODAS_CATEGORIAS,
            "termo_busca": q,
            "tem_materiais": bool(listar_materiais()),
        },
    )
