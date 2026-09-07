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
from webapp.seguranca.limite_taxa import ia_por_aluno, texto_de_espera
from webapp.services.jogo_suporte_ia import (
    enviar_mensagem,
    iniciar_jogo,
    obter_tela,
    proximo_atendimento,
    reiniciar,
)
from webapp.templating import templates

router = APIRouter()

# Um atendimento inteiro termina em no máximo 10 turnos (_MAX_TURNOS no
# serviço), e uma fala de atendente cabe de sobra aqui. O teto existe porque
# cada mensagem vira uma chamada paga ao Gemini, cobrada por quantidade de
# texto: sem ele, um único aluno consegue enviar um livro por requisição.
_LIMITE_CARACTERES_MENSAGEM = 1500


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
    def recusar(aviso: str, rascunho: str = ""):
        contexto = obter_tela(aluno["id"])
        return templates.TemplateResponse(
            request, "jogo/suporte_ia.html",
            {"aluno": aluno, "erro_ia": aviso, "rascunho": rascunho, **contexto},
        )

    espera = ia_por_aluno.segundos_de_bloqueio(aluno["id"])
    if espera:
        return recusar(
            f"Você mandou muitas mensagens seguidas. Aguarde {texto_de_espera(espera)} "
            "para continuar o atendimento.",
            rascunho=mensagem[:_LIMITE_CARACTERES_MENSAGEM],
        )

    if len(mensagem) > _LIMITE_CARACTERES_MENSAGEM:
        return recusar(
            f"Sua mensagem passou de {_LIMITE_CARACTERES_MENSAGEM} caracteres. "
            "Resuma o que você diria ao cliente e envie de novo.",
            rascunho=mensagem[:_LIMITE_CARACTERES_MENSAGEM],
        )

    # Cada envio conta, dê certo ou não: o custo da chamada acontece de todo
    # jeito, e é justamente o repetir sem parar que precisa ser contido.
    ia_por_aluno.registrar_falha(aluno["id"])

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
