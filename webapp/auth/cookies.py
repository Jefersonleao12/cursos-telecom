"""
Cookie de sessão httponly — substitui o mecanismo de URL + localStorage da
app antiga (um contorno que só existia porque o Streamlit não dá acesso a
cookies de verdade). Mais simples e mais seguro: o navegador manda o
cookie sozinho em toda requisição, o JavaScript da página nunca enxerga o
token, e não sobra rastro na URL.
"""
from fastapi import Response

from webapp.auth.security import DURACAO_SESSAO_SEGUNDOS

NOME_COOKIE = "sessao"


def definir_cookie_sessao(response: Response, token: str) -> None:
    response.set_cookie(
        key=NOME_COOKIE,
        value=token,
        max_age=DURACAO_SESSAO_SEGUNDOS,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )


def limpar_cookie_sessao(response: Response) -> None:
    response.delete_cookie(key=NOME_COOKIE, path="/")
