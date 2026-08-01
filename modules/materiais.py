"""
Módulo de Materiais.

Página onde os alunos encontram fotos, documentos e arquivos disponibilizados
pela empresa, organizados por categoria e com uma barra de busca para
localizar rapidamente o que precisam.
"""
import streamlit as st

from database.repositorio import (
    listar_materiais,
    listar_categorias_materiais,
    url_publica_material,
)

# Ícone exibido ao lado de cada material, de acordo com o tipo de arquivo.
_ICONES_POR_TIPO = {
    "pdf": "📄",
    "doc": "📄", "docx": "📄",
    "xls": "📊", "xlsx": "📊", "csv": "📊",
    "ppt": "📊", "pptx": "📊",
    "jpg": "🖼️", "jpeg": "🖼️", "png": "🖼️", "gif": "🖼️", "webp": "🖼️",
    "zip": "🗜️", "rar": "🗜️",
    "mp4": "🎞️", "mov": "🎞️", "avi": "🎞️",
    "mp3": "🎵", "wav": "🎵",
}


def _icone_para(tipo_arquivo: str) -> str:
    return _ICONES_POR_TIPO.get((tipo_arquivo or "").lower(), "📁")


def _formatar_tamanho(tamanho_bytes) -> str:
    """Converte um tamanho em bytes para uma leitura amigável (KB/MB)."""
    if not tamanho_bytes:
        return ""
    tamanho_mb = tamanho_bytes / (1024 * 1024)
    if tamanho_mb >= 1:
        return f"{tamanho_mb:.1f} MB"
    tamanho_kb = tamanho_bytes / 1024
    return f"{tamanho_kb:.0f} KB"


def tela_materiais():
    st.title("🗂️ Materiais")
    st.caption("Fotos, documentos e arquivos disponibilizados pela Norte Tel para consulta e download.")

    materiais = listar_materiais()

    if not materiais:
        st.info("Nenhum material disponível no momento. Volte em breve!")
        return

    categorias = listar_categorias_materiais()

    col_busca, col_categoria = st.columns([3, 2])
    with col_busca:
        termo_busca = st.text_input(
            "🔎 Buscar",
            placeholder="Digite o nome do arquivo que você precisa...",
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
                col_info, col_botao = st.columns([4, 1])
                with col_info:
                    icone = _icone_para(item.get("tipo_arquivo"))
                    st.markdown(f"{icone} **{item['titulo']}**")
                    if item.get("descricao"):
                        st.caption(item["descricao"])
                    tamanho = _formatar_tamanho(item.get("tamanho_bytes"))
                    if tamanho:
                        st.caption(f"Tamanho: {tamanho}")
                with col_botao:
                    url = url_publica_material(item["caminho_storage"])
                    st.link_button("⬇️ Baixar", url, use_container_width=True)
        st.write("")
