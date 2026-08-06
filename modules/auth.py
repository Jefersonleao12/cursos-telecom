"""
Módulo de Autenticação: cadastro e login de alunos.

A senha NUNCA é salva em texto puro — usamos bcrypt para gerar um hash
seguro e irreversível, que é o que fica armazenado no banco de dados.

Sessão persistente (sobrevive a F5)
------------------------------------
Por padrão, o `st.session_state` do Streamlit vive apenas enquanto a conexão
do navegador com o servidor estiver ativa: um recarregamento de página (F5)
cria uma sessão nova e o aluno cai de volta na tela de login, mesmo tendo
acabado de entrar.

Para resolver isso, ao logar guardamos um "token de sessão" assinado
(aluno_id + validade + assinatura HMAC) como parâmetro na URL
(`st.query_params`). Como a URL não muda num F5, ao recarregar a página o
app consegue ler esse token, validar a assinatura e restaurar a sessão do
aluno automaticamente — sem precisar guardar nada extra no banco.
"""
import hmac
import hashlib
import time
from pathlib import Path

import streamlit as st
import bcrypt

from database.repositorio import criar_aluno, buscar_aluno_por_email, buscar_aluno_por_id
from utils.helpers import email_valido, FILIAIS

# Caminho da logo: assets/logo.png, na raiz do projeto (um nível acima de modules/)
_CAMINHO_LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo.png"

# Sessão fica válida por 30 dias (o token é renovado a cada novo login).
_DURACAO_SESSAO_SEGUNDOS = 30 * 24 * 60 * 60
_PARAM_SESSAO = "sessao"


# ---------------------------------------------------------------------------
# Senhas
# ---------------------------------------------------------------------------

def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha digitada em um hash seguro (irreversível)."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha_digitada: str, senha_hash_salva: str) -> bool:
    """Confere se a senha digitada corresponde ao hash salvo no banco."""
    return bcrypt.checkpw(senha_digitada.encode("utf-8"), senha_hash_salva.encode("utf-8"))


# ---------------------------------------------------------------------------
# Token de sessão (mantém o aluno logado mesmo depois de um F5)
# ---------------------------------------------------------------------------

def _chave_secreta() -> bytes:
    """
    Chave usada para assinar o token de sessão. Reaproveita a chave de
    serviço do Supabase (já configurada em secrets.toml) para não exigir
    nenhuma configuração extra do usuário.
    """
    chave = st.secrets.get("SUPABASE_SERVICE_KEY", "chave-padrao-troque-em-producao")
    return f"cursos-telecom::token-sessao::{chave}".encode("utf-8")


