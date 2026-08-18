"""Admin — Dúvidas. Porta a aba '❓ Dúvidas' de modules/admin.py."""
import re

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from database.repositorio import listar_duvidas, marcar_duvida_respondida
from modules.whatsapp import diagnosticar_configuracao
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


def _numero_whatsapp(telefone: str) -> str:
    numero = re.sub(r"\D", "", telefone or "")
    if numero and not numero.startswith("55"):
        numero = f"55{numero}"
    return numero


def _renderizar(request: Request, aluno: dict, pendentes: bool, **extra):
    lista = listar_duvidas(apenas_nao_respondidas=pendentes)
    for d in lista:
        d["numero_whatsapp"] = _numero_whatsapp(d.get("telefone"))

    return templates.TemplateResponse(
        request,
        "admin/duvidas.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "duvidas": lista,
            "apenas_pendentes": pendentes,
            **extra,
        },
    )


@router.get("/admin/duvidas")
def duvidas(request: Request, pendentes: bool = True, aluno: dict = Depends(exigir_admin)):
    return _renderizar(request, aluno, pendentes)


@router.post("/admin/duvidas/{duvida_id}/responder")
def responder(duvida_id: int, pendentes: bool = True, aluno: dict = Depends(exigir_admin)):
    marcar_duvida_respondida(duvida_id)
    return RedirectResponse(f"/admin/duvidas?pendentes={str(pendentes).lower()}", status_code=303)


@router.post("/admin/duvidas/testar-whatsapp")
def testar_whatsapp(request: Request, pendentes: bool = True, aluno: dict = Depends(exigir_admin)):
    sucesso, detalhe = diagnosticar_configuracao()
    return _renderizar(request, aluno, pendentes, teste_resultado=detalhe, teste_ok=sucesso)
