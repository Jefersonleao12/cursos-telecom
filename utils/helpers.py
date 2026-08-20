"""
Funções utilitárias usadas em várias partes do sistema.
Mantê-las separadas facilita testar e reaproveitar o código.

Sem dependência de nenhum framework de UI.
"""
import os
import re
import uuid
from datetime import datetime


def obter_segredo(chave: str, default=None):
    """
    Lê uma credencial (Supabase, WhatsApp etc.) de variável de ambiente do
    sistema operacional.

    Também limpa espaços/quebras de linha "escondidos" que podem entrar
    sem querer ao colar um valor longo (o campo de variáveis de ambiente
    de um painel de hospedagem, por exemplo, quebra a linha visualmente
    pra exibir — o que é só aparência — mas se uma quebra de linha real
    ficar no meio do valor colado, fica impossível notar só olhando, e
    uma chave JWT do Supabase com qualquer espaço/quebra vira "Invalid
    API key" na hora. Nem URL nem chave de API têm espaço de verdade,
    então é seguro remover.
    """
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


def somente_digitos(texto: str) -> str:
    """Remove tudo que não for número (usado pra CPF/telefone digitados com ou sem pontuação)."""
    return re.sub(r"\D", "", texto or "")


def cpf_valido(cpf: str) -> bool:
    """
    Valida um CPF (só o formato/dígitos verificadores, não confere se a
    pessoa existe de verdade) — aceita com ou sem pontuação
    (000.000.000-00 ou 00000000000).
    """
    digitos = somente_digitos(cpf)
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        return False

    def _digito_verificador(parcial: str) -> str:
        soma = sum(int(d) * peso for d, peso in zip(parcial, range(len(parcial) + 1, 1, -1)))
        resto = (soma * 10) % 11
        return str(resto if resto < 10 else 0)

    d1 = _digito_verificador(digitos[:9])
    d2 = _digito_verificador(digitos[:9] + d1)
    return digitos[-2:] == d1 + d2


def formatar_cpf(cpf: str) -> str:
    """Formata um CPF de 11 dígitos como 000.000.000-00 (só para exibição)."""
    digitos = somente_digitos(cpf)
    if len(digitos) != 11:
        return cpf or ""
    return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"


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
