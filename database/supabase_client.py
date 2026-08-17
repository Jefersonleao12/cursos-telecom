"""
Módulo responsável por criar e fornecer a conexão única (singleton) com o Supabase.
Toda comunicação com o banco de dados passa por aqui.

Compartilhado pelas duas apps que coexistem durante a migração: a app
antiga (Streamlit, app.py/modules/*.py) e a nova (webapp/, FastAPI) — por
isso não depende de nenhuma das duas, só do supabase-py puro.
"""
from supabase import create_client, Client

from database.cache import recurso_singleton
from utils.helpers import obter_segredo


class ConfiguracaoAusente(RuntimeError):
    """Levantado quando SUPABASE_URL/SUPABASE_SERVICE_KEY não estão configurados."""


@recurso_singleton
def get_supabase_client() -> Client:
    """
    Cria (uma única vez por processo, graças a @recurso_singleton) o
    cliente do Supabase.

    As credenciais vêm do arquivo .streamlit/secrets.toml (localmente, ou
    das "Secrets" do Streamlit Community Cloud) ou de variáveis de
    ambiente do sistema (Render, ou qualquer outro host) — ver
    utils/helpers.obter_segredo.

    IMPORTANTE: usamos a chave "service_role" (não a "anon"), pois este
    código roda inteiramente no servidor, nunca no navegador do usuário.
    Isso permite que a app leia/grave no banco sem precisar configurar
    políticas de RLS — RLS fica desligado de propósito (ver schema.sql).
    """
    url = obter_segredo("SUPABASE_URL")
    key = obter_segredo("SUPABASE_SERVICE_KEY")

    if not url or not key:
        raise ConfiguracaoAusente(
            "As credenciais do Supabase não foram configuradas. Preencha "
            "'.streamlit/secrets.toml' (localmente), configure as 'Secrets' "
            "no painel do Streamlit Community Cloud, ou defina as variáveis "
            "de ambiente SUPABASE_URL e SUPABASE_SERVICE_KEY (Render, "
            "Hugging Face ou outro host)."
        )

    return create_client(url, key)
