"""
Funções utilitárias usadas em várias partes do sistema.
Mantê-las separadas facilita testar e reaproveitar o código.
"""
import re
import uuid
from datetime import datetime


# Lista de filiais (cidades) disponíveis para o aluno selecionar no cadastro.
# Mantida em ordem alfabética para facilitar a leitura no formulário e no painel admin.
FILIAIS = sorted([
    "Cacoal",
    "São Domingos",
    "São Miguel",
    "5 Bec",
    "Alta Floresta",
    "Colniza",
    "Conselvan",
    "Cujubim",
    "Vale do Anari",
    "Theobroma",
    "São Francisco",
    "Pimenta Bueno",
    "Machadinho",
    "Juína",
    "Governador J/ Teixeira",
    "Alto Alegre",
    "Aripuanã",
])


def email_valido(email: str) -> bool:
    """Valida um formato básico de e-mail (ex: nome@empresa.com)."""
    padrao = r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email or "") is not None


def gerar_codigo_verificacao() -> str:
    """Gera um código único e curto para validar a autenticidade de um certificado."""
    return f"CERT-{uuid.uuid4().hex[:10].upper()}"


def formatar_data_br(data) -> str:
    """Formata uma data (string ISO vinda do Supabase ou objeto datetime) no padrão dd/mm/aaaa."""
    if isinstance(data, str):
        try:
            data = datetime.fromisoformat(data.replace("Z", "+00:00"))
        except ValueError:
            return data
    if isinstance(data, datetime):
        return data.strftime("%d/%m/%Y")
    return str(data)
