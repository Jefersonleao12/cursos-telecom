"""
Lista de cursos. Fase 2 do plano de reescrita cobre só a listagem (busca +
progresso); o detalhe do curso (módulos/aulas com desbloqueio sequencial,
provas, rastreador do YouTube) é a Fase 3.
"""
from fastapi import APIRouter, Depends, Request

from database.repositorio import calcular_progresso_curso, listar_cursos
from webapp.deps import obter_aluno_atual
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

    itens = []
    for curso in cursos:
        progresso = calcular_progresso_curso(aluno["id"], curso["id"])
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


@router.get("/cursos/{curso_id}")
def detalhe_curso(request: Request, curso_id: int, aluno: dict = Depends(obter_aluno_atual)):
    # Desbloqueio de módulos/aulas, provas e certificado chegam na Fase 3
    # do plano — por enquanto só um placeholder pra não deixar o link
    # "Acessar curso" quebrado.
    return templates.TemplateResponse(
        request,
        "cursos/em_construcao.html",
        {"aluno": aluno, "curso_id": curso_id},
    )
