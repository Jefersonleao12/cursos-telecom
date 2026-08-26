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
    abrir_apr,
    chamar_cliente,
    continuar,
    enviar_apr,
    iniciar_jogo,
    iniciar_missao,
    obter_tela,
    proxima_missao,
    reiniciar,
    responder,
    responder_evento_cliente,
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


@router.post("/jogo/chamar-cliente")
def jogo_chamar_cliente(aluno: dict = Depends(obter_aluno_atual)):
    chamar_cliente(aluno["id"])
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/responder-cliente")
def jogo_responder_cliente(resposta: int = Form(...), aluno: dict = Depends(obter_aluno_atual)):
    responder_evento_cliente(aluno["id"], resposta)
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/abrir-apr")
def jogo_abrir_apr(origem: str = Form(...), aluno: dict = Depends(obter_aluno_atual)):
    abrir_apr(aluno["id"], origem)
    return RedirectResponse("/jogo", status_code=303)


@router.post("/jogo/enviar-apr")
def jogo_enviar_apr(
    atividades: list[str] = Form([]),
    subiu_poste: str = Form(None),
    riscos: list[str] = Form([]),
    epis: list[str] = Form([]),
    realizar: str = Form(None),
    justificativa: str = Form(""),
    aluno: dict = Depends(obter_aluno_atual),
):
    enviar_apr(
        aluno["id"],
        atividades=atividades,
        subiu_poste=subiu_poste,
        riscos=riscos,
        epis=epis,
        realizar=realizar,
        justificativa=justificativa,
    )
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
