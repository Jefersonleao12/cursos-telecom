"""
Cache em memória com TTL (Time To Live).

Cache simples em memória, sem depender de nenhum framework externo.

O FastAPI atende requisições em threads concorrentes, então o cache usa
lock pra evitar corrupção se duas requisições baterem no cache ao mesmo
tempo.
"""
import functools
import threading

from cachetools import TTLCache


def cache_com_ttl(ttl: int, maxsize: int = 256):
    """
    Equivalente a `@st.cache_data(ttl=..., show_spinner=False)`: memoiza
    o retorno da função por `ttl` segundos. A função decorada ganha um
    `.clear()` pra invalidar o cache manualmente — usado depois de toda
    escrita (criar/editar/excluir), exatamente como já era feito com
    `@st.cache_data` (ver os `.clear()` espalhados em repositorio.py).

    Ganha também um `.definir(valor, *args)`: quando uma escrita já devolve
    o registro atualizado (é o caso dos upserts do Supabase), dá pra guardar
    esse valor direto, em vez de jogar o cache fora e obrigar a próxima tela
    a consultar o banco de novo pra ver o que a gente acabou de gravar.
    """
    def decorador(func):
        cache = TTLCache(maxsize=maxsize, ttl=ttl)
        lock = threading.RLock()

        def _chave(args, kwargs):
            return (args, tuple(sorted(kwargs.items())))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            chave = _chave(args, kwargs)
            with lock:
                if chave in cache:
                    return cache[chave]
            resultado = func(*args, **kwargs)
            with lock:
                cache[chave] = resultado
            return resultado

        def definir(valor, *args, **kwargs):
            with lock:
                cache[_chave(args, kwargs)] = valor
            return valor

        wrapper.clear = cache.clear
        wrapper.definir = definir
        return wrapper

    return decorador


def recurso_singleton(func):
    """
    Equivalente a `@st.cache_resource`: chama `func()` só uma vez (na
    primeira chamada) e reaproveita o mesmo resultado depois — usado pro
    cliente do Supabase, que deve ser criado uma única vez por processo.
    """
    lock = threading.RLock()
    estado: dict = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "valor" not in estado:
            with lock:
                if "valor" not in estado:
                    estado["valor"] = func(*args, **kwargs)
        return estado["valor"]

    return wrapper
