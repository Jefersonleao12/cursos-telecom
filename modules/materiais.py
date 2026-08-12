"""
Módulo de Materiais.

Página onde os alunos encontram links (ex: pastas/arquivos do Google Drive)
disponibilizados pela empresa, organizados por categoria e com uma barra de
busca para localizar rapidamente o que precisam. Cada material vira um
cartão com ícone + título + descrição e um botão "Abrir" que leva ao link.
"""
import streamlit as st

from database.repositorio import (
    listar_materiais,
    listar_categorias_materiais,
)


def _estilos_materiais():
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.material-icone) {
            transition: box-shadow .15s ease, border-color .15s ease;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.material-icone):hover {
            box-shadow: 0 4px 14px rgba(20, 60, 110, 0.12);
            border-color: #143C6E;
        }
        .material-icone {
            font-size: 2rem;
            line-height: 1;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def tela_materiais():
    st.title("🗂️ Materiais")
    st.caption("Links e pastas disponibilizados pela Norte Tel para consulta — clique em \"Abrir\" para acessar.")
    _estilos_materiais()

    materiais = listar_materiais()

    if not materiais:
        st.info("Nenhum material disponível no momento. Volte em breve!")
        return

    categorias = listar_categorias_materiais()

    col_busca, col_categoria = st.columns([3, 2])
    with col_busca:
        termo_busca = st.text_input(
            "🔎 Buscar",
            placeholder="Digite o nome do material que você precisa...",
            label_visibility="collapsed",
        )
    with col_categoria:
        categoria_escolhida = st.selectbox(
            "Categoria",
            ["Todas as categorias"] + categorias,
            label_visibility="collapsed",
        )

    # Aplica os filtros escolhidos (categoria e/ou texto buscado)
    filtrados = materiais
    if categoria_escolhida != "Todas as categorias":
        filtrados = [m for m in filtrados if m.get("categoria") == categoria_escolhida]
    if termo_busca:
        termo = termo_busca.lower().strip()
        filtrados = [
            m for m in filtrados
            if termo in (m.get("titulo") or "").lower()
            or termo in (m.get("descricao") or "").lower()
        ]

    st.divider()

    if not filtrados:
        st.warning("Nenhum material encontrado com esses filtros. Tente outra busca.")
        return

    # Agrupa os resultados por categoria, para ficar organizado na tela
    agrupado: dict = {}
    for m in filtrados:
        agrupado.setdefault(m.get("categoria") or "Outros", []).append(m)

    for categoria, itens in agrupado.items():
        st.subheader(f"📂 {categoria}")
        for item in itens:
            with st.container(border=True):
                col_icone, col_texto, col_botao = st.columns([1, 6, 2])
                with col_icone:
                    st.markdown(
                        f'<div class="material-icone">{item.get("icone") or "🔗"}</div>',
                        unsafe_allow_html=True,
                    )
                with col_texto:
                    st.markdown(f"**{item.get('titulo') or ''}**")
                    if item.get("descricao"):
                        st.caption(item["descricao"])
                with col_botao:
                    st.link_button("Abrir ↗", item.get("link_url") or "#", use_container_width=True)
        st.write("")
