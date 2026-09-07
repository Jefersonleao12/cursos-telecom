"""
Cabeçalhos de proteção enviados em toda resposta.

Nada aqui substitui a validação feita no servidor — são instruções para o
navegador do aluno, uma segunda linha de defesa para o caso de algum conteúdo
malicioso conseguir entrar numa página.

Sobre a Content-Security-Policy: ela permite script inline ('unsafe-inline') e
avaliação dinâmica ('unsafe-eval') porque o Alpine.js, que move os menus e os
modais do site inteiro, compila as expressões dos atributos x-data/@click em
tempo de execução — sem essas duas permissões a plataforma simplesmente para
de responder aos cliques. O que a política ainda garante, e que é o principal
aqui, é a origem: script só pode vir do nosso próprio domínio, então um texto
injetado numa página não consegue puxar código de fora nem mandar dados de
aluno para um servidor de terceiro. A proteção real contra HTML injetado
continua sendo o escape automático do Jinja2 (nenhum template usa "| safe").
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Onde o vídeo das aulas e das novidades pode ser hospedado (ver
# webapp/services/video.py, que só monta URLs de embed para estes dois).
_ORIGENS_VIDEO = (
    "https://www.youtube-nocookie.com",
    "https://www.youtube.com",
    "https://drive.google.com",
)

_POLITICA = "; ".join([
    "default-src 'self'",
    # ver a explicação no topo do arquivo sobre 'unsafe-inline'/'unsafe-eval'
    "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
    "style-src 'self' 'unsafe-inline'",
    # foto de perfil e imagens de destaque ficam no Storage do Supabase, cuja
    # URL vem de variável de ambiente; imagem não executa código, então
    # liberar https é seguro e evita quebrar quando o projeto muda de host
    "img-src 'self' data: https:",
    "font-src 'self' data:",
    "media-src 'self' https:",
    "connect-src 'self'",
    f"frame-src {' '.join(_ORIGENS_VIDEO)}",
    # ninguém pode embutir a plataforma dentro de outra página: fecha o golpe
    # de sobrepor uma tela falsa por cima da nossa (clickjacking)
    "frame-ancestors 'none'",
    # se algum conteúdo injetado tentar trocar o destino de um formulário, o
    # navegador recusa: senha e dados de aluno não saem para fora do domínio
    "form-action 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "upgrade-insecure-requests",
])

_FIXOS = {
    "Content-Security-Policy": _POLITICA,
    # redundante com frame-ancestors, mantido para navegadores antigos
    "X-Frame-Options": "DENY",
    # impede o navegador de "adivinhar" que um upload é HTML e executá-lo
    "X-Content-Type-Options": "nosniff",
    # o endereço da página não vaza para sites externos (o caminho pode conter
    # o id de um curso, de um certificado...)
    "Referrer-Policy": "strict-origin-when-cross-origin",
    # a plataforma não usa câmera, microfone nem localização
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), interest-cohort=()",
}

# Um ano. Depois da primeira visita, o navegador se recusa a falar com o site
# em HTTP puro — mesmo que alguém consiga forçar um link http:// no meio do
# caminho. Sem includeSubDomains de propósito: o domínio de produção pode ter
# subdomínios servidos por outros serviços.
_HSTS = "max-age=31536000"


class CabecalhosDeSegurancaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resposta = await call_next(request)
        for nome, valor in _FIXOS.items():
            resposta.headers.setdefault(nome, valor)

        # HSTS só faz sentido (e só é respeitado) sobre HTTPS. Atrás do Caddy o
        # esquema real chega em X-Forwarded-Proto.
        esquema = request.headers.get("x-forwarded-proto", request.url.scheme)
        if esquema == "https":
            resposta.headers.setdefault("Strict-Transport-Security", _HSTS)

        return resposta
