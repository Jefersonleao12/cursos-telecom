"""
Configuração da app nova (FastAPI).

Lê os mesmos segredos que a app antiga, usando
utils.helpers.obter_segredo — sem duplicar a lógica de leitura (essa
função já sabe ler tanto de variável de ambiente quanto de st.secrets
quando disponível, e já limpa espaço/quebra de linha "escondidos").
"""
from functools import lru_cache

from utils.helpers import obter_segredo


class Configuracoes:
    def __init__(self):
        self.supabase_url = obter_segredo("SUPABASE_URL", "")
        self.supabase_service_key = obter_segredo("SUPABASE_SERVICE_KEY", "")
        # Chave própria pra assinar o cookie de sessão — diferente da chave
        # do Supabase (a app antiga reaproveitava a SUPABASE_SERVICE_KEY
        # pra isso; aqui já nasce separada, pra vazar uma não comprometer
        # a outra). Sem valor padrão: se não tiver configurada, a app
        # recusa a subir (ver validar()) em vez de assinar sessões com uma
        # chave previsível.
        self.session_secret = obter_segredo("SESSION_SECRET", "")
        self.whatsapp_phone = obter_segredo("WHATSAPP_PHONE", "")
        self.whatsapp_apikey = obter_segredo("WHATSAPP_APIKEY", "")

    def validar(self):
        """Levanta um erro claro na subida da app se faltar algo essencial,
        em vez de deixar o erro aparecer só na primeira requisição."""
        obrigatorias = {
            "SUPABASE_URL": self.supabase_url,
            "SUPABASE_SERVICE_KEY": self.supabase_service_key,
            "SESSION_SECRET": self.session_secret,
        }
        faltando = [nome for nome, valor in obrigatorias.items() if not valor]
        if faltando:
            raise RuntimeError(
                "Variáveis de ambiente ausentes: " + ", ".join(faltando)
            )


@lru_cache
def obter_configuracoes() -> Configuracoes:
    config = Configuracoes()
    config.validar()
    return config
