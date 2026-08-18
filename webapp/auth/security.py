"""
Senha (bcrypt) e token de sessão (HMAC) — portado de modules/auth.py.

Duas diferenças em relação à app antiga:
1. A chave de assinatura do token agora é a SESSION_SECRET própria (ver
   webapp/config.py), não mais a SUPABASE_SERVICE_KEY reaproveitada.
2. O token deixa de viajar pela URL/localStorage: webapp/auth/cookies.py
   guarda o mesmo token num cookie httponly. A lógica de gerar/validar o
   token em si (HMAC + validade) é idêntica.
"""
import hashlib
import hmac
import time

import bcrypt

from webapp.config import obter_configuracoes

# Sessão fica válida por 30 dias (o token é renovado a cada novo login) —
# mesma duração da app antiga.
DURACAO_SESSAO_SEGUNDOS = 30 * 24 * 60 * 60


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha digitada em um hash seguro (irreversível)."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha_digitada: str, senha_hash_salva: str) -> bool:
    """Confere se a senha digitada corresponde ao hash salvo no banco."""
    return bcrypt.checkpw(senha_digitada.encode("utf-8"), senha_hash_salva.encode("utf-8"))


def _chave_secreta() -> bytes:
    segredo = obter_configuracoes().session_secret
    return f"cursos-telecom::token-sessao::{segredo}".encode("utf-8")


def gerar_token_sessao(aluno_id: str) -> str:
    validade = int(time.time()) + DURACAO_SESSAO_SEGUNDOS
    mensagem = f"{aluno_id}.{validade}"
    assinatura = hmac.new(_chave_secreta(), mensagem.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{mensagem}.{assinatura}"


def validar_token_sessao(token: str) -> str | None:
    """Retorna o aluno_id se o token for válido e ainda não tiver expirado, senão None."""
    try:
        aluno_id, validade_str, assinatura = token.split(".")
        validade = int(validade_str)
    except (ValueError, AttributeError):
        return None

    mensagem = f"{aluno_id}.{validade_str}"
    assinatura_esperada = hmac.new(_chave_secreta(), mensagem.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(assinatura, assinatura_esperada):
        return None  # token adulterado ou assinado com outra chave
    if validade < int(time.time()):
        return None  # expirado

    return aluno_id
