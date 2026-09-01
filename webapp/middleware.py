"""
Middleware de autenticação: roda em toda requisição, resolve o aluno logado
a partir do cookie de sessão e decide se deixa passar, manda pro login, ou
manda pra alguma tela obrigatória pendente (troca de senha, depois foto —
nessa ordem, igual à app antiga).

Substitui por completo o mecanismo antigo de "restaurar sessão da URL /
localStorage" (modules/auth.py) — aqui não existe estado "pendente" de
round-trip de JavaScript: o cookie já chega pronto na própria requisição.
"""
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from database.repositorio import buscar_aluno_por_id
from webapp.auth.cookies import NOME_COOKIE, limpar_cookie_sessao
from webapp.auth.security import validar_token_sessao

# Caminhos que não exigem login. As telas obrigatórias (troca de senha,
# foto) NÃO entram aqui de propósito — só quem já está logado pode vê-las.
_CAMINHOS_PUBLICOS = {"/login", "/logout", "/esqueci-senha", "/healthz", "/healthz/banco", "/healthz/rotas", "/sw.js"}
_PREFIXOS_PUBLICOS = ("/static/", "/assets/")

_TROCAR_SENHA = "/trocar-senha-obrigatoria"
_DEFINIR_FOTO = "/definir-foto-obrigatoria"


def _resolver_aluno(request: Request):
    """Retorna (aluno_ou_None, token_invalido). token_invalido indica que
    havia um cookie mas ele não é mais válido (expirado, adulterado, conta
    excluída ou desativada) — usado só para decidir se vale a pena limpar
    o cookie na resposta."""
    token = request.cookies.get(NOME_COOKIE)
    if not token:
        return None, False

    aluno_id = validar_token_sessao(token)
    if not aluno_id:
        return None, True

    aluno = buscar_aluno_por_id(aluno_id)
    if not aluno or not aluno.get("ativo", True):
        return None, True

    return aluno, False


class AutenticacaoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # _resolver_aluno faz uma consulta síncrona ao Supabase — rodar ela
        # direto aqui bloquearia o event loop inteiro (e, com ele, TODAS as
        # requisições de TODO MUNDO) até a consulta voltar, já que isso roda
        # em toda requisição autenticada. run_in_threadpool joga essa
        # chamada bloqueante pra uma thread separada, do mesmo jeito que o
        # FastAPI já faz automaticamente pras rotas declaradas com "def"
        # (não "async def").
        aluno, token_invalido = await run_in_threadpool(_resolver_aluno, request)
        request.state.aluno = aluno

        publico = path in _CAMINHOS_PUBLICOS or any(path.startswith(p) for p in _PREFIXOS_PUBLICOS)

        if publico:
            if aluno and path == "/login":
                return RedirectResponse("/", status_code=303)
            resposta = await call_next(request)
            if token_invalido:
                limpar_cookie_sessao(resposta)
            return resposta

        if aluno is None:
            resposta = RedirectResponse("/login", status_code=303)
            if token_invalido:
                limpar_cookie_sessao(resposta)
            return resposta

        # Ordem obrigatória: troca de senha primeiro, foto de perfil depois
        # (igual a _telas_obrigatorias_pendentes() da app antiga).
        if aluno.get("deve_trocar_senha"):
            if path != _TROCAR_SENHA:
                return RedirectResponse(_TROCAR_SENHA, status_code=303)
        elif aluno.get("deve_definir_foto"):
            if path != _DEFINIR_FOTO:
                return RedirectResponse(_DEFINIR_FOTO, status_code=303)
        elif path in (_TROCAR_SENHA, _DEFINIR_FOTO):
            # Não há pendência nenhuma: não deixa acessar essas telas à toa.
            return RedirectResponse("/", status_code=303)

        return await call_next(request)
