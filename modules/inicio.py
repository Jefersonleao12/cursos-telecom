"""
Módulo da página Início.

É a primeira tela que o aluno vê ao entrar na plataforma: uma saudação de
acordo com o horário do dia (bom dia / boa tarde / boa noite), um resumo do
progresso, avisos gerais, atalhos rápidos e um canal para dúvidas do dia a dia.
"""
import html
import random
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components

from database.repositorio import (
    enviar_duvida,
    listar_cursos,
    calcular_progresso_curso,
    curso_totalmente_concluido,
    listar_avisos_ativos,
    listar_destaques_ativos,
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

        if curso_totalmente_concluido(aluno_id, curso["id"]):
            certificados += 1

    return {"concluidos": concluidos, "em_andamento": em_andamento, "certificados": certificados}


def _estilos_inicio():
    st.markdown(
        """
        <style>
            @keyframes apareceSuaveInicio {
                from { opacity: 0; transform: translateY(14px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            /* ---------- Cabeçalho / boas-vindas ---------- */
            .inicio-hero {
                background: linear-gradient(150deg, #0F2E56 0%, #143C6E 55%, #1F5AA8 100%);
                border-radius: 18px;
                padding: 1.9rem 2.2rem;
                color: #FFFFFF;
                animation: apareceSuaveInicio 0.5s ease-out;
                box-shadow: 0 12px 30px rgba(20, 60, 110, 0.22);
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1.5rem;
                flex-wrap: wrap;
            }
            .inicio-hero .saudacao {
                font-size: clamp(1.3rem, 3.2vw, 1.7rem);
                font-weight: 700;
                margin-bottom: 0.15rem;
            }
            .inicio-hero .data-hoje {
                font-size: 0.85rem;
                opacity: 0.75;
                text-transform: capitalize;
            }
            .inicio-hero .frase-bloco {
                border-left: 3px solid rgba(255,255,255,0.35);
                padding-left: 1.1rem;
                max-width: 480px;
                font-size: clamp(1.05rem, 2vw, 1.25rem);
                font-style: italic;
                line-height: 1.5;
                opacity: 0.97;
            }

            /* ---------- Cartões de estatística ---------- */
            .stat-card {
                background: #FFFFFF;
                border: 1px solid #E6ECF3;
                border-radius: 14px;
                padding: 1.1rem 1.3rem;
                display: flex;
                align-items: center;
                gap: 0.9rem;
                box-shadow: 0 2px 10px rgba(20, 60, 110, 0.06);
                transition: box-shadow 0.25s ease, transform 0.25s ease;
                height: 100%;
            }
            .stat-card:hover {
                box-shadow: 0 8px 22px rgba(20, 60, 110, 0.14);
                transform: translateY(-2px);
            }
            .stat-card .icone {
                width: 46px;
                height: 46px;
                min-width: 46px;
                border-radius: 12px;
                background: #EAF1FB;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.3rem;
            }
            .stat-card .numero {
                font-size: 1.6rem;
                font-weight: 700;
                color: #143C6E;
                line-height: 1.1;
            }
            .stat-card .rotulo {
                font-size: 0.82rem;
                color: #6B7A8F;
            }

            /* Os estilos do card de aviso e do carrossel de destaques ficam
               dentro dos próprios componentes HTML deles (ver _carrossel_destaques
               e o bloco de avisos em tela_inicio) — não aqui. */

            /* ---------- Cabeçalhos de seção ---------- */
            .secao-titulo {
                font-size: 1.05rem;
                font-weight: 700;
                color: #143C6E;
                margin: 0.3rem 0 0.1rem 0;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .secao-sub {
                color: #6B7A8F;
                font-size: 0.88rem;
                margin-bottom: 0.9rem;
            }

            /* ---------- Cartões de ação rápida ---------- */
            .acao-icone {
                font-size: 1.6rem;
                margin-bottom: 0.3rem;
            }
            .acao-titulo {
                font-weight: 700;
                color: #1A1A1A;
                font-size: 0.98rem;
                margin-bottom: 0.15rem;
            }
            .acao-desc {
                color: #6B7A8F;
                font-size: 0.82rem;
                margin-bottom: 0.7rem;
                min-height: 2.2em;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# CSS reaproveitado pelos dois componentes HTML abaixo (avisos e carrossel
# de destaques). Fica FORA do <style> principal de propósito — ver o
# comentário logo acima de _carrossel_destaques.
_ESTILO_AVISO = """
    html, body { margin: 0; padding: 0; background: transparent; }
    body { font-family: "Source Sans Pro", "Segoe UI", sans-serif; }
    .aviso-card {
        background: #FFF8E8;
        border-left: 4px solid #E3A11C;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
        box-sizing: border-box;
    }
    .aviso-card .aviso-titulo {
        font-weight: 700;
        color: #7A5B0A;
        margin-bottom: 0.15rem;
        font-size: 0.95rem;
    }
    .aviso-card .aviso-texto {
        color: #5C4A1F;
        font-size: 0.9rem;
        line-height: 1.45;
        white-space: pre-wrap;
    }
"""

_ESTILO_DESTAQUES = """
    html, body { margin: 0; padding: 0; background: transparent; }
    body { font-family: "Source Sans Pro", "Segoe UI", sans-serif; }
    .destaques-scroll {
        display: flex;
        align-items: stretch;
        gap: 1rem;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        padding: 4px 4px 12px 4px;
        box-sizing: border-box;
        -webkit-overflow-scrolling: touch;
    }
    .destaques-scroll::-webkit-scrollbar { height: 6px; }
    .destaques-scroll::-webkit-scrollbar-thumb { background: #D7E1EE; border-radius: 999px; }
    .destaque-card {
        flex: 0 0 auto;
        width: 230px;
        scroll-snap-align: start;
        background: #FFFFFF;
        border: 1px solid #E6ECF3;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(20, 60, 110, 0.06);
        display: flex;
        flex-direction: column;
    }
    .destaque-card img {
        width: 100%;
        flex: 0 0 auto;
        aspect-ratio: 4 / 3;
        object-fit: cover;
        display: block;
    }
    .destaque-card .destaque-texto {
        padding: 0.7rem 0.85rem 0.9rem;
        flex: 1 1 auto;
    }
    .destaque-card .destaque-titulo {
        font-weight: 700;
        color: #143C6E;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    .destaque-card .destaque-desc {
        color: #6B7A8F;
        font-size: 0.79rem;
        line-height: 1.4;
    }
"""


def _carrossel_destaques():
    """
    Carrossel horizontal (arraste para o lado) com fotos de destaque — ex:
    técnicos da equipe, trajetória de carreira dentro da empresa. Some por
    completo se o admin não tiver cadastrado nenhum destaque ativo.

    Importante: título/descrição são texto livre digitado pelo admin, e
    isso é renderizado com components.html() (um <iframe> de verdade) em
    vez de st.markdown(unsafe_allow_html=True). O st.markdown passa o
    conteúdo por um interpretador de Markdown ANTES de permitir HTML cru —
    então um simples crase (`), sublinhado (_) ou "#" no início de uma
    linha, digitado por acaso na descrição, já é suficiente pra quebrar a
    montagem da página (vira um bloco de código cru, ou pior). Escapar só
    aspas/`<`/`>` (html.escape) não é suficiente pra evitar isso — só o
    <iframe> isolado do components.html() garante que o texto do admin
    nunca seja interpretado como Markdown nem quebre o HTML dos outros
    cards.
    """
    destaques = listar_destaques_ativos()
    if not destaques:
        return

    st.write("")
    st.markdown('<div class="secao-titulo">🌟 Nossa Equipe</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="secao-sub">Arraste para o lado para conhecer nossos técnicos e trajetórias dentro da empresa.</div>',
        unsafe_allow_html=True,
    )

    cartoes_html = ""
    altura_maxima = 0
    for destaque in destaques:
        titulo_seguro = html.escape(destaque["titulo"])
        foto_url_segura = html.escape(destaque["foto_url"], quote=True)
        descricao_segura = html.escape(destaque["descricao"]) if destaque.get("descricao") else ""

        cartoes_html += f"""
            <div class="destaque-card">
                <img src="{foto_url_segura}" alt="{titulo_seguro}" />
                <div class="destaque-texto">
                    <div class="destaque-titulo">{titulo_seguro}</div>
                    {f'<div class="destaque-desc">{descricao_segura}</div>' if descricao_segura else ''}
                </div>
            </div>
        """
        altura_maxima = max(altura_maxima, _altura_estimada_cartao(destaque))

    pagina_html = f"<style>{_ESTILO_DESTAQUES}</style><div class=\"destaques-scroll\">{cartoes_html}</div>"
    # A altura do quadro acompanha a descrição mais longa entre os destaques
    # ativos (todos os cartões esticam pra ficar do tamanho do maior, veja
    # "align-items: stretch" no CSS acima) — assim a descrição inteira
    # sempre aparece, sem cortar e sem precisar rolar dentro do cartão.
    # scrolling=True fica só como rede de segurança, caso a estimativa erre
    # pra menos numa descrição bem fora do comum.
    components.html(pagina_html, height=min(altura_maxima + 20, 900), scrolling=True)


def _altura_estimada_cartao(destaque: dict) -> int:
    """
    Estima a altura (em pixels) que um cartão do carrossel vai ocupar, com
    base no tanto de texto do título e da descrição. É só uma estimativa
    (não conta quebra de palavra de verdade) — por isso o componente
    também tem scrolling=True como rede de segurança.
    """
    altura_imagem = 172  # cartão de 230px de largura, foto 4:3
    padding_vertical = 42  # 0.7rem + 0.9rem de padding, arredondado com folga

    caracteres_por_linha_titulo = 24
    titulo = destaque["titulo"]
    linhas_titulo = max(1, -(-len(titulo) // caracteres_por_linha_titulo))
    altura_titulo = linhas_titulo * 21

    descricao = destaque.get("descricao") or ""
    caracteres_por_linha_desc = 30
    linhas_desc = -(-len(descricao) // caracteres_por_linha_desc) if descricao else 0
    altura_desc = linhas_desc * 18

    return altura_imagem + padding_vertical + altura_titulo + altura_desc


def tela_inicio():
    # Sorteia uma frase nova toda vez que a página é aberta (sem precisar de botão).
    st.session_state["frase_motivacional"] = random.choice(_FRASES)

    _estilos_inicio()

    saudacao, icone = _saudacao_e_icone()
    primeiro_nome = st.session_state["aluno_nome"].split(" ")[0]

    # ---------------- CABEÇALHO ----------------
    st.markdown(
        f"""
        <div class="inicio-hero">
            <div>
                <div class="saudacao">{icone} {saudacao}, {primeiro_nome}!</div>
                <div class="data-hoje">{_data_por_extenso()}</div>
            </div>
            <div class="frase-bloco">“{st.session_state['frase_motivacional']}”</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- AVISOS ----------------
    # Renderizado com components.html() (não st.markdown) pelo mesmo motivo
    # explicado no docstring de _carrossel_destaques: título/mensagem são
    # texto livre do admin, e só um <iframe> isolado evita que Markdown
    # "acidental" no texto (crase, sublinhado, "#" no início da linha etc.)
    # quebre a renderização.
    avisos = listar_avisos_ativos()
    if avisos:
        st.write("")
        cards_html = ""
        for aviso in avisos:
            titulo_seguro = html.escape(aviso["titulo"])
            mensagem_segura = html.escape(aviso["mensagem"])
            cards_html += f"""
                <div class="aviso-card">
                    <div class="aviso-titulo">📢 {titulo_seguro}</div>
                    <div class="aviso-texto">{mensagem_segura}</div>
                </div>
            """
        pagina_html = f"<style>{_ESTILO_AVISO}</style>{cards_html}"
        # Altura estimada por aviso (título + ~3 linhas de mensagem); o
        # scrolling=True garante que, mesmo se um aviso for bem mais longo
        # que o previsto, ele fica com uma barra de rolagem própria em vez
        # de cortar o conteúdo.
        altura_estimada = min(120 * len(avisos) + 20, 640)
        components.html(pagina_html, height=altura_estimada, scrolling=True)

    # ---------------- RESUMO (estatísticas) ----------------
    st.write("")
    resumo = _resumo_do_aluno(st.session_state["aluno_id"])
    estatisticas = [
        ("📚", str(resumo["em_andamento"]), "Cursos em andamento"),
        ("✅", str(resumo["concluidos"]), "Cursos concluídos"),
        ("🏆", str(resumo["certificados"]), "Certificados de capacitação"),
    ]
    col_a, col_b, col_c = st.columns(3)
    for coluna, (ic, numero, rotulo) in zip((col_a, col_b, col_c), estatisticas):
        with coluna:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="icone">{ic}</div>
                    <div>
                        <div class="numero">{numero}</div>
                        <div class="rotulo">{rotulo}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------------- ACESSO RÁPIDO ----------------
    st.write("")
    st.markdown('<div class="secao-titulo">🧭 Acesso rápido</div>', unsafe_allow_html=True)
    st.markdown('<div class="secao-sub">Vá direto para onde você precisa.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    acoes = [
        (col1, "📚", "Meus Cursos", "Continue de onde parou ou comece um novo curso.", "lista_cursos"),
        (col2, "🏆", "Certificados de Capacitação", "Baixe seus certificados de capacitação dos cursos concluídos.", "certificados"),
        (col3, "🗂️", "Materiais", "Fotos, documentos e arquivos para consulta.", "materiais"),
    ]
    for coluna, ic, titulo, desc, destino in acoes:
        with coluna:
            with st.container(border=True):
                st.markdown(f'<div class="acao-icone">{ic}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="acao-titulo">{titulo}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="acao-desc">{desc}</div>', unsafe_allow_html=True)
                if st.button("Acessar", key=f"acesso_rapido_{destino}", use_container_width=True):
                    st.session_state["pagina_atual"] = destino
                    st.rerun()

    # ---------------- CARROSSEL DE DESTAQUES (equipe/carreira) ----------------
    _carrossel_destaques()

    # ---------------- DÚVIDAS DO DIA A DIA ----------------
    st.write("")
    st.write("")
    st.markdown('<div class="secao-titulo">💬 Tire sua dúvida</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="secao-sub">Escreva sua pergunta e ela chega direto para o time responsável.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
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
