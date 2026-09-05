"""Arquivos estáticos (CSS, JS, imagens, logo) servidos com cache no navegador.

Sem isso, o navegador do aluno rebaixa o CSS, o Alpine.js e a logo a cada
página aberta — em conexão de celular isso sozinho já custa alguns décimos de
segundo por clique. Com cache, ele baixa uma vez e nas próximas páginas usa o
que já tem, sem nem falar com o servidor.

Segurança contra "ficar preso na versão antiga": os arquivos que mudam com o
código (CSS/JS) são pedidos com `?v=<versão>` no fim (ver webapp/templating.py).
Ao publicar uma versão nova a URL muda, então o navegador é obrigado a buscar
a nova — o cache longo nunca serve conteúdo desatualizado.
"""
from starlette.staticfiles import StaticFiles

# 1 ano pros arquivos versionados (?v=...), 1 dia pro resto (ícones, logo,
# manifest — mudam raramente e não têm versão na URL).
_UM_ANO = 60 * 60 * 24 * 365
_UM_DIA = 60 * 60 * 24


class EstaticosComCache(StaticFiles):
    def file_response(self, full_path, stat_result, scope, status_code=200):
        resposta = super().file_response(full_path, stat_result, scope, status_code)
        versionado = b"v=" in scope.get("query_string", b"")
        idade = _UM_ANO if versionado else _UM_DIA
        imutavel = ", immutable" if versionado else ""
        resposta.headers["Cache-Control"] = f"public, max-age={idade}{imutavel}"
        return resposta
