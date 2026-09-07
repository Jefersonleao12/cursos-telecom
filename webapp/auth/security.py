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


# O bcrypt só olha os primeiros 72 bytes da senha; o resto é descartado em
# silêncio. Recusar acima disso evita a situação em que duas senhas diferentes
# abrem a mesma conta, e de quebra impede que alguém mande megabytes de texto
# só para fazer o servidor trabalhar.
TAMANHO_MAXIMO_SENHA = 72
TAMANHO_MINIMO_SENHA = 8


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha digitada em um hash seguro (irreversível)."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha_digitada: str, senha_hash_salva: str) -> bool:
    """Confere se a senha digitada corresponde ao hash salvo no banco."""
    try:
        return bcrypt.checkpw(
            senha_digitada.encode("utf-8")[:TAMANHO_MAXIMO_SENHA],
            senha_hash_salva.encode("utf-8"),
        )
    except (ValueError, TypeError):
        # Hash ausente ou corrompido no banco: é falha de autenticação, não
        # erro 500 — e não pode virar uma porta que se abre sozinha.
        return False


# Hash descartável, gerado uma vez na subida. Serve só para gastar o mesmo
# tempo de CPU quando o CPF digitado não existe (ver consumir_tempo_de_senha).
_HASH_DE_COMPARACAO = gerar_hash_senha("senha-que-nao-abre-conta-nenhuma")


def consumir_tempo_de_senha(senha: str) -> None:
    """Roda uma verificação que sempre falha, só para gastar tempo.

    O bcrypt é lento de propósito. Quando o CPF não existe, pular essa etapa
    faz a resposta voltar muito mais rápido — e essa diferença de tempo, medida
    do lado de fora, revela quais CPFs estão cadastrados mesmo com a mensagem
    de erro sendo idêntica nos dois casos.
    """
    verificar_senha(senha, _HASH_DE_COMPARACAO)


def erro_de_politica_de_senha(nova_senha: str, cpf: str = "", nome: str = "") -> str | None:
    """Devolve a mensagem do problema, ou None se a senha serve.

    A senha inicial de todo aluno é o próprio CPF, que também é o login. Se a
    troca obrigatória aceitar de volta o CPF (ou uma sequência óbvia), a troca
    não protege de nada.
    """
    senha = nova_senha or ""
    if len(senha) < TAMANHO_MINIMO_SENHA:
        return f"A senha deve ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres."
    if len(senha.encode("utf-8")) > TAMANHO_MAXIMO_SENHA:
        return f"A senha deve ter no máximo {TAMANHO_MAXIMO_SENHA} caracteres."
    if senha.isdigit() and len(set(senha)) <= 2:
        return "Escolha uma senha que não seja só um número repetido."

    apenas_digitos = "".join(c for c in senha if c.isdigit())
    if cpf and apenas_digitos and apenas_digitos == "".join(c for c in cpf if c.isdigit()):
        return "A senha não pode ser o seu CPF. Escolha outra."

    comparavel = senha.casefold()
    if comparavel in _SENHAS_PROIBIDAS:
        return "Essa senha é fácil demais de adivinhar. Escolha outra."

    primeiro_nome = (nome or "").strip().split(" ")[0].casefold()
    if len(primeiro_nome) >= 4 and primeiro_nome in comparavel:
        return "A senha não pode conter o seu nome. Escolha outra."

    return None


# Lista curta e proposital: são as senhas que aparecem primeiro em qualquer
# tentativa automatizada, mais as variações previsíveis no contexto da empresa.
_SENHAS_PROIBIDAS = {
    "12345678", "123456789", "1234567890", "senha123", "senha1234",
    "password", "password1", "qwertyui", "abcd1234", "11223344",
    "mudar123", "trocar123", "primeiro123", "telecom123", "nortetel",
    "nortetel123", "internet123", "administrador", "admin123",
}


def _chave_secreta() -> bytes:
    segredo = obter_configuracoes().session_secret
    return f"cursos-telecom::token-sessao::{segredo}".encode("utf-8")


def marca_de_senha(senha_hash: str) -> str:
    """Impressão curta da senha atual, gravada dentro do token de sessão.

    Serve para que trocar a senha derrube todas as sessões abertas. Sem isso,
    um cookie copiado do celular de alguém continuaria funcionando por trinta
    dias mesmo depois da vítima trocar a senha — que é justamente a primeira
    coisa que se faz ao desconfiar de acesso indevido.

    É derivada do hash (que já é irreversível), nunca da senha, e vai só nos
    primeiros dígitos: o suficiente para mudar quando a senha muda, e curto
    demais para servir de pista sobre o hash guardado no banco.
    """
    return hashlib.sha256(f"marca::{senha_hash}".encode("utf-8")).hexdigest()[:16]


def gerar_token_sessao(aluno_id: str, senha_hash: str = "") -> str:
    validade = int(time.time()) + DURACAO_SESSAO_SEGUNDOS
    marca = marca_de_senha(senha_hash) if senha_hash else "-"
    mensagem = f"{aluno_id}.{validade}.{marca}"
    assinatura = hmac.new(_chave_secreta(), mensagem.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{mensagem}.{assinatura}"


def validar_token_sessao(token: str) -> tuple[str, str] | None:
    """Confere assinatura e validade. Devolve (aluno_id, marca_da_senha).

    A marca ainda precisa ser comparada com a senha atual do aluno — isso
    acontece no middleware, que é onde o cadastro é carregado (ver
    webapp/middleware.py).
    """
    try:
        aluno_id, validade_str, marca, assinatura = token.split(".")
        validade = int(validade_str)
    except (ValueError, AttributeError):
        return None

    mensagem = f"{aluno_id}.{validade_str}.{marca}"
    assinatura_esperada = hmac.new(_chave_secreta(), mensagem.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(assinatura, assinatura_esperada):
        return None  # token adulterado ou assinado com outra chave
    if validade < int(time.time()):
        return None  # expirado

    return aluno_id, marca
