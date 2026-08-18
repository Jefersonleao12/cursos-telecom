"""Admin — Provas e Perguntas + liberar tentativa. Porta a aba
'📝 Provas e Perguntas' de modules/admin.py."""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import (
    buscar_prova_do_modulo,
    criar_pergunta,
    criar_prova,
    editar_pergunta,
    editar_prova,
    excluir_pergunta,
    excluir_prova,
    liberar_nova_tentativa,
    listar_cursos,
    listar_modulos_do_curso,
    listar_perguntas,
    listar_resultados_da_prova,
    listar_todos_alunos,
)
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


def _url_secao(curso_id: int, modulo_id: int) -> str:
    return f"/admin/provas?curso_id={curso_id}&modulo_id={modulo_id}"


def _formatar_duracao(segundos) -> str:
    if not segundos:
        return None
    segundos = int(segundos)
    dias, resto = divmod(segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, _ = divmod(resto, 60)
    if dias > 0:
        return f"{dias}d {horas}h"
    if horas > 0:
        return f"{horas}h {minutos}min"
    return f"{minutos}min"


@router.get("/admin/provas")
def provas(
    request: Request,
    curso_id: int = 0,
    modulo_id: int = 0,
    editar_prova: int = 0,
    excluir_prova: int = 0,
    editar_pergunta: int = 0,
    aluno: dict = Depends(exigir_admin),
):
    cursos = listar_cursos()
    curso_id = curso_id or (cursos[0]["id"] if cursos else 0)
    modulos = listar_modulos_do_curso(curso_id) if curso_id else []
    if modulo_id not in [m["id"] for m in modulos]:
        modulo_id = modulos[0]["id"] if modulos else 0

    prova = buscar_prova_do_modulo(modulo_id) if modulo_id else None
    perguntas = listar_perguntas(prova["id"]) if prova else []

    tentativas = []
    if prova:
        todos_resultados = listar_resultados_da_prova(prova["id"])
        nomes_alunos = {a["id"]: a["nome_completo"] for a in listar_todos_alunos()}
        vistos = set()
        for resultado in todos_resultados:
            if resultado["aluno_id"] in vistos:
                continue
            vistos.add(resultado["aluno_id"])
            tentativas.append(
                {
                    "resultado": resultado,
                    "nome": nomes_alunos.get(resultado["aluno_id"], "Aluno removido"),
                    "tempo_formatado": _formatar_duracao(resultado.get("tempo_gasto_segundos")),
                }
            )

    return templates.TemplateResponse(
        request,
        "admin/provas.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "cursos": cursos,
            "curso_id": curso_id,
            "modulos": modulos,
            "modulo_id": modulo_id,
            "prova": prova,
            "perguntas": perguntas,
            "tentativas": tentativas,
            "editando_prova_id": editar_prova or None,
            "excluindo_prova_id": excluir_prova or None,
            "editando_pergunta_id": editar_pergunta or None,
        },
    )


@router.post("/admin/provas")
def criar(
    curso_id: int = Form(...),
    modulo_id: int = Form(...),
    titulo: str = Form("Avaliação do módulo"),
    nota_minima: float = Form(7.0),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip():
        criar_prova(modulo_id, curso_id, titulo, nota_minima)
    return RedirectResponse(_url_secao(curso_id, modulo_id), status_code=303)


@router.post("/admin/provas/{prova_id}/editar")
def editar(
    prova_id: int,
    curso_id: int = Form(...),
    modulo_id: int = Form(...),
    titulo: str = Form(...),
    nota_minima: float = Form(7.0),
    aluno: dict = Depends(exigir_admin),
):
    if titulo.strip():
        editar_prova(prova_id, titulo, nota_minima)
    return RedirectResponse(_url_secao(curso_id, modulo_id), status_code=303)


@router.post("/admin/provas/{prova_id}/excluir")
def excluir(prova_id: int, curso_id: int = Form(...), modulo_id: int = Form(...), aluno: dict = Depends(exigir_admin)):
    excluir_prova(prova_id)
    return RedirectResponse(_url_secao(curso_id, modulo_id), status_code=303)


@router.post("/admin/perguntas")
def criar_pergunta_rota(
    curso_id: int = Form(...),
    modulo_id: int = Form(...),
    prova_id: int = Form(...),
    enunciado: str = Form(...),
    opcao_a: str = Form(...),
    opcao_b: str = Form(...),
    opcao_c: str = Form(...),
    opcao_d: str = Form(...),
    resposta_correta: str = Form(...),
    ordem: int = Form(1),
    aluno: dict = Depends(exigir_admin),
):
    if all([enunciado.strip(), opcao_a.strip(), opcao_b.strip(), opcao_c.strip(), opcao_d.strip()]):
        criar_pergunta(prova_id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta, ordem)
    return RedirectResponse(_url_secao(curso_id, modulo_id), status_code=303)


@router.post("/admin/perguntas/{pergunta_id}/editar")
def editar_pergunta_rota(
    pergunta_id: int,
    curso_id: int = Form(...),
    modulo_id: int = Form(...),
    enunciado: str = Form(...),
    opcao_a: str = Form(...),
    opcao_b: str = Form(...),
    opcao_c: str = Form(...),
    opcao_d: str = Form(...),
    resposta_correta: str = Form(...),
    ordem: int = Form(1),
    aluno: dict = Depends(exigir_admin),
):
    if all([enunciado.strip(), opcao_a.strip(), opcao_b.strip(), opcao_c.strip(), opcao_d.strip()]):
        editar_pergunta(pergunta_id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta, ordem)
    return RedirectResponse(_url_secao(curso_id, modulo_id), status_code=303)


@router.post("/admin/perguntas/{pergunta_id}/excluir")
def excluir_pergunta_rota(
    pergunta_id: int, curso_id: int = Form(...), modulo_id: int = Form(...), aluno: dict = Depends(exigir_admin)
):
    excluir_pergunta(pergunta_id)
    return RedirectResponse(_url_secao(curso_id, modulo_id), status_code=303)


@router.post("/admin/resultados/{resultado_id}/liberar")
def liberar(resultado_id: int, curso_id: int = Form(...), modulo_id: int = Form(...), aluno: dict = Depends(exigir_admin)):
    liberar_nova_tentativa(resultado_id)
    return RedirectResponse(_url_secao(curso_id, modulo_id), status_code=303)