def _gerar_token_sessao(aluno_id: str) -> str:
    validade = int(time.time()) + _DURACAO_SESSAO_SEGUNDOS
    mensagem = f"{aluno_id}.{validade}"
    assinatura = hmac.new(_chave_secreta(), mensagem.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{mensagem}.{assinatura}"


def _validar_token_sessao(token: str):
    """Retorna o aluno_id se o token for válido e ainda não tiver expirado, senão None."""
    try:
        aluno_id, validade_str, assinatura = token.split(".")
        validade = int(validade_str)
    except (ValueError, AttributeError):
        return None

    mensagem = f"{aluno_id}.{validade_str}"
    assinatura_esperada = hmac.new(_chave_secreta(), mensagem.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(assinatura, assinatura_esperada):
        return None  # token adulterado ou assinado com outra chave
    if validade < int(time.time()):
        return None  # expirado

    return aluno_id


def _login_efetuado(aluno: dict, lembrar: bool = True):
    """Guarda os dados do aluno logado na sessão do navegador (st.session_state)."""
    st.session_state["aluno_logado"] = True
    st.session_state["aluno_id"] = aluno["id"]
    st.session_state["aluno_nome"] = aluno["nome_completo"]
    st.session_state["aluno_email"] = aluno["email"]
    st.session_state["aluno_empresa"] = aluno.get("empresa") or ""
    st.session_state["aluno_filial"] = aluno.get("filial") or ""
    st.session_state["aluno_is_admin"] = aluno.get("is_admin", False)

    if lembrar:
        # Grava o token na URL para sobreviver a um F5 (ver docstring do módulo).
        st.query_params[_PARAM_SESSAO] = _gerar_token_sessao(aluno["id"])


def fazer_logout():
    """Remove todos os dados da sessão, apaga o token da URL e volta para o login."""
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.query_params.clear()
    st.rerun()


def _restaurar_sessao_da_url() -> bool:
    """
    Tenta restaurar a sessão a partir do token salvo em st.query_params
    (ou seja, sobrevivente a um recarregamento de página). Retorna True se
    conseguiu logar o aluno automaticamente.
    """
    token = st.query_params.get(_PARAM_SESSAO)
    if not token:
        return False

    aluno_id = _validar_token_sessao(token)
    if not aluno_id:
        st.query_params.clear()  # token inválido/expirado: limpa pra não tentar de novo
        return False

    aluno = buscar_aluno_por_id(aluno_id)
    if not aluno:
        st.query_params.clear()  # conta pode ter sido excluída
        return False

    _login_efetuado(aluno, lembrar=False)  # o token já está na URL, não precisa regravar
    return True


# ---------------------------------------------------------------------------
# Visual das telas de login / cadastro
# ---------------------------------------------------------------------------

def _estilos_auth():
    st.markdown(
        """
        <style>
        .auth-hero {
            background: linear-gradient(150deg, #0F2E56 0%, #143C6E 55%, #1F5AA8 100%);
            border-radius: 20px;
            padding: 2.6rem 2.2rem;
            color: #FFFFFF;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        /* No desktop, o painel azul (hero) e o card de login/cadastro ficam
           lado a lado. O card (menor) sobrava um espaço em branco embaixo
           porque cada um só ocupa a altura do seu próprio conteúdo. Em vez
           de depender de "esticar" as colunas do Streamlit (frágil, pois
           existem várias divs internas entre a coluna e o conteúdo), damos
           uma altura mínima igual para os dois e centralizamos o conteúdo
           do card dentro dela — assim as bordas ficam alinhadas. */
        @media (min-width: 768px) {
            .auth-hero {
                min-height: 620px;
            }
            div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stForm"]) {
                min-height: 620px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
        }
        .auth-hero h1 {
            font-size: 1.55rem;
            line-height: 1.35;
            margin: 0 0 .6rem 0;
            font-weight: 700;
        }
        .auth-hero p.auth-sub {
            opacity: .88;
            font-size: .96rem;
            margin-bottom: 1.6rem;
        }
        .auth-feature {
            display: flex;
            align-items: center;
            gap: .65rem;
            margin: .5rem 0;
            font-size: .92rem;
            opacity: .95;
        }
        .auth-feature span.ico {
            font-size: 1.1rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stForm"]) {
            border-radius: 18px !important;
        }
        .auth-card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #143C6E;
            margin-bottom: .2rem;
        }
        .auth-card-sub {
            color: #6B7A8F;
            font-size: .9rem;
            margin-bottom: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _painel_hero():
    st.markdown(
        """
        <div class="auth-hero">
            <h1>Bem-vindo à Plataforma de<br>Treinamentos em Telecomunicações</h1>
            <p class="auth-sub">
                Cursos, avaliações e certificados da equipe, tudo em um só lugar —
                de qualquer filial, no computador ou no celular.
            </p>
            <div class="auth-feature"><span class="ico">📚</span> Cursos e aulas em vídeo</div>
            <div class="auth-feature"><span class="ico">📝</span> Avaliações com certificado</div>
            <div class="auth-feature"><span class="ico">🗂️</span> Materiais para consulta</div>
            <div class="auth-feature"><span class="ico">🏆</span> Acompanhamento do seu progresso</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _seletor_login_cadastro():
    """Alterna entre login/cadastro com dois botões estilo 'abas'."""
    pagina_atual = st.session_state.get("pagina_auth", "login")
    col_login, col_cadastro = st.columns(2)
    with col_login:
        if st.button(
            "Entrar", use_container_width=True,
            type="primary" if pagina_atual == "login" else "secondary",
        ):
            st.session_state["pagina_auth"] = "login"
            st.rerun()
    with col_cadastro:
        if st.button(
            "Criar cadastro", use_container_width=True,
            type="primary" if pagina_atual == "cadastro" else "secondary",
        ):
            st.session_state["pagina_auth"] = "cadastro"
            st.rerun()
    st.write("")


def tela_login():
    st.markdown('<div class="auth-card-title">🔐 Entrar na plataforma</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-card-sub">Use o e-mail e a senha do seu cadastro.</div>', unsafe_allow_html=True)

    with st.form("form_login", clear_on_submit=False):
        email = st.text_input("📧 E-mail", placeholder="voce@empresa.com")
        senha = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
        entrar = st.form_submit_button("Entrar", width="stretch", type="primary")

    if entrar:
        if not email or not senha:
            st.warning("Preencha e-mail e senha.")
            return

        aluno = buscar_aluno_por_email(email)
        if aluno is None:
            st.error("E-mail não encontrado. Verifique ou cadastre-se acima.")
            return

        if verificar_senha(senha, aluno["senha_hash"]):
            _login_efetuado(aluno)
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")


def tela_cadastro():
    st.markdown('<div class="auth-card-title">📝 Criar cadastro de aluno</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-card-sub">Leva menos de um minuto.</div>', unsafe_allow_html=True)

    with st.form("form_cadastro", clear_on_submit=False):
        nome = st.text_input("Nome completo *")
        email = st.text_input("E-mail *")
        col_empresa, col_cargo = st.columns(2)
        with col_empresa:
            empresa = st.text_input("Empresa")
        with col_cargo:
            cargo = st.text_input("Cargo / Função")
        filial = st.selectbox(
            "Filial (cidade) *",
            options=[""] + FILIAIS,
            format_func=lambda v: "Selecione..." if v == "" else v,
        )
        col_senha, col_confirmar = st.columns(2)
        with col_senha:
            senha = st.text_input("Senha *", type="password", help="Mínimo de 6 caracteres.")
        with col_confirmar:
            confirmar_senha = st.text_input("Confirmar senha *", type="password")
        cadastrar = st.form_submit_button("Cadastrar", width="stretch", type="primary")

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
            st.error("Já existe um cadastro com este e-mail. Faça login acima.")
            return

        senha_hash = gerar_hash_senha(senha)
        novo_aluno = criar_aluno(nome, email, senha_hash, empresa, cargo, filial)
        st.success("Cadastro realizado com sucesso!")
        _login_efetuado(novo_aluno)
        st.rerun()


def exigir_login():
    """
    Função 'porteira': se o usuário não estiver logado, tenta primeiro
    restaurar a sessão a partir do token na URL (sobrevive a F5); se não
    conseguir, mostra as telas de login/cadastro e interrompe a execução
