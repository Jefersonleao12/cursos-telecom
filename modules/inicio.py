"""
Módulo da página Início.

É a primeira tela que o aluno vê ao entrar na plataforma: uma saudação de
acordo com o horário do dia (bom dia / boa tarde / boa noite) e uma frase
motivacional sorteada, em um cartão visual.
"""
import random
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

from database.repositorio import (
    enviar_duvida,
    listar_cursos,
    calcular_progresso_curso,
    buscar_prova_do_curso,
    melhor_resultado,
    enviar_duvida,
)
from modules.whatsapp import notificar_nova_duvida

# Horário de Rondônia (onde ficam as filiais da Norte Tel), usado para decidir
# a saudação certa mesmo que o servidor da aplicação rode em outro fuso.
_FUSO_HORARIO = ZoneInfo("America/Porto_Velho")

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

_DIAS_SEMANA = {
    0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira", 3: "quinta-feira",
    4: "sexta-feira", 5: "sábado", 6: "domingo",
}
_MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho",
    7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}


def _saudacao_e_icone() -> tuple[str, str]:
    """Escolhe 'Bom dia' / 'Boa tarde' / 'Boa noite' de acordo com a hora atual."""
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
    """Calcula um resumo rápido do progresso do aluno em todos os cursos."""
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

        prova = buscar_prova_do_curso(curso["id"])
        if prova:
            resultado = melhor_resultado(aluno_id, prova["id"])
            if resultado and resultado["aprovado"]:
                certificados += 1

    return {"concluidos": concluidos, "em_andamento": em_andamento, "certificados": certificados}

def tela_inicio():
    # Sorteia uma frase só na primeira vez (fica guardada na sessão), para não
    # trocar sozinha a cada clique — só quando o aluno pedir outra.
    if "frase_motivacional" not in st.session_state:
        st.session_state["frase_motivacional"] = random.choice(_FRASES)

    saudacao, icone = _saudacao_e_icone()
    primeiro_nome = st.session_state["aluno_nome"].split(" ")[0]

    st.markdown(
        """
        <style>
            @keyframes apareceSuaveInicio {{
                from {{ opacity: 0; transform: translateY(14px); }}
                to   {{ opacity: 1; transform: translateY(0); }}
            }}
            .cartao-boas-vindas {{
                background: linear-gradient(135deg, #143C6E 0%, #28316E 55%, #3B4A9E 100%);
                border-radius: 18px;
                padding: clamp(1.8rem, 5vw, 2.8rem) clamp(1.2rem, 4vw, 2.2rem);
                margin-top: 1.5rem;
                color: #FFFFFF;
                text-align: center;
                animation: apareceSuaveInicio 0.6s ease-out;
                box-shadow: 0 12px 30px rgba(20, 60, 110, 0.28);
            }}
            .cartao-boas-vindas .saudacao {{
                font-size: clamp(1.5rem, 4vw, 2.1rem);
                font-weight: 700;
                margin-bottom: 0.3rem;
            }}
            .cartao-boas-vindas .data-hoje {{
                font-size: 0.9rem;
                opacity: 0.85;
                margin-bottom: 1.4rem;
                text-transform: capitalize;
            }}
            .cartao-boas-vindas .frase {{
                font-size: clamp(1rem, 2.3vw, 1.25rem);
                font-style: italic;
                line-height: 1.55;
                max-width: 560px;
                margin: 0 auto;
            }}
        </style>
        <div class="cartao-boas-vindas">
            <div class="saudacao">{icone} {saudacao}, {primeiro_nome}!</div>
            <div class="data-hoje">{_data_por_extenso()}</div>
            <div class="frase">“{st.session_state['frase_motivacional']}”</div>
        </div>
        """,
        unsafe_allow_html=True,
        st.write("")
    resumo = _resumo_do_aluno(st.session_state["aluno_id"])
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("📚 Em andamento", resumo["em_andamento"])
    col_b.metric("✅ Concluídos", resumo["concluidos"])
    col_c.metric("🏆 Certificados", resumo["certificados"])
        )
    st.write("")
    _esq, col_botao, _dir = st.columns([2, 1, 2])
    with col_botao:
        if st.button("🔄 Nova frase", use_container_width=True):
            nova = random.choice(_FRASES)
            # Evita sortear a mesma frase duas vezes seguidas.
            tentativas = 0
            while nova == st.session_state["frase_motivacional"] and tentativas < 10:
                nova = random.choice(_FRASES)
                tentativas += 1
            st.session_state["frase_motivacional"] = nova
            st.rerun()

    st.write("")
    st.subheader("O que você quer fazer agora?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 Ver meus cursos", use_container_width=True):
            st.session_state["pagina_atual"] = "lista_cursos"
            st.rerun()
    with col2:
        if st.button("🏆 Meus certificados", use_container_width=True):
            st.session_state["pagina_atual"] = "certificados"
            st.rerun()
    with col3:
        if st.button("🗂️ Materiais", use_container_width=True):
            st.session_state["pagina_atual"] = "materiais"
            st.rerun()

    # ---------------- DÚVIDAS DO DIA A DIA ----------------
    st.write("")
    st.divider()
    st.subheader("💬 Tire sua dúvida")
    st.caption("Escreva sua pergunta e ela chega direto para o time responsável.")

    with st.form("form_duvida", clear_on_submit=True):
        mensagem_duvida = st.text_area(
            "Sua dúvida",
            placeholder="Digite aqui sua dúvida do dia a dia...",
            label_visibility="collapsed",
            height=100,
        )
        enviar_duvida_btn = st.form_submit_button("Enviar dúvida", type="primary")

    if enviar_duvida_btn:
        if not mensagem_duvida or not mensagem_duvida.strip():
            st.warning("Escreva sua dúvida antes de enviar.")
        else:
            nome_completo = st.session_state["aluno_nome"]
            enviar_duvida(st.session_state["aluno_id"], nome_completo, mensagem_duvida)
            notificar_nova_duvida(nome_completo, mensagem_duvida)
            st.success("Dúvida enviada com sucesso! Em breve alguém vai te responder. 🙌")
