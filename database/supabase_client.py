"""
Módulo responsável por criar e fornecer a conexão única (singleton) com o Supabase.
Toda comunicação com o banco de dados passa por aqui.

Não depende de nenhum framework de UI, só do supabase-py puro.
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

    As credenciais vêm de variáveis de ambiente do sistema (ver
    utils/helpers.obter_segredo).

    IMPORTANTE: usamos a chave "service_role" (não a "anon"), pois este
    código roda inteiramente no servidor, nunca no navegador do usuário.
    Isso permite que a app leia/grave no banco sem precisar configurar
    políticas de RLS — RLS fica desligado de propósito (ver schema.sql).
    """
    url = obter_segredo("SUPABASE_URL")
    key = obter_segredo("SUPABASE_SERVICE_KEY")

    if not url or not key:
        raise ConfiguracaoAusente(
            "As credenciais do Supabase não foram configuradas. Defina as "
            "variáveis de ambiente SUPABASE_URL e SUPABASE_SERVICE_KEY."
        )

    return create_client(url, key)
