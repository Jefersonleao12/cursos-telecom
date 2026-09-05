"""
Tela Início — primeira coisa que o aluno vê depois de logar. Porta o
restante de modules/inicio.py (avisos, carrossel de destaques, resumo de
progresso, acesso rápido e o canal de dúvidas do dia a dia) — a saudação
já tinha sido portada na Fase 1.

Diferença importante em relação à app antiga: lá, título/mensagem de
aviso e título/descrição de destaque são texto livre do admin, e por
isso precisavam ser renderizados num <iframe> isolado (components.html) —
st.markdown passa tudo por um interpretador de Markdown antes de aceitar
HTML cru, e um simples crase ou "#" no início da linha já quebrava a
página. Aqui isso não é necessário: o autoescape nativo do Jinja2 já
protege {{ aviso.titulo }} e {{ destaque.descricao }} da mesma forma,
sem precisar de nenhum contorno.
"""
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request

from database.repositorio import (
    calcular_progresso_curso,
    curso_totalmente_concluido,
    enviar_duvida,
    listar_avisos_ativos,
    listar_cursos,
    listar_destaques_ativos,
)
from webapp.integrations.whatsapp import notificar_nova_duvida
from webapp.services.resumo_jogos import resumo_do_jogo, resumo_do_suporte, resumo_do_suporte_ia
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

_FRASES = [
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "Motivação faz você começar, o hábito faz você continuar.",
    "Não espere pelo momento perfeito, comece hoje, com o que tem.",
    "Hoje é o dia perfeito para dar o primeiro passo.",
    "Você é mais forte do que imagina.",
    "Grandes coisas nunca vêm da zona de conforto.",
    "Encare cada desafio como uma chance de crescimento.",
    "O impossível é só o possível que ainda não foi tentado.",
    "O que você faz hoje pode melhorar todos os amanhãs.",
    "Acredite no poder dos seus sonhos e siga em frente.",
    "Plante foco, colha conquistas.",
    "O seu melhor está por vir.",
    "Faça com medo, mas faça.",
    "O primeiro passo não te leva ao destino, mas te tira do lugar.",
    "Se a oportunidade não bater na sua porta, construa uma porta!",
    "Tenha coragem de dar o salto.",
    "Um dia é preciso parar de sonhar e começar.",
    "A vontade pode tudo.",
    "Arrisque. Se der certo, felicidade. Se der errado, aprendizado.",
    "A coragem não é a ausência do medo, é a persistência apesar dele.",
    "Tome atitude e mude o seu destino.",
    "O melhor momento para recomeçar é agora.",
    "A disciplina liberta.",
    "A constância leva onde o talento sozinho não alcança.",
    "Nós somos o que fazemos repetidamente.",
    "Trabalhe em silêncio e deixe o sucesso fazer barulho.",
    "A excelência é um hábito, não um ato.",
    "Foco no objetivo e força para continuar.",
    "Cada escolha define o seu futuro.",
    "Menos desculpas, mais ação.",
]


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


def _resumo_do_aluno(aluno_id: str) -> dict:
    cursos = listar_cursos()
    concluidos = 0
    em_andamento = 0
    certificados = 0

    for curso in cursos:
        progresso = calcular_progresso_curso(aluno_id, curso["id"])
        if progresso >= 1.0:
            concluidos += 1
        elif progresso > 0:
            em_andamento += 1

        if curso_totalmente_concluido(aluno_id, curso["id"]):
            certificados += 1

    return {"concluidos": concluidos, "em_andamento": em_andamento, "certificados": certificados}


def _renderizar(request: Request, aluno: dict, **extra):
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
            "frase_motivacional": random.choice(_FRASES),
            "avisos": listar_avisos_ativos(),
            "destaques": listar_destaques_ativos(),
            "resumo": _resumo_do_aluno(aluno["id"]),
            "jogo": resumo_do_jogo(aluno["id"]),
            "suporte": resumo_do_suporte(aluno["id"]),
            "suporte_ia": resumo_do_suporte_ia(aluno["id"]),
            **extra,
        },
    )


@router.get("/")
def inicio(request: Request, aluno: dict = Depends(obter_aluno_atual)):
    return _renderizar(request, aluno)


@router.post("/duvida")
def enviar_duvida_rota(
    request: Request,
    background_tasks: BackgroundTasks,
    mensagem: str = Form(...),
    aluno: dict = Depends(obter_aluno_atual),
):
    if not mensagem.strip():
        return _renderizar(request, aluno, erro_duvida="Escreva sua dúvida antes de enviar.")

    telefone = aluno.get("telefone")
    enviar_duvida(aluno["id"], aluno["nome_completo"], mensagem, telefone)
    # O aviso do WhatsApp não precisa segurar a resposta pro aluno — a
    # dúvida já foi salva no banco acima, o WhatsApp é só um aviso extra
    # pra equipe, então roda depois de responder (evita o aluno esperar
    # o timeout de 10s da API do CallMeBot se ela estiver lenta).
    background_tasks.add_task(notificar_nova_duvida, aluno["nome_completo"], mensagem, telefone)
    return _renderizar(request, aluno, sucesso_duvida="Dúvida enviada com sucesso! Em breve alguém vai te responder. 🙌")
