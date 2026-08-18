"""Admin — Módulos. Porta a aba '🧩 Módulos' de modules/admin.py."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import (
    criar_modulo,
    editar_modulo,
    excluir_modulo,
    listar_cursos,
    listar_modulos_do_curso,
)
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


@router.get("/admin/modulos")
def modulos(
    request: Request,
    curso_id: int = 0,
    editar: int = 0,
    excluir: int = 0,
    aluno: dict = Depends(exigir_admin),
):
    cursos = listar_cursos()
    curso_id = curso_id or (cursos[0]["id"] if cursos else 0)
    return templates.TemplateResponse(
        request,
        "admin/modulos.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "cursos": cursos,
            "curso_id": curso_id,
            "modulos": listar_modulos_do_curso(curso_id) if curso_id else [],
            "editando_id": editar or None,
            "excluindo_id": excluir or None,
        },
    )


@router.post("/admin/modulos")
def criar(
    curso_id: int = Form(...),
    titulo: str = Form(...),
    ordem: int = Form(1),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip():
        criar_modulo(curso_id, titulo, ordem)
    return RedirectResponse(f"/admin/modulos?curso_id={curso_id}", status_code=303)


@router.post("/admin/modulos/{modulo_id}/editar")
def editar(
    modulo_id: int,
    curso_id: int = Form(...),
    titulo: str = Form(...),
    ordem: int = Form(1),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip():
        editar_modulo(modulo_id, titulo, ordem)
    return RedirectResponse(f"/admin/modulos?curso_id={curso_id}", status_code=303)


@router.post("/admin/modulos/{modulo_id}/excluir")
def excluir(modulo_id: int, curso_id: int = Form(...), aluno: dict = Depends(exigir_admin)):
    excluir_modulo(modulo_id)
    return RedirectResponse(f"/admin/modulos?curso_id={curso_id}", status_code=303)
