"""
Painel "visão geral" (4 métricas) mostrado no topo de toda página do
admin — porta modules/admin.py:_painel_visao_geral(). Fica num serviço
compartilhado porque, na app antiga, aparecia acima das 11 abas (ou seja,
em qualquer uma delas); aqui cada seção do admin é uma página própria, e
todas precisam do mesmo cabeçalho.
"""
from database.repositorio import (
    listar_cursos,
    listar_duvidas,
    listar_perguntas,
    listar_provas_do_curso,
    listar_todos_alunos,
)


def visao_geral() -> dict:
    cursos = listar_cursos()
    alunos = listar_todos_alunos()
    duvidas_pendentes = listar_duvidas(apenas_nao_respondidas=True)
    total_perguntas = sum(
        len(listar_perguntas(p["id"])) for c in cursos for p in listar_provas_do_curso(c["id"])
    )
    return {
        "cursos": len(cursos),
        "alunos": len(alunos),
        "duvidas_pendentes": len(duvidas_pendentes),
        "perguntas": total_perguntas,
    }
