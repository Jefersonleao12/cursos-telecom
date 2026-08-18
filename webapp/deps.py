"""
Dependências do FastAPI para as rotas protegidas. O AutenticacaoMiddleware
já bloqueia quem não está logado antes de qualquer rota rodar — essas
dependências só expõem o aluno (já resolvido em request.state.aluno) com
tipagem, e barram quem não é admin nas rotas /admin.
"""
from fastapi import HTTPException, Request, status


def obter_aluno_atual(request: Request) -> dict:
    aluno = getattr(request.state, "aluno", None)
    if aluno is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return aluno


def exigir_admin(request: Request) -> dict:
    aluno = obter_aluno_atual(request)
    if not aluno.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return aluno
