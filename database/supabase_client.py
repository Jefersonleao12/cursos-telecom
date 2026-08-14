"""
Módulo responsável por criar e fornecer a conexão única (singleton) com o Supabase.
Toda comunicação com o banco de dados passa por aqui.
"""
import streamlit as st
from supabase import create_client, Client

from utils.helpers import obter_segredo


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    """
    Cria (uma única vez, graças ao @st.cache_resource) o cliente do Supabase.

    As credenciais vêm do arquivo .streamlit/secrets.toml (localmente, ou nas
    "Secrets" do Streamlit Community Cloud) ou de variáveis de ambiente do
    sistema (Render ou qualquer outro host) — ver utils/helpers.obter_segredo.

    IMPORTANTE: usamos a chave "service_role" (não a "anon"), pois este código roda
    inteiramente no servidor (Streamlit), nunca no navegador do usuário. Isso permite
    que o app leia/grave no banco sem precisar configurar políticas de RLS,
    mantendo o projeto simples para quem está começando.
    """
    url = obter_segredo("SUPABASE_URL")
    key = obter_segredo("SUPABASE_SERVICE_KEY")

    if not url or not key:
        st.error(
            "⚠️ As credenciais do Supabase não foram configuradas.\n\n"
            "Preencha `.streamlit/secrets.toml` (localmente), configure as "
            "'Secrets' no painel do Streamlit Community Cloud, ou defina as "
            "variáveis de ambiente SUPABASE_URL e SUPABASE_SERVICE_KEY "
            "(Render ou outro host)."
        )
        st.stop()

    return create_client(url, key)
