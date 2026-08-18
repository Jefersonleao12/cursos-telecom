"""Certificado de capacitação — porta modules/certificado.py (download real via URL, não mais blob)."""
import re

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse

from database.repositorio import (
    buscar_certificado,
    buscar_curso,
    curso_totalmente_concluido,
    emitir_certificado,
    listar_cursos,
    nota_final_curso,
)
from utils.helpers import formatar_data_br, gerar_codigo_verificacao
from webapp.deps import obter_aluno_atual
from webapp.services.certificado import gerar_pdf_certificado
from webapp.templating import templates

router = APIRouter()


def _slug_arquivo(titulo: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", titulo.strip()).strip("_") or "curso"


@router.get("/certificados")
def lista_certificados(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    itens = []
    for curso in listar_cursos():
        if not curso_totalmente_concluido(aluno["id"], curso["id"]):
            continue
        itens.append({"curso": curso, "nota": nota_final_curso(aluno["id"], curso["id"])})

    return templates.TemplateResponse(
        request, "certificados.html", {"aluno": aluno, "itens": itens}
    )


@router.get("/certificados/{curso_id}.pdf")
def baixar_certificado(curso_id: int, aluno: dict = Depends(obter_aluno_atual)):
    curso = buscar_curso(curso_id)
    if curso is None or not curso_totalmente_concluido(aluno["id"], curso_id):
        # Não revela se o curso existe ou só não foi concluído — nos dois
        # casos o aluno não tem nada pra baixar aqui.
        return RedirectResponse("/certificados", status_code=303)

    certificado = buscar_certificado(aluno["id"], curso_id)
    if certificado is None:
        codigo = gerar_codigo_verificacao()
        certificado = emitir_certificado(aluno["id"], curso_id, codigo)

    nota = nota_final_curso(aluno["id"], curso_id)
    pdf_bytes = gerar_pdf_certificado(
        nome_aluno=aluno["nome_completo"],
        empresa=aluno.get("empresa") or "",
        curso_titulo=curso["titulo"],
        instrutor=curso["instrutor"],
        carga_horaria=curso.get("carga_horaria"),
        nota=nota,
        data_emissao=formatar_data_br(certificado["emitido_em"]),
        codigo_verificacao=certificado["codigo_verificacao"],
    )

    nome_arquivo = f"certificado_capacitacao_{_slug_arquivo(curso['titulo'])}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'},
    )
