"""
Cursos: lista (Fase 2) e detalhe (Fase 3) — módulos/aulas com desbloqueio
sequencial, vídeo (Drive/YouTube/outro) com gate de tempo mínimo verificado
no servidor, e prova por módulo.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool

from database.repositorio import (
    buscar_aula,
    buscar_curso,
    calcular_progresso_curso,
    curso_totalmente_concluido,
    progresso_e_conclusao_do_aluno,
    finalizar_progresso_curso,
    listar_cursos,
    marcar_aula_concluida,
    registrar_inicio_curso,
    salvar_resultado_prova,
)
from webapp.deps import obter_aluno_atual
from webapp.services.progresso_curso import calcular_estado_curso, calcular_gate_video, pode_concluir_aula
from webapp.services.video import info_embed_video
from webapp.templating import templates

router = APIRouter()


def _status_progresso(progresso: float) -> tuple[str, str]:
    if progresso >= 1.0:
        return "concluido", "✅ Concluído"
    if progresso > 0:
        return "andamento", "⏳ Em andamento"
    return "novo", "🆕 Não iniciado"


@router.get("/cursos")
def lista_cursos(request: Request, q: str = "", aluno: dict = Depends(obter_aluno_atual)):
    cursos = listar_cursos()

    termo = q.lower().strip()
    if termo:
        cursos = [c for c in cursos if termo in c["titulo"].lower()]

    # Uma consulta só pro progresso de todos os cursos (antes era um laço
    # curso a curso, cada volta com suas próprias idas até o Supabase).
    progresso_por_curso, _ = progresso_e_conclusao_do_aluno(aluno["id"])

    itens = []
    for curso in cursos:
        progresso = progresso_por_curso.get(curso["id"], 0.0)
        classe, rotulo = _status_progresso(progresso)
        itens.append(
            {
                "curso": curso,
                "progresso": progresso,
                "progresso_pct": int(progresso * 100),
                "status_classe": classe,
                "status_rotulo": rotulo,
            }
        )

    return templates.TemplateResponse(
        request,
        "cursos/lista.html",
        {"aluno": aluno, "itens": itens, "termo_busca": q},
    )


def _renderizar_detalhe(request: Request, curso: dict, aluno: dict, *, erro_prova_modulo_id=None, erro_prova_msg=None):
    modulos_estado = calcular_estado_curso(aluno["id"], curso["id"])

    for item in modulos_estado:
        for aula_estado in item["aulas"]:
            aula = aula_estado["aula"]
            aula_estado["embed"] = info_embed_video(aula.get("url_video"))
            if aula_estado["desbloqueada"] and not aula_estado["concluida"]:
                aula_estado["segundos_restantes"] = calcular_gate_video(aluno["id"], aula)
            else:
                aula_estado["segundos_restantes"] = 0

    progresso_geral = calcular_progresso_curso(aluno["id"], curso["id"])
    curso_completo_agora = bool(modulos_estado) and all(m["completo"] for m in modulos_estado)

    return templates.TemplateResponse(
        request,
        "cursos/detalhe.html",
        {
            "aluno": aluno,
            "curso": curso,
            "modulos_estado": modulos_estado,
            "progresso_geral": progresso_geral,
            "progresso_geral_pct": int(progresso_geral * 100),
            "curso_completo_agora": curso_completo_agora,
            "erro_prova_modulo_id": erro_prova_modulo_id,
            "erro_prova_msg": erro_prova_msg,
        },
    )


@router.get("/cursos/{curso_id}")
def detalhe_curso(request: Request, curso_id: int, aluno: dict = Depends(obter_aluno_atual)):
    curso = buscar_curso(curso_id)
    if curso is None:
        return templates.TemplateResponse(
            request, "cursos/nao_encontrado.html", {"aluno": aluno}, status_code=404
        )

    registrar_inicio_curso(aluno["id"], curso_id)
    return _renderizar_detalhe(request, curso, aluno)


@router.post("/cursos/{curso_id}/aulas/{aula_id}/concluir")
def concluir_aula(curso_id: int, aula_id: int, aluno: dict = Depends(obter_aluno_atual)):
    aula = buscar_aula(aula_id)
    if aula and aula.get("curso_id") == curso_id:
        # Confere de novo no servidor que a aula está mesmo desbloqueada
        # (aula anterior concluída) antes de aceitar — o botão já vem
        # desabilitado na tela pra isso, mas um POST direto não pode
        # contornar a trava.
        modulos_estado = calcular_estado_curso(aluno["id"], curso_id)
        aula_liberada = any(
            ae["aula"]["id"] == aula_id and ae["desbloqueada"]
            for item in modulos_estado
            for ae in item["aulas"]
        )
        if aula_liberada and pode_concluir_aula(aluno["id"], aula):
            marcar_aula_concluida(aluno["id"], aula_id)
            # Um módulo sem prova fica completo assim que a última aula é
            # concluída (sem passar pelo fluxo de aprovação da prova, que
            # é o outro lugar que fecha o curso) — confere aqui também,
            # senão progresso_cursos.finalizado_em nunca seria preenchido
            # pra cursos cujo último módulo não tem avaliação.
            if curso_totalmente_concluido(aluno["id"], curso_id):
                finalizar_progresso_curso(aluno["id"], curso_id)

    return RedirectResponse(f"/cursos/{curso_id}#aula-{aula_id}", status_code=303)


@router.post("/cursos/{curso_id}/modulos/{modulo_id}/prova")
async def enviar_prova(request: Request, curso_id: int, modulo_id: int, aluno: dict = Depends(obter_aluno_atual)):
    # await request.form() precisa rodar no event loop (é I/O assíncrono de
    # verdade), mas o resto da função inteira é síncrono e bate várias vezes
    # no Supabase — roda tudo isso numa thread separada (run_in_threadpool)
    # pra não travar o processamento das requisições de outros alunos
    # enquanto a prova é corrigida e salva.
    dados_form = await request.form()
    respostas_brutas = dict(dados_form)
    return await run_in_threadpool(_processar_prova, request, curso_id, modulo_id, aluno, respostas_brutas)


def _processar_prova(request: Request, curso_id: int, modulo_id: int, aluno: dict, respostas_brutas: dict):
    curso = buscar_curso(curso_id)
    if curso is None:
        return templates.TemplateResponse(
            request, "cursos/nao_encontrado.html", {"aluno": aluno}, status_code=404
        )

    modulos_estado = calcular_estado_curso(aluno["id"], curso_id)
    item = next((m for m in modulos_estado if m["modulo"]["id"] == modulo_id), None)

    if not item or not item["prova"] or not item["perguntas_prova"]:
        return RedirectResponse(f"/cursos/{curso_id}#modulo-{modulo_id}", status_code=303)

    resultado_anterior = item["resultado_prova"]
    if resultado_anterior and (
        resultado_anterior["aprovado"] or not resultado_anterior.get("liberado_para_nova_tentativa")
    ):
        # Já aprovado, ou reprovado e sem liberação — não processa de novo.
        return RedirectResponse(f"/cursos/{curso_id}#modulo-{modulo_id}", status_code=303)

    prova = item["prova"]
    perguntas = item["perguntas_prova"]
    respostas = {p["id"]: respostas_brutas.get(f"pergunta_{p['id']}") for p in perguntas}

    if any(resposta is None for resposta in respostas.values()):
        return _renderizar_detalhe(
            request,
            curso,
            aluno,
            erro_prova_modulo_id=modulo_id,
            erro_prova_msg="Responda todas as perguntas antes de enviar.",
        )

    acertos = sum(1 for p in perguntas if respostas[p["id"]] == p["resposta_correta"])
    nota = round((acertos / len(perguntas)) * 10, 1)
    aprovado = nota >= prova["nota_minima"]

    salvar_resultado_prova(aluno["id"], prova["id"], nota, aprovado, tempo_gasto_segundos=None)

    if aprovado and curso_totalmente_concluido(aluno["id"], curso_id):
        finalizar_progresso_curso(aluno["id"], curso_id)

    return RedirectResponse(f"/cursos/{curso_id}#modulo-{modulo_id}", status_code=303)
