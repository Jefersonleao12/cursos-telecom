"""Admin — Aulas. Porta a aba '🎬 Aulas' de modules/admin.py."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import (
    criar_aula,
    editar_aula,
    excluir_aula,
    listar_aulas_do_modulo,
    listar_cursos,
    listar_modulos_do_curso,
)
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


@router.get("/admin/aulas")
def aulas(
    request: Request,
    curso_id: int = 0,
    modulo_id: int = 0,
    editar: int = 0,
    aluno: dict = Depends(exigir_admin),
):
    cursos = listar_cursos()
    curso_id = curso_id or (cursos[0]["id"] if cursos else 0)
    modulos = listar_modulos_do_curso(curso_id) if curso_id else []
    if modulo_id not in [m["id"] for m in modulos]:
        modulo_id = modulos[0]["id"] if modulos else 0

    return templates.TemplateResponse(
        request,
        "admin/aulas.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "cursos": cursos,
            "curso_id": curso_id,
            "modulos": modulos,
            "modulo_id": modulo_id,
            "aulas": listar_aulas_do_modulo(modulo_id) if modulo_id else [],
            "editando_id": editar or None,
        },
    )


@router.post("/admin/aulas")
def criar(
    curso_id: int = Form(...),
    modulo_id: int = Form(...),
    titulo: str = Form(...),
    url_video: str = Form(...),
    ordem: int = Form(1),
    duracao_minutos: int = Form(10),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip() and url_video.strip():
        criar_aula(modulo_id, curso_id, titulo, url_video, ordem, duracao_minutos)
    return RedirectResponse(f"/admin/aulas?curso_id={curso_id}&modulo_id={modulo_id}", status_code=303)


@router.post("/admin/aulas/{aula_id}/editar")
def editar(
    aula_id: int,
    curso_id: int = Form(...),
    modulo_id: int = Form(...),
    titulo: str = Form(...),
    url_video: str = Form(...),
    ordem: int = Form(1),
    duracao_minutos: int = Form(10),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip() and url_video.strip():
        editar_aula(aula_id, titulo, url_video, ordem, duracao_minutos)
    return RedirectResponse(f"/admin/aulas?curso_id={curso_id}&modulo_id={modulo_id}", status_code=303)


@router.post("/admin/aulas/{aula_id}/excluir")
def excluir(
    aula_id: int,
    curso_id: int = Form(...),
    modulo_id: int = Form(...),
    aluno: dict = Depends(exigir_admin),
):
    excluir_aula(aula_id)
    return RedirectResponse(f"/admin/aulas?curso_id={curso_id}&modulo_id={modulo_id}", status_code=303)
