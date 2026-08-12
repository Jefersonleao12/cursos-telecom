"""
Módulo responsável por criar e fornecer a conexão única (singleton) com o Supabase.
Toda comunicação com o banco de dados passa por aqui.
"""
import streamlit as st
from supabase import create_client, Client


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    """
    Cria (uma única vez, graças ao @st.cache_resource) o cliente do Supabase.

    As credenciais vêm do arquivo .streamlit/secrets.toml (em desenvolvimento local)
    ou das "Secrets" configuradas no painel do Streamlit Community Cloud (em produção).

    IMPORTANTE: usamos a chave "service_role" (não a "anon"), pois este código roda
    inteiramente no servidor (Streamlit), nunca no navegador do usuário. Isso permite
    que o app leia/grave no banco sem precisar configurar políticas de RLS,
    mantendo o projeto simples para quem está começando.
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_SERVICE_KEY"]
    except (KeyError, FileNotFoundError):
        st.error(
            "⚠️ As credenciais do Supabase não foram configuradas.\n\n"
            "Preencha `.streamlit/secrets.toml` (localmente) ou configure as "
            "'Secrets' no painel do Streamlit Community Cloud (em produção) "
            "com as chaves SUPABASE_URL e SUPABASE_SERVICE_KEY."
        )
        st.stop()

    return create_client(url, key)
