"""
Painel "visão geral" (4 métricas) mostrado no topo de toda página do
admin — porta modules/admin.py:_painel_visao_geral(). Fica num serviço
compartilhado porque, na app antiga, aparecia acima das 11 abas (ou seja,
em qualquer uma delas); aqui cada seção do admin é uma página própria, e
todas precisam do mesmo cabeçalho.
"""
from database.repositorio import (
    contar_perguntas,
    listar_cursos,
    listar_duvidas,
    listar_todos_alunos,
)


def visao_geral() -> dict:
    cursos = listar_cursos()
    alunos = listar_todos_alunos()
    duvidas_pendentes = listar_duvidas(apenas_nao_respondidas=True)
    # Uma consulta só (antes: curso → provas → perguntas, dezenas de idas
    # ao banco só pra montar o cabeçalho que aparece em toda página do admin).
    total_perguntas = contar_perguntas()
    return {
        "cursos": len(cursos),
        "alunos": len(alunos),
        "duvidas_pendentes": len(duvidas_pendentes),
        "perguntas": total_perguntas,
    }
