"""
Sala de Simulação — página que reúne os 3 simuladores de treinamento
(Campo, Suporte clássico, Suporte por IA) num só lugar. Esses cards
viviam na Início; foram movidos pra cá pra deixar a Início mais enxuta
(só um resumo em números), sem perder o acesso fácil aos simuladores.
"""
from fastapi import APIRouter, Depends, Request

from webapp.services.resumo_jogos import resumo_do_jogo, resumo_do_suporte, resumo_do_suporte_ia
from webapp.deps import obter_aluno_atual
from webapp.templating import templates

router = APIRouter()


@router.get("/simuladores")
def simuladores(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    return templates.TemplateResponse(
        request,
        "simuladores.html",
        {
            "aluno": aluno,
            "jogo": resumo_do_jogo(aluno["id"]),
            "suporte": resumo_do_suporte(aluno["id"]),
            "suporte_ia": resumo_do_suporte_ia(aluno["id"]),
        },
    )
