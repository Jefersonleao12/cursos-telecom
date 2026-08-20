"""Admin — Alunos. Porta a aba '🧑‍🎓 Alunos' de modules/admin.py."""
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from database.repositorio import (
    buscar_aluno_por_cpf,
    buscar_aluno_por_email,
    buscar_aluno_por_id,
    criar_aluno_admin,
    definir_acesso_aluno,
    definir_admin_aluno,
    editar_aluno_admin,
    gerar_senha_temporaria,
    listar_cursos,
    listar_todos_alunos,
    progresso_e_conclusao_em_lote,
    todos_tempos_curso,
)
from utils.helpers import FILIAIS, cpf_valido, email_valido, formatar_cpf, somente_digitos
from webapp.deps import exigir_admin
from webapp.integrations.email import enviar_email_admin
from webapp.services.admin_stats import visao_geral
from webapp.templating import templates

router = APIRouter()


def _formatar_duracao(segundos) -> str:
    segundos = int(segundos)
    dias, resto = divmod(segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, _ = divmod(resto, 60)
    if dias > 0:
        return f"{dias}d {horas}h"
    if horas > 0:
        return f"{horas}h {minutos}min"
    return f"{minutos}min"


def _progresso_dos_cursos(aluno_id: str, cursos: list, progresso_aluno: dict, tempos_todos: dict) -> list:
    linhas = []
    for curso in cursos:
        p = progresso_aluno.get(curso["id"], 0.0)
        if p <= 0:
            continue
        texto = f"{curso['titulo']}: {int(p * 100)}%"
        tempos = tempos_todos.get((aluno_id, curso["id"]))
        if tempos and tempos.get("finalizado_em"):
            inicio = datetime.fromisoformat(tempos["iniciado_em"].replace("Z", "+00:00"))
            fim = datetime.fromisoformat(tempos["finalizado_em"].replace("Z", "+00:00"))
            texto += f" · concluído em {_formatar_duracao((fim - inicio).total_seconds())}"
        elif tempos:
            texto += " · em andamento"
        linhas.append(texto)
    return linhas


def _renderizar(request: Request, aluno: dict, q: str = "", editando_id: str = None, enviando_email_id: str = None, **extra):
    alunos = listar_todos_alunos()

    if q:
        termo_digitos = somente_digitos(q)
        termo = q.strip().lower()
        alunos = [
            a for a in alunos
            if termo in a["nome_completo"].lower()
            or termo in a["email"].lower()
            or (termo_digitos and termo_digitos in (a.get("cpf") or ""))
        ]

    cursos = listar_cursos()
    progresso, _concluido = progresso_e_conclusao_em_lote(alunos, cursos)
    tempos_todos = todos_tempos_curso()
    itens = []
    for a in alunos:
        itens.append(
            {
                "aluno": a,
                "cpf_formatado": formatar_cpf(a["cpf"]) if a.get("cpf") else None,
                "progresso": _progresso_dos_cursos(a["id"], cursos, progresso[a["id"]], tempos_todos),
            }
        )

    return templates.TemplateResponse(
        request,
        "admin/alunos.html",
        {
            "aluno": aluno,
            "visao_geral": visao_geral(),
            "itens": itens,
            "termo_busca": q,
            "pedidos_senha": sum(1 for a in alunos if a.get("solicitou_redefinicao_senha")),
            "sem_cpf": sum(1 for a in alunos if not a.get("cpf")),
            "filiais": FILIAIS,
            "editando_id": editando_id,
            "enviando_email_id": enviando_email_id,
            **extra,
        },
    )


@router.get("/admin/alunos")
def alunos(request: Request, q: str = "", editar: str = "", email: str = "", aluno: dict = Depends(exigir_admin)):
    return _renderizar(request, aluno, q=q, editando_id=editar or None, enviando_email_id=email or None)


@router.post("/admin/alunos")
def criar(
    request: Request,
    nome_completo: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(""),
    filial: str = Form(...),
    cargo: str = Form(""),
    aluno: dict = Depends(exigir_admin),
):
    erro = None
    sucesso = None
    if not nome_completo.strip() or not cpf.strip() or not email.strip() or not filial.strip():
        erro = "Preencha todos os campos obrigatórios (*)."
    elif not cpf_valido(cpf):
        erro = "CPF inválido. Confira os números digitados."
    elif not email_valido(email):
        erro = "Digite um e-mail válido."
    elif buscar_aluno_por_cpf(cpf) is not None:
        erro = "Já existe um aluno cadastrado com esse CPF."
    elif buscar_aluno_por_email(email) is not None:
        erro = "Já existe um aluno cadastrado com esse e-mail."
    else:
        criar_aluno_admin(nome_completo, cpf, email, telefone, filial, cargo)
        sucesso = (
            f"Aluno {nome_completo} cadastrado! Login: CPF {formatar_cpf(cpf)} "
            f"· Senha inicial: o próprio CPF (só números)."
        )

    return _renderizar(request, aluno, erro_cadastro=erro, sucesso_cadastro=sucesso)


@router.post("/admin/alunos/{aluno_id}/editar")
def editar(
    request: Request,
    aluno_id: str,
    nome_completo: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(""),
    filial: str = Form(...),
    cargo: str = Form(""),
    resetar_senha: bool = Form(False),
    aluno: dict = Depends(exigir_admin),
):
    erro = None
    if not nome_completo.strip() or not cpf.strip() or not email.strip() or not filial.strip():
        erro = "Preencha todos os campos obrigatórios (*)."
    elif not cpf_valido(cpf):
        erro = "CPF inválido. Confira os números digitados."
    elif not email_valido(email):
        erro = "Digite um e-mail válido."
    else:
        outro_cpf = buscar_aluno_por_cpf(cpf)
        outro_email = buscar_aluno_por_email(email)
        if outro_cpf and outro_cpf["id"] != aluno_id:
            erro = "Já existe outro aluno cadastrado com esse CPF."
        elif outro_email and outro_email["id"] != aluno_id:
            erro = "Já existe outro aluno cadastrado com esse e-mail."

    if erro:
        return _renderizar(request, aluno, editando_id=aluno_id, erro_edicao=erro)

    editar_aluno_admin(
        aluno_id, nome_completo, cpf, email, telefone, filial, cargo,
        resetar_senha_para_cpf=resetar_senha,
    )
    return RedirectResponse("/admin/alunos", status_code=303)


@router.post("/admin/alunos/{aluno_id}/admin")
def alternar_admin(aluno_id: str, tornar: bool = Form(...), aluno: dict = Depends(exigir_admin)):
    definir_admin_aluno(aluno_id, tornar)
    return RedirectResponse("/admin/alunos", status_code=303)


@router.post("/admin/alunos/{aluno_id}/acesso")
def alternar_acesso(aluno_id: str, ativar: bool = Form(...), aluno: dict = Depends(exigir_admin)):
    definir_acesso_aluno(aluno_id, ativar)
    return RedirectResponse("/admin/alunos", status_code=303)


@router.post("/admin/alunos/{aluno_id}/gerar-senha")
def gerar_senha(request: Request, aluno_id: str, aluno: dict = Depends(exigir_admin)):
    senha = gerar_senha_temporaria(aluno_id)
    return _renderizar(request, aluno, senha_gerada_id=aluno_id, senha_gerada_valor=senha)


@router.post("/admin/alunos/{aluno_id}/enviar-email")
def enviar_email(
    request: Request,
    aluno_id: str,
    assunto: str = Form(...),
    mensagem: str = Form(...),
    aluno: dict = Depends(exigir_admin),
):
    destinatario = buscar_aluno_por_id(aluno_id)
    if not destinatario or not assunto.strip() or not mensagem.strip():
        return _renderizar(
            request, aluno, enviando_email_id=aluno_id,
            erro_email="Preencha o assunto e a mensagem antes de enviar.",
        )

    if enviar_email_admin(destinatario, assunto.strip(), mensagem.strip()):
        return _renderizar(request, aluno, email_enviado_id=aluno_id)

    return _renderizar(
        request, aluno, enviando_email_id=aluno_id,
        erro_email="Não consegui enviar o e-mail. Confira se EMAIL_REMETENTE/EMAIL_SENHA_APP estão configurados no servidor.",
    )
