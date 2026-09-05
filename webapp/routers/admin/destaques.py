"""Admin — Destaques (carrossel de fotos da Início). Porta a aba
'🌟 Destaques' de modules/admin.py."""
from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool

from database.repositorio import (
    ImagemInvalidaError,
    criar_destaque,
    editar_destaque,
    excluir_destaque,
    listar_todos_destaques,
)
from webapp.deps import exigir_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


def _renderizar(request: Request, aluno: dict, editando_id: int = None, excluindo_id: int = None, **extra):
    return templates.TemplateResponse(
        request,
        "admin/destaques.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "destaques": listar_todos_destaques(),
            "editando_id": editando_id,
            "excluindo_id": excluindo_id,
            **extra,
        },
    )


@router.get("/admin/destaques")
def destaques(request: Request, editar: int = 0, excluir: int = 0, aluno: dict = Depends(exigir_admin)):
    return _renderizar(request, aluno, editando_id=editar or None, excluindo_id=excluir or None)


@router.post("/admin/destaques")
async def criar(
    request: Request,
    # Form("") e não Form(...): assim um título vazio chega até aqui e o admin
    # vê a mensagem explicando o que faltou, em vez de uma tela de erro crua
    # do FastAPI (que é o que acontece quando o campo é declarado obrigatório).
    titulo: str = Form(""),
    descricao: str = Form(""),
    ordem: int = Form(1),
    foto: UploadFile = None,
    aluno: dict = Depends(exigir_admin),
):
    conteudo = await foto.read() if foto else b""
    if not titulo.strip() or not conteudo:
        return _renderizar(request, aluno, erro_cadastro="Preencha o título e escolha uma foto.")
    try:
        # Processa a imagem (Pillow) e envia pro Storage numa thread
        # separada, pra não travar o event loop de todo mundo.
        await run_in_threadpool(criar_destaque, titulo, descricao, conteudo, ordem)
    except ImagemInvalidaError as erro:
        return _renderizar(request, aluno, erro_cadastro=str(erro))
    return RedirectResponse("/admin/destaques", status_code=303)


@router.post("/admin/destaques/{destaque_id}/editar")
async def editar(
    request: Request,
    destaque_id: int,
    titulo: str = Form(...),
    descricao: str = Form(""),
    ordem: int = Form(1),
    ativo: bool = Form(False),
    caminho_storage_atual: str = Form(...),
    foto: UploadFile = None,
    aluno: dict = Depends(exigir_admin),
):
    if not titulo.strip():
        return _renderizar(request, aluno, editando_id=destaque_id, erro_edicao="Informe o título.")

    conteudo = await foto.read() if foto else None
    try:
        # Processa a imagem (Pillow) e envia pro Storage numa thread
        # separada, pra não travar o event loop de todo mundo.
        await run_in_threadpool(
            editar_destaque, destaque_id, titulo, descricao, ordem, ativo, caminho_storage_atual, conteudo or None
        )
    except ImagemInvalidaError as erro:
        return _renderizar(request, aluno, editando_id=destaque_id, erro_edicao=str(erro))
    return RedirectResponse("/admin/destaques", status_code=303)


@router.post("/admin/destaques/{destaque_id}/excluir")
def excluir(destaque_id: int, caminho_storage: str = Form(...), aluno: dict = Depends(exigir_admin)):
    excluir_destaque(destaque_id, caminho_storage)
    return RedirectResponse("/admin/destaques", status_code=303)
