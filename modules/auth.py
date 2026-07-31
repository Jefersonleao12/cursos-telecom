"""
Módulo de Autenticação: cadastro e login de alunos.

A senha NUNCA é salva em texto puro — usamos bcrypt para gerar um hash
seguro e irreversível, que é o que fica armazenado no banco de dados.
"""
import streamlit as st
import bcrypt

from database.repositorio import criar_aluno, buscar_aluno_por_email
from utils.helpers import email_valido, FILIAIS


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha digitada em um hash seguro (irreversível)."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha_digitada: str, senha_hash_salva: str) -> bool:
    """Confere se a senha digitada corresponde ao hash salvo no banco."""
    return bcrypt.checkpw(senha_digitada.encode("utf-8"), senha_hash_salva.encode("utf-8"))


def _login_efetuado(aluno: dict):
    """Guarda os dados do aluno logado na sessão do navegador (st.session_state)."""
    st.session_state["aluno_logado"] = True
    st.session_state["aluno_id"] = aluno["id"]
    st.session_state["aluno_nome"] = aluno["nome_completo"]
    st.session_state["aluno_email"] = aluno["email"]
    st.session_state["aluno_empresa"] = aluno.get("empresa") or ""
    st.session_state["aluno_filial"] = aluno.get("filial") or ""
    st.session_state["aluno_is_admin"] = aluno.get("is_admin", False)


def fazer_logout():
    """Remove todos os dados da sessão e volta para a tela de login."""
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()


def tela_login():
    st.subheader("🔐 Entrar na Plataforma")

    with st.form("form_login", clear_on_submit=False):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar", use_container_width=True, type="primary")

    if entrar:
        if not email or not senha:
            st.warning("Preencha e-mail e senha.")
            return

        aluno = buscar_aluno_por_email(email)
        if aluno is None:
            st.error("E-mail não encontrado. Verifique ou cadastre-se abaixo.")
            return

        if verificar_senha(senha, aluno["senha_hash"]):
            _login_efetuado(aluno)
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")

    st.divider()
    st.caption("Ainda não tem uma conta?")
    if st.button("Criar cadastro", use_container_width=True):
        st.session_state["pagina_auth"] = "cadastro"
        st.rerun()


def tela_cadastro():
    st.subheader("📝 Criar Cadastro de Aluno")

    with st.form("form_cadastro", clear_on_submit=False):
        nome = st.text_input("Nome completo *")
        email = st.text_input("E-mail *")
        empresa = st.text_input("Empresa")
        cargo = st.text_input("Cargo / Função")
        filial = st.selectbox("Filial (cidade) *", options=[""] + FILIAIS, format_func=lambda v: "Selecione..." if v == "" else v)
        senha = st.text_input("Senha *", type="password")
        confirmar_senha = st.text_input("Confirmar senha *", type="password")
        cadastrar = st.form_submit_button("Cadastrar", use_container_width=True, type="primary")

    if cadastrar:
        if not nome or not email or not senha:
            st.warning("Preencha todos os campos obrigatórios (*).")
            return
        if not filial:
            st.warning("Selecione sua filial (cidade).")
            return
        if not email_valido(email):
            st.warning("Digite um e-mail válido.")
            return
        if len(senha) < 6:
            st.warning("A senha deve ter pelo menos 6 caracteres.")
            return
        if senha != confirmar_senha:
            st.warning("As senhas não coincidem.")
            return
        if buscar_aluno_por_email(email) is not None:
            st.error("Já existe um cadastro com este e-mail. Faça login.")
            return

        senha_hash = gerar_hash_senha(senha)
        novo_aluno = criar_aluno(nome, email, senha_hash, empresa, cargo, filial)
        st.success("Cadastro realizado com sucesso!")
        _login_efetuado(novo_aluno)
        st.rerun()

    st.divider()
    st.caption("Já tem uma conta?")
    if st.button("Voltar para login", use_container_width=True):
        st.session_state["pagina_auth"] = "login"
        st.rerun()


def exigir_login():
    """
    Função 'porteira': se o usuário não estiver logado, mostra as telas
    de login/cadastro e interrompe a execução do restante do app (st.stop()).
    Chame esta função no início do app.py, antes de montar o resto da interface.
    """
    if st.session_state.get("aluno_logado"):
        return  # já está logado, o app.py segue o fluxo normal

    # As colunas laterais (vazias) empurram o conteúdo para o centro em telas
    # largas (PC). Em telas estreitas (celular), o Streamlit empilha as
    # colunas automaticamente, então a coluna do meio ocupa 100% da largura.
    _esq, centro, _dir = st.columns([1, 2, 1])
    with centro:
        st.markdown(
            "<h2 style='text-align:center; margin-bottom:0.2rem;'>"
            "📡 Plataforma de Treinamentos em Telecomunicações</h2>",
            unsafe_allow_html=True,
        )
        if st.session_state.get("pagina_auth") == "cadastro":
            tela_cadastro()
        else:
            tela_login()

    st.stop()
