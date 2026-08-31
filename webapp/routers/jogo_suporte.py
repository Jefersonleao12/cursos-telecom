"""
Simulador de Suporte — jogo de treinamento de atendimento ao cliente por
chat (ver webapp/services/jogo_suporte.py). Mesmo padrão do Simulador de
Campo: cada ação do jogador é um POST que atualiza o progresso no banco e
redireciona de volta pra GET /suporte, que sempre renderiza a tela atual.
"""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from webapp.deps import obter_aluno_atual
from webapp.services.jogo_suporte import (
    continuar,
    iniciar_atendimento,
    iniciar_jogo,
    obter_tela,
    proximo_atendimento,
    reiniciar,
    responder,
)
from webapp.templating import templates

router = APIRouter()


@router.get("/suporte")
def suporte(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    contexto = obter_tela(aluno["id"])
    return templates.TemplateResponse(request, "jogo/suporte.html", {"aluno": aluno, **contexto})


@router.post("/suporte/iniciar")
def suporte_iniciar(aluno: dict = Depends(obter_aluno_atual)):
    iniciar_jogo(aluno["id"])
    return RedirectResponse("/suporte", status_code=303)


@router.post("/suporte/iniciar-atendimento")
def suporte_iniciar_atendimento(aluno: dict = Depends(obter_aluno_atual)):
    iniciar_atendimento(aluno["id"])
    return RedirectResponse("/suporte", status_code=303)


@router.post("/suporte/responder")
def suporte_responder(opcao: int = Form(...), aluno: dict = Depends(obter_aluno_atual)):
    responder(aluno["id"], opcao)
    return RedirectResponse("/suporte", status_code=303)


@router.post("/suporte/continuar")
def suporte_continuar(aluno: dict = Depends(obter_aluno_atual)):
    continuar(aluno["id"])
    return RedirectResponse("/suporte", status_code=303)


@router.post("/suporte/proximo-atendimento")
def suporte_proximo_atendimento(aluno: dict = Depends(obter_aluno_atual)):
    proximo_atendimento(aluno["id"])
    return RedirectResponse("/suporte", status_code=303)


@router.post("/suporte/reiniciar")
def suporte_reiniciar(aluno: dict = Depends(obter_aluno_atual)):
    reiniciar(aluno["id"])
    return RedirectResponse("/suporte", status_code=303)
