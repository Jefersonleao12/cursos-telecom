"""Admin — Materiais. Porta a aba '🗂️ Materiais' de modules/admin.py."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import (
    criar_material,
    editar_material,
    excluir_material,
    listar_categorias_materiais,
    listar_materiais,
)
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()

ICONES_MATERIAIS = {
    "📁 Pasta / Drive": "📁",
    "📄 Documento": "📄",
    "📊 Planilha": "📊",
    "🖼️ Fotos": "🖼️",
    "🎥 Vídeo": "🎥",
    "🛠️ Ferramentas": "🛠️",
    "📘 Manual": "📘",
    "🔄 Atualizações": "🔄",
    "🔗 Link genérico": "🔗",
}

_NOVA_CATEGORIA = "+ Nova categoria..."


def _renderizar(request: Request, aluno: dict, editando_id: int = None, **extra):
    return templates.TemplateResponse(
        request,
        "admin/materiais.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "materiais": listar_materiais(),
            "categorias": listar_categorias_materiais(),
            "icones": ICONES_MATERIAIS,
            "nova_categoria_opcao": _NOVA_CATEGORIA,
            "editando_id": editando_id,
            **extra,
        },
    )


@router.get("/admin/materiais")
def materiais(request: Request, editar: int = 0, aluno: dict = Depends(exigir_admin)):
    return _renderizar(request, aluno, editando_id=editar or None)


@router.post("/admin/materiais")
def criar(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(""),
    categoria_opcao: str = Form(...),
    nova_categoria: str = Form(""),
    link_url: str = Form(...),
    icone_label: str = Form(...),
    aluno: dict = Depends(exigir_admin),
):
    categoria_final = nova_categoria.strip() if categoria_opcao == _NOVA_CATEGORIA else categoria_opcao

    erro = None
    if not titulo.strip() or not categoria_final or not link_url.strip():
        erro = "Preencha todos os campos obrigatórios (*)."
    elif not link_url.strip().lower().startswith(("http://", "https://")):
        erro = "O link precisa começar com http:// ou https://"
    else:
        criar_material(titulo, descricao, categoria_final, link_url, ICONES_MATERIAIS.get(icone_label, "🔗"))

    if erro:
        return _renderizar(request, aluno, erro_cadastro=erro)
    return RedirectResponse("/admin/materiais", status_code=303)


@router.post("/admin/materiais/{material_id}/editar")
def editar(
    request: Request,
    material_id: int,
    titulo: str = Form(...),
    descricao: str = Form(""),
    categoria: str = Form(...),
    link_url: str = Form(...),
    icone_label: str = Form(...),
    aluno: dict = Depends(exigir_admin),
):
    if not titulo.strip() or not categoria.strip() or not link_url.strip():
        return _renderizar(
            request, aluno, editando_id=material_id, erro_edicao="Preencha os campos obrigatórios (*)."
        )
    editar_material(material_id, titulo, descricao, categoria, link_url, ICONES_MATERIAIS.get(icone_label, "🔗"))
    return RedirectResponse("/admin/materiais", status_code=303)


@router.post("/admin/materiais/{material_id}/excluir")
def excluir(material_id: int, aluno: dict = Depends(exigir_admin)):
    excluir_material(material_id)
    return RedirectResponse("/admin/materiais", status_code=303)
