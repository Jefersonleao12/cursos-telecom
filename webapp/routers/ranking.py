"""Top alunos por progresso — porta modules/ranking.py."""
from fastapi import APIRouter, Depends, Request

from database.repositorio import (
    calcular_ranking_alunos,
    jogo_campo_missoes_completadas_em_lote,
    jogo_suporte_atendimentos_completados_em_lote,
)
from webapp.deps import obter_aluno_atual
from webapp.services.jogo_campo import selos_conquistados
from webapp.services.jogo_suporte import selos_conquistados as suporte_selos_conquistados
from webapp.templating import templates

router = APIRouter()

_MEDALHAS = {1: "🥇", 2: "🥈", 3: "🥉"}
_QUANTIDADE_EXIBIDA = 5


@router.get("/ranking")
def ranking(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    lista = calcular_ranking_alunos()

    missoes_por_aluno = jogo_campo_missoes_completadas_em_lote(
        [{"id": item["aluno_id"]} for item in lista]
    )
    atendimentos_por_aluno = jogo_suporte_atendimentos_completados_em_lote(
        [{"id": item["aluno_id"]} for item in lista]
    )

    top = []
    for posicao, item in enumerate(lista[:_QUANTIDADE_EXIBIDA], start=1):
        selos_jogo = [
            {**selo, "tipo": "campo"}
            for selo in selos_conquistados(missoes_por_aluno.get(item["aluno_id"], 0))
        ]
        selos_suporte = [
            {**selo, "tipo": "suporte"}
            for selo in suporte_selos_conquistados(atendimentos_por_aluno.get(item["aluno_id"], 0))
        ]
        top.append(
            {
                "posicao": posicao,
                "medalha": _MEDALHAS.get(posicao, f"{posicao}º"),
                "item": item,
                "eh_voce": item["aluno_id"] == aluno["id"],
                "progresso_pct": int(item["progresso_medio"] * 100),
                # Combinados numa lista só pra template poder mostrar os 10
                # primeiros e esconder o resto atrás de um "mostrar mais"
                # (sem isso, um aluno com muitos selos polui o card inteiro).
                "selos": selos_jogo + selos_suporte,
            }
        )

    posicao_atual = next(
        (i for i, item in enumerate(lista, start=1) if item["aluno_id"] == aluno["id"]),
        None,
    )

    return templates.TemplateResponse(
        request,
        "ranking.html",
        {
            "aluno": aluno,
            "top": top,
            "tem_ranking": bool(lista),
            "total_alunos": len(lista),
            "posicao_atual": posicao_atual,
            "quantidade_exibida": _QUANTIDADE_EXIBIDA,
        },
    )
