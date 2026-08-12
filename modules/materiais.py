"""
Módulo de Materiais.

Página onde os alunos encontram links (ex: pastas/arquivos do Google Drive)
disponibilizados pela empresa, organizados por categoria e com uma barra de
busca para localizar rapidamente o que precisam. Cada material é um card
com ícone + título clicável que abre o link em outra aba.
"""
import html

import streamlit as st
import streamlit.components.v1 as components

from database.repositorio import (
    listar_materiais,
    listar_categorias_materiais,
)

_ESTILO_MATERIAIS = """
<style>
    * { box-sizing: border-box; }
    body { margin: 0; font-family: "Source Sans Pro", sans-serif; }
    .material-card {
        display: flex;
        align-items: center;
        gap: .9rem;
        background: #FFFFFF;
        border: 1px solid #E6ECF3;
        border-radius: 12px;
        padding: .9rem 1.1rem;
        text-decoration: none;
        transition: box-shadow .15s ease, transform .15s ease, border-color .15s ease;
    }
    .material-card:hover {
        box-shadow: 0 4px 14px rgba(20, 60, 110, 0.12);
        border-color: #143C6E;
        transform: translateY(-1px);
    }
    .material-icone {
        font-size: 1.8rem;
        line-height: 1;
        flex-shrink: 0;
    }
    .material-texto { min-width: 0; }
    .material-titulo {
        font-weight: 600;
        color: #143C6E;
        font-size: 1rem;
        margin: 0 0 .15rem 0;
    }
    .material-descricao {
        color: #5A6B80;
        font-size: .85rem;
        margin: 0;
    }
    .material-seta {
        margin-left: auto;
        color: #A8B6C8;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
</style>
"""


def _cartao_material(item: dict) -> str:
    icone = html.escape(item.get("icone") or "🔗")
    titulo = html.escape(item.get("titulo") or "")
    descricao = html.escape(item.get("descricao") or "")
    link = html.escape(item.get("link_url") or "#", quote=True)
    bloco_descricao = f'<p class="material-descricao">{descricao}</p>' if descricao else ""
    return f"""
    <a class="material-card" href="{link}" target="_blank" rel="noopener noreferrer">
        <div class="material-icone">{icone}</div>
        <div class="material-texto">
            <p class="material-titulo">{titulo}</p>
            {bloco_descricao}
        </div>
        <div class="material-seta">↗</div>
    </a>
    """


def _altura_estimada(item: dict) -> int:
    base = 62
    if item.get("descricao"):
        base += 22 + (len(item["descricao"]) // 60) * 18
    return base


def tela_materiais():
    st.title("🗂️ Materiais")
    st.caption("Links e pastas disponibilizados pela Norte Tel para consulta — clique num card para abrir.")

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
        # Renderizado com components.html() (não st.markdown) porque título e
        # descrição são texto livre do admin — só um <iframe> isolado evita
        # que Markdown "acidental" no texto quebre a renderização (mesmo
        # motivo do carrossel de destaques e dos avisos na tela Início).
        cartoes = "".join(_cartao_material(item) for item in itens)
        altura_total = sum(_altura_estimada(item) + 12 for item in itens) + 10
        components.html(
            f"{_ESTILO_MATERIAIS}<div style='display:flex; flex-direction:column; gap:.7rem;'>{cartoes}</div>",
            height=altura_total,
            scrolling=True,
        )
        st.write("")
