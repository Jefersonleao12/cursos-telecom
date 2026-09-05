"""Impede o navegador de guardar as PÁGINAS (o HTML) por conta própria.

Os arquivos estáticos (CSS, JS, imagens) a gente manda guardar por muito
tempo de propósito — eles têm ?v=<versão> na URL, então uma versão nova muda
a URL e o navegador busca sozinho.

O HTML é o oposto: a URL é sempre a mesma (/login, /cursos...) e o conteúdo
muda a cada aula concluída, aviso novo ou deploy. Como não estávamos dizendo
nada sobre cache nessas respostas, o navegador ficava livre pra decidir
sozinho — e o Chrome, nesse caso, aplica um cache "por palpite" (heurístico).
O efeito prático: depois de publicar uma correção, o aluno continuava vendo a
tela antiga, e junto com ela o CSS antigo (porque o HTML velho aponta pro
?v= velho, que está guardado por um ano).

"no-cache" não quer dizer "não guarde": quer dizer "pode guardar, mas
pergunte ao servidor antes de usar". Se nada mudou, o servidor responde
"pode usar o que você tem" — barato. Se mudou, vem a página nova na hora.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CacheDeHtmlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resposta = await call_next(request)

        # Só mexe em página HTML. Estático já vem com o seu próprio
        # Cache-Control (ver webapp/static_cache.py) e não pode ser tocado —
        # é justamente o cache longo dele que deixa a navegação instantânea.
        tipo = resposta.headers.get("content-type", "")
        if tipo.startswith("text/html") and "cache-control" not in resposta.headers:
            resposta.headers["Cache-Control"] = "no-cache, must-revalidate"

        return resposta
