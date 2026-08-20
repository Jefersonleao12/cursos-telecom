"""Painel do admin — visão geral + aba Dashboard, porta modules/admin.py
(_painel_visao_geral + a aba "📊 Dashboard")."""
from fastapi import APIRouter, Depends, Request

from database.repositorio import (
    contar_alunos_por_filial,
    listar_cursos,
    listar_todos_alunos,
    listar_todos_certificados,
    listar_todos_resultados_provas,
    progresso_e_conclusao_em_lote,
)
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


@router.get("/admin")
def dashboard(request: Request, aluno: dict = Depends(exigir_admin)):
    cursos_todos = listar_cursos()
    alunos_todos = listar_todos_alunos()
    certificados_todos = listar_todos_certificados()
    resultados_todos = listar_todos_resultados_provas()

    alunos_ativos = [a for a in alunos_todos if a.get("ativo", True)]
    taxa_aprovacao = 0
    if resultados_todos:
        taxa_aprovacao = round(sum(1 for r in resultados_todos if r["aprovado"]) / len(resultados_todos) * 100)

    grupos_filial = contar_alunos_por_filial()
    alunos_por_filial = [{"nome": nome, "quantidade": len(lista)} for nome, lista in grupos_filial.items()]
    maximo_filial = max((f["quantidade"] for f in alunos_por_filial), default=0)

    nomes_curso = {c["id"]: c["titulo"] for c in cursos_todos}
    contagem_certificados: dict[str, int] = {}
    for cert in certificados_todos:
        nome = nomes_curso.get(cert["curso_id"], "Curso removido")
        contagem_certificados[nome] = contagem_certificados.get(nome, 0) + 1
    certificados_por_curso = [{"nome": n, "quantidade": q} for n, q in contagem_certificados.items()]
    maximo_certificados = max((c["quantidade"] for c in certificados_por_curso), default=0)

    progresso, _concluido = progresso_e_conclusao_em_lote(alunos_todos, cursos_todos)

    progresso_por_curso = []
    for curso in cursos_todos:
        progressos = [progresso[a["id"]][curso["id"]] for a in alunos_todos]
        iniciados = [p for p in progressos if p > 0]
        if iniciados:
            media = sum(iniciados) / len(iniciados)
            progresso_por_curso.append(
                {"titulo": curso["titulo"], "media_pct": int(media * 100), "alunos": len(iniciados)}
            )

    return templates.TemplateResponse(
        request,
        "admin/dashboard.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "total_alunos_ativos": len(alunos_ativos),
            "total_cursos": len(cursos_todos),
            "total_certificados": len(certificados_todos),
            "taxa_aprovacao": taxa_aprovacao,
            "alunos_por_filial": alunos_por_filial,
            "maximo_filial": maximo_filial,
            "certificados_por_curso": certificados_por_curso,
            "maximo_certificados": maximo_certificados,
            "progresso_por_curso": progresso_por_curso,
        },
    )
