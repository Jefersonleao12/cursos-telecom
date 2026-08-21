"""
Simulador de Campo — jogo de treinamento com Ordens de Serviço simuladas
(ver webapp/services/jogo_campo.py). Cada ação do jogador (escolher uma
alternativa, avançar de tela) é um POST que atualiza o progresso no banco
e redireciona de volta pra GET /jogo, que sempre renderiza a tela atual —
assim um F5 no meio do jogo nunca perde o lugar nem reenvia a última ação.
"""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from webapp.deps import obter_aluno_atual
from webapp.services.jogo_campo import (
    continuar,
    iniciar_jogo,
    iniciar_missao,
    obter_tela,
    proxima_missao,
    reiniciar,
    responder,
)
from webapp.templating import templates

router = APIRouter()


@router.get("/jogo")
def jogo(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    contexto = obter_tela(aluno["id"])
    return templates.TemplateResponse(request, "jogo/simulador.html", {"aluno": aluno, **contexto})


@router.post("/jogo/iniciar")
def jogo_iniciar(aluno: dict = Depends(obter_aluno_atual)):
    iniciar_jogo(aluno["id"])
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/iniciar-missao")
def jogo_iniciar_missao(aluno: dict = Depends(obter_aluno_atual)):
    iniciar_missao(aluno["id"])
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/responder")
def jogo_responder(opcao: int = Form(...), aluno: dict = Depends(obter_aluno_atual)):
    responder(aluno["id"], opcao)
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/continuar")
def jogo_continuar(aluno: dict = Depends(obter_aluno_atual)):
    continuar(aluno["id"])
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/proxima-missao")
def jogo_proxima_missao(aluno: dict = Depends(obter_aluno_atual)):
    proxima_missao(aluno["id"])
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/reiniciar")
def jogo_reiniciar(aluno: dict = Depends(obter_aluno_atual)):
    reiniciar(aluno["id"])
    return RedirectResponse("/jogo", status_code=303)
