"""Admin — Avisos. Porta a aba '📢 Avisos' de modules/admin.py."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import criar_aviso, desativar_aviso, listar_todos_avisos
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


@router.get("/admin/avisos")
def avisos(request: Request, aluno: dict = Depends(exigir_admin), erro: str = ""):
    return templates.TemplateResponse(
        request,
        "admin/avisos.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "avisos": listar_todos_avisos(),
            "erro_cadastro": erro or None,
        },
    )


@router.post("/admin/avisos")
def criar(titulo: str = Form(...), mensagem: str = Form(...), aluno: dict = Depends(exigir_admin)):
    if not titulo.strip() or not mensagem.strip():
        return RedirectResponse("/admin/avisos?erro=Preencha o título e a mensagem.", status_code=303)
    criar_aviso(titulo, mensagem)
    return RedirectResponse("/admin/avisos", status_code=303)


@router.post("/admin/avisos/{aviso_id}/desativar")
def desativar(aviso_id: int, aluno: dict = Depends(exigir_admin)):
    desativar_aviso(aviso_id)
    return RedirectResponse("/admin/avisos", status_code=303)
