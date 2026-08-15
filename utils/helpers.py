"""
Funções utilitárias usadas em várias partes do sistema.
Mantê-las separadas facilita testar e reaproveitar o código.
"""
import os
import re
import uuid
from datetime import datetime

import streamlit as st


def obter_segredo(chave: str, default=None):
    """
    Lê uma credencial (Supabase, WhatsApp etc.) tanto de `st.secrets`
    (arquivo .streamlit/secrets.toml local, ou "Secrets" no painel do
    Streamlit Community Cloud) quanto de variável de ambiente do sistema
    operacional (usado no Render e em qualquer outro host que não seja o
    Streamlit Community Cloud). Isso deixa o projeto independente de onde
    ele está hospedado, sem precisar mudar nada no código pra trocar de
    provedor — só configurar a credencial do jeito que aquele host espera.

    Também limpa espaços/quebras de linha "escondidos" que podem entrar
    sem querer ao colar um valor longo (o campo de variáveis de ambiente
    do Render, por exemplo, quebra a linha visualmente pra exibir — o que
    é só aparência — mas se uma quebra de linha real ficar no meio do
    valor colado, fica impossível notar só olhando, e uma chave JWT do
    Supabase com qualquer espaço/quebra vira "Invalid API key" na hora.
    Nem URL nem chave de API têm espaço de verdade, então é seguro remover.
    """
    valor = None
    try:
        if chave in st.secrets:
            valor = st.secrets[chave]
    except Exception:
        pass  # sem secrets.toml configurado: cai para a variável de ambiente
    if valor is None:
        valor = os.environ.get(chave, default)
    if isinstance(valor, str):
        valor = re.sub(r"\s+", "", valor)
    return valor


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
