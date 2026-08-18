"""Admin — Filiais. Porta a aba '📍 Filiais' de modules/admin.py (só leitura)."""
from fastapi import APIRouter, Depends, Request

from database.repositorio import contar_alunos_por_filial
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


@router.get("/admin/filiais")
def filiais(request: Request, aluno: dict = Depends(exigir_admin)):
    grupos = contar_alunos_por_filial()
    total_alunos = sum(len(lista) for lista in grupos.values())

    return templates.TemplateResponse(
        request,
        "admin/filiais.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "grupos": grupos,
            "total_alunos": total_alunos,
        },
    )
