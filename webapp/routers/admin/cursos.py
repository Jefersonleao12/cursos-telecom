"""Admin — Cursos. Porta a aba '📚 Cursos' de modules/admin.py."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import criar_curso, editar_curso, excluir_curso, listar_cursos
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


@router.get("/admin/cursos")
def cursos(request: Request, editar: int = 0, excluir: int = 0, aluno: dict = Depends(exigir_admin)):
    return templates.TemplateResponse(
        request,
        "admin/cursos.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "cursos": listar_cursos(),
            "editando_id": editar or None,
            "excluindo_id": excluir or None,
        },
    )


@router.post("/admin/cursos")
def criar(
    titulo: str = Form(...),
    descricao: str = Form(""),
    instrutor: str = Form(...),
    carga_horaria: int = Form(8),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip() and instrutor.strip():
        criar_curso(titulo, descricao, instrutor, carga_horaria)
    return RedirectResponse("/admin/cursos", status_code=303)


@router.post("/admin/cursos/{curso_id}/editar")
def editar(
    curso_id: int,
    titulo: str = Form(...),
    descricao: str = Form(""),
    instrutor: str = Form(...),
    carga_horaria: int = Form(8),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip() and instrutor.strip():
        editar_curso(curso_id, titulo, descricao, instrutor, carga_horaria)
    return RedirectResponse("/admin/cursos", status_code=303)


@router.post("/admin/cursos/{curso_id}/excluir")
def excluir(curso_id: int, aluno: dict = Depends(exigir_admin)):
    excluir_curso(curso_id)
    return RedirectResponse("/admin/cursos", status_code=303)
