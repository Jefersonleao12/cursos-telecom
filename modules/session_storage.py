"""
Persistência de sessão no navegador (localStorage), independente da URL.

O login do aluno já sobrevive a um F5 através de um token assinado na URL
(ver docstring de modules/auth.py). Mas se o aluno fechar a aba e abrir a
plataforma de novo por um link "limpo" (favorito, digitando o endereço,
ícone da tela de início no PWA), a URL não carrega mais esse token e ele
precisa logar de novo.

Este componente estático guarda o mesmo token também no localStorage do
navegador — que persiste entre aberturas, independente da URL usada — para
que o aluno continue logado "de verdade", como um cookie de sessão.
"""
import os

import streamlit.components.v1 as components

_DIR_COMPONENTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components", "session_storage")
_session_storage = components.declare_component("session_storage", path=_DIR_COMPONENTE)

# Valor sentinela devolvido enquanto a resposta do JavaScript ainda não
# chegou (a primeira renderização de um componente do Streamlit sempre
# volta o "default" antes do round-trip terminar) — distinto de "" (que
# significa "não havia nada salvo").
_AGUARDANDO = "__aguardando__"


def ler_sessao_local():
    """
    Lê o token salvo no localStorage. Retorna:
    - None enquanto a resposta do JavaScript ainda não chegou;
    - "" se não havia nada salvo;
    - o token salvo, se havia.
    """
    valor = _session_storage(acao="ler", token=None, key="session_storage_ler", default=_AGUARDANDO)
    return None if valor == _AGUARDANDO else valor


def gravar_sessao_local(token: str):
    """Salva o token no localStorage (persiste entre aberturas do app/navegador)."""
    _session_storage(acao="gravar", token=token, key="session_storage_gravar")


def apagar_sessao_local():
    """Remove o token salvo no localStorage (logout)."""
    _session_storage(acao="apagar", token=None, key="session_storage_apagar")
