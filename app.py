"""
Ponto de entrada da Plataforma de Treinamentos em Telecomunicações.

Responsável por:
1) Configurar a página (título, ícone, layout responsivo para desktop/mobile);
2) Exigir login antes de mostrar qualquer conteúdo;
3) Rotear entre as telas do sistema (cursos, provas, certificados, admin).

Para rodar localmente:  streamlit run app.py
"""
import base64
import streamlit as st
from pathlib import Path

from modules.auth import exigir_login, fazer_logout
from modules.cursos import tela_lista_cursos, tela_detalhe_curso
from modules.provas import tela_prova
from modules.certificado import tela_certificados
from modules.admin import tela_admin


st.set_page_config(
    page_title="Treinamentos Telecom",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ícone (só o "N" circular, sem o texto) usado no topo da barra lateral.
_CAMINHO_ICONE = Path(__file__).resolve().parent / "assets" / "icone.png"


@st.cache_data(show_spinner=False)
def _icone_base64() -> str:
    with open(_CAMINHO_ICONE, "rb") as arquivo:
        return base64.b64encode(arquivo.read()).decode("utf-8")

# CSS simples para deixar formulários e botões mais confortáveis no celular.
# O Streamlit já é responsivo por padrão (a barra lateral vira um menu
# recolhível em telas pequenas), este CSS só refina a aparência.
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;   /* evita que o conteúdo fique esticado em monitores muito largos */
            margin: 0 auto;
        }
        div[data-testid="stForm"] { border: 1px solid #e6e6e6; border-radius: 10px; padding: 1.2rem; }
        div[data-testid="stImage"] { overflow: visible; }
        div[data-testid="stImage"] img { overflow: visible; }
        section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }
        section[data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
            width: 300px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    # 1) Garante que o usuário está logado (mostra login/cadastro e para aqui, se não estiver)
    exigir_login()

    # 2) Define a página padrão, na primeira execução da sessão
    if "pagina_atual" not in st.session_state:
        st.session_state["pagina_atual"] = "lista_cursos"

    # 3) Menu lateral (em celulares, o Streamlit já transforma isto num menu ☰ recolhível)
    with st.sidebar:
        st.markdown(
            f"<div style='text-align:center; margin-top:-0.5rem; margin-bottom:0.3rem;'>"
            f"<img src='data:image/png;base64,{_icone_base64()}' alt='Norte Tel' "
            f"style='width:90px; max-width:35%; height:auto;' />"
            f"</div>",
            unsafe_allow_html=True,
        )

        primeiro_nome = st.session_state["aluno_nome"].split(" ")[0]
        st.markdown(f"### 👋 Olá, {primeiro_nome}!")
        if st.session_state.get("aluno_empresa"):
            st.caption(st.session_state["aluno_empresa"])
        st.divider()

        if st.button("📚 Meus Cursos", use_container_width=True):
            st.session_state["pagina_atual"] = "lista_cursos"
            st.rerun()

        if st.button("🏆 Meus Certificados", use_container_width=True):
            st.session_state["pagina_atual"] = "certificados"
            st.rerun()

        if st.session_state.get("aluno_is_admin"):
            st.divider()
            if st.button("⚙️ Administração", use_container_width=True):
                st.session_state["pagina_atual"] = "admin"
                st.rerun()

        st.divider()
        if st.button("🚪 Sair", use_container_width=True):
            fazer_logout()

    # 4) Roteamento simples entre as telas do sistema
    pagina = st.session_state["pagina_atual"]

    if pagina == "lista_cursos":
        tela_lista_cursos()
    elif pagina == "detalhe_curso":
        tela_detalhe_curso()
    elif pagina == "prova":
        tela_prova()
    elif pagina == "certificados":
        tela_certificados()
    elif pagina == "admin" and st.session_state.get("aluno_is_admin"):
        tela_admin()
    else:
        st.session_state["pagina_atual"] = "lista_cursos"
        st.rerun()


if __name__ == "__main__":
    main()
