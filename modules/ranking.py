"""
Módulo de Ranking dos Alunos.

Mostra os alunos com mais progresso na plataforma — uma forma de reconhecer
quem está mais adiantado e incentivar todo mundo a continuar estudando.
Visível para qualquer aluno logado (não é uma tela só de administração).
"""
import html

import streamlit as st
import streamlit.components.v1 as components

from database.repositorio import calcular_ranking_alunos

_MEDALHAS = {1: "🥇", 2: "🥈", 3: "🥉"}
_QUANTIDADE_EXIBIDA = 5

# Nome completo/empresa/filial vêm do cadastro do próprio aluno — texto
# livre. Por isso o "cartão" de cada posição é renderizado com
# components.html() (um <iframe> isolado) em vez de st.markdown com
# unsafe_allow_html: st.markdown passa tudo por um interpretador de
# Markdown antes de permitir HTML cru, e um simples crase/sublinhado/"#"
# digitado por acaso no nome já quebraria a página (o mesmo problema já
# corrigido antes no carrossel de destaques e nos avisos — ver inicio.py).
_ESTILO_CARTAO = """
    html, body { margin: 0; padding: 0; background: transparent; }
    body { font-family: "Source Sans Pro", "Segoe UI", sans-serif; }
    .ranking-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        box-sizing: border-box;
    }
    .ranking-posicao {
        font-size: 1.6rem;
        font-weight: 700;
        width: 2.4rem;
        text-align: center;
        flex-shrink: 0;
    }
    .ranking-foto {
        width: 52px;
        height: 52px;
        min-width: 52px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #E6ECF3;
    }
    .ranking-foto-vazia {
        width: 52px;
        height: 52px;
        min-width: 52px;
        border-radius: 50%;
        background: #EAF1FB;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .ranking-nome {
        font-weight: 700;
        color: #143C6E;
        font-size: 1rem;
    }
    .ranking-detalhe {
        color: #6B7A8F;
        font-size: 0.85rem;
    }
"""


def _cartao_aluno(posicao: int, item: dict, eh_voce: bool):
    medalha = _MEDALHAS.get(posicao, f"{posicao}º")

    if item.get("foto_url"):
        foto_html = f'<img class="ranking-foto" src="{html.escape(item["foto_url"], quote=True)}" alt="" />'
    else:
        foto_html = '<div class="ranking-foto-vazia">👤</div>'

    nome_seguro = html.escape(item["nome_completo"]) + (" (você)" if eh_voce else "")
    detalhes_seguros = html.escape(" · ".join(filter(None, [item.get("empresa"), item.get("filial")])))

    pagina_html = f"""
        <style>{_ESTILO_CARTAO}</style>
        <div class="ranking-card">
            <div class="ranking-posicao">{medalha}</div>
            {foto_html}
            <div>
                <div class="ranking-nome">{nome_seguro}</div>
                <div class="ranking-detalhe">{detalhes_seguros}</div>
            </div>
        </div>
    """
    components.html(pagina_html, height=70, scrolling=False)


def tela_ranking():
    st.title("🏅 Top Alunos")
    st.caption(
        "Os alunos com mais progresso na plataforma — continue estudando "
        "para aparecer aqui e subir de posição!"
    )

    ranking = calcular_ranking_alunos()
    if not ranking:
        st.info("Ninguém começou um curso ainda. Seja o primeiro a aparecer aqui! 💪")
        return

    aluno_id_atual = st.session_state["aluno_id"]

    for posicao, item in enumerate(ranking[:_QUANTIDADE_EXIBIDA], start=1):
        eh_voce = item["aluno_id"] == aluno_id_atual
        with st.container(border=True):
            col_conteudo, col_progresso = st.columns([3, 2])
            with col_conteudo:
                _cartao_aluno(posicao, item, eh_voce)
            with col_progresso:
                rotulo_cursos = "curso concluído" if item["cursos_concluidos"] == 1 else "cursos concluídos"
                st.write(f"🏆 **{item['cursos_concluidos']}** {rotulo_cursos}")
                st.progress(
                    item["progresso_medio"],
                    text=f"{int(item['progresso_medio'] * 100)}% de progresso médio",
                )

    # Mostra a posição do próprio aluno quando ele não está entre os
    # primeiros — assim o incentivo vale pra todo mundo, não só pra quem já
    # está no topo.
    posicao_atual = next(
        (i for i, item in enumerate(ranking, start=1) if item["aluno_id"] == aluno_id_atual),
        None,
    )
    st.divider()
    if posicao_atual is None:
        st.info("Você ainda não apareceu no ranking — comece um curso para entrar na disputa! 💪")
    elif posicao_atual > _QUANTIDADE_EXIBIDA:
        st.info(
            f"📍 Sua posição atual: **{posicao_atual}º lugar** de {len(ranking)} "
            f"alunos no ranking. Continue estudando para subir!"
        )
    else:
        st.success("🎉 Você está entre os primeiros do ranking! Continue assim.")
