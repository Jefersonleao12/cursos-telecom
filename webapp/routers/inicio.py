"""
Tela Início — primeira coisa que o aluno vê depois de logar. Fase 1 do
plano de reescrita cobre só a saudação (mesma lógica de fuso horário fixo
de Rondônia da app antiga, ver modules/inicio.py); avisos, progresso e
destaques entram nas fases seguintes.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request

from webapp.deps import obter_aluno_atual
from webapp.templating import templates

router = APIRouter()

# Horário de Rondônia (onde ficam as filiais da Norte Tel), usado para
# decidir a saudação certa mesmo que o servidor rode em outro fuso.
_FUSO_HORARIO = ZoneInfo("America/Porto_Velho")

_DIAS_SEMANA = {
    0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira", 3: "quinta-feira",
    4: "sexta-feira", 5: "sábado", 6: "domingo",
}
_MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho",
    7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}


def _saudacao_e_icone() -> tuple[str, str]:
    hora = datetime.now(_FUSO_HORARIO).hour
    if 5 <= hora < 12:
        return "Bom dia", "☀️"
    if 12 <= hora < 18:
        return "Boa tarde", "🌤️"
    return "Boa noite", "🌙"


def _data_por_extenso() -> str:
    agora = datetime.now(_FUSO_HORARIO)
    return f"{_DIAS_SEMANA[agora.weekday()]}, {agora.day} de {_MESES[agora.month]} de {agora.year}"


@router.get("/")
def inicio(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    saudacao, icone = _saudacao_e_icone()
    primeiro_nome = (aluno.get("nome_completo") or "").split(" ")[0]
    return templates.TemplateResponse(
        request,
        "inicio.html",
        {
            "aluno": aluno,
            "saudacao": saudacao,
            "icone": icone,
            "primeiro_nome": primeiro_nome,
            "data_por_extenso": _data_por_extenso(),
        },
    )
