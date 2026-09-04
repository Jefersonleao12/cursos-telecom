"""
Simulador de Suporte por IA — modo piloto em chat livre (ver
webapp/services/jogo_suporte_ia.py). Mesmo padrão de POST-então-redireciona
do Simulador de Suporte clássico, com uma exceção: se a chamada ao Gemini
falhar, a rota de enviar mensagem renderiza a tela direto (em vez de
redirecionar) pra mostrar o aviso sem descartar o texto que o aluno digitou.
"""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool

from webapp.deps import obter_aluno_atual
from webapp.services.jogo_suporte_ia import (
    enviar_mensagem,
    iniciar_jogo,
    obter_tela,
    proximo_atendimento,
    reiniciar,
)
from webapp.templating import templates

router = APIRouter()


@router.get("/suporte-ia")
def suporte_ia(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    contexto = obter_tela(aluno["id"])
    return templates.TemplateResponse(request, "jogo/suporte_ia.html", {"aluno": aluno, **contexto})


@router.post("/suporte-ia/iniciar")
def suporte_ia_iniciar(aluno: dict = Depends(obter_aluno_atual)):
    iniciar_jogo(aluno["id"])
    return RedirectResponse("/suporte-ia", status_code=303)


@router.post("/suporte-ia/enviar")
async def suporte_ia_enviar(request: Request, mensagem: str = Form(...), aluno: dict = Depends(obter_aluno_atual)):
    # A chamada ao Gemini é bloqueante (requests) — roda numa thread separada
    # pra não travar o event loop de todo mundo enquanto a IA responde.
    sucesso, erro = await run_in_threadpool(enviar_mensagem, aluno["id"], mensagem)
    if not sucesso:
        contexto = obter_tela(aluno["id"])
        return templates.TemplateResponse(
            request, "jogo/suporte_ia.html",
            {"aluno": aluno, "erro_ia": erro, "rascunho": mensagem, **contexto},
        )
    return RedirectResponse("/suporte-ia", status_code=303)


@router.post("/suporte-ia/proximo-atendimento")
def suporte_ia_proximo_atendimento(aluno: dict = Depends(obter_aluno_atual)):
    proximo_atendimento(aluno["id"])
    return RedirectResponse("/suporte-ia", status_code=303)


@router.post("/suporte-ia/reiniciar")
def suporte_ia_reiniciar(aluno: dict = Depends(obter_aluno_atual)):
    reiniciar(aluno["id"])
    return RedirectResponse("/suporte-ia", status_code=303)
