"""
Módulo Repositório.

Centraliza todas as operações de leitura e escrita no banco de dados Supabase.
"""
import os
import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase_client() -> Client:
    """Inicializa e retorna o cliente do Supabase utilizando as Secrets do Streamlit."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# ==========================================
# AUTENTICAÇÃO E USUÁRIOS
# ==========================================

def buscar_aluno_por_email(email: str):
    """Busca um usuário no banco de dados pelo e-mail."""
    sb = get_supabase_client()
    resposta = sb.table("usuarios").select("*").eq("email", email).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_aluno(nome_completo: str, email: str, senha_hash: str, empresa: str = None, cargo: str = None):
    """Cadastra um novo aluno no banco de dados."""
    sb = get_supabase_client()
    dados = {
        "nome_completo": nome_completo,
        "email": email,
        "senha": senha_hash,
        "empresa": empresa,
        "cargo": cargo,
        "is_admin": False
    }
    sb.table("usuarios").insert(dados).execute()


# ==========================================
# CURSOS
# ==========================================

def listar_cursos():
    """Retorna a lista de todos os cursos cadastrados."""
    sb = get_supabase_client()
    resposta = sb.table("cursos").select("*").order("created_at", desc=False).execute()
    return resposta.data


def buscar_curso(curso_id: int):
    """Busca os detalhes de um curso específico pelo ID."""
    sb = get_supabase_client()
    resposta = sb.table("cursos").select("*").eq("id", curso_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_curso(titulo: str, descricao: str, instrutor: str, carga_horaria: int):
    """Cadastra um novo curso."""
    sb = get_supabase_client()
    dados = {
        "titulo": titulo,
        "descricao": descricao,
        "instrutor": instrutor,
        "carga_horaria": carga_horaria,
    }
    sb.table("cursos").insert(dados).execute()


def atualizar_curso(curso_id: int, titulo: str, descricao: str, instrutor: str, carga_horaria: int):
    """Atualiza as informações de um curso existente."""
    sb = get_supabase_client()
    dados = {
        "titulo": titulo,
        "descricao": descricao,
        "instrutor": instrutor,
        "carga_horaria": carga_horaria,
    }
    sb.table("cursos").update(dados).eq("id", curso_id).execute()


def excluir_curso(curso_id: int):
    """Exclui um curso pelo seu ID."""
    sb = get_supabase_client()
    sb.table("cursos").delete().eq("id", curso_id).execute()


# ==========================================
# AULAS
# ==========================================

def listar_aulas_do_curso(curso_id: int):
    """Retorna todas as aulas pertencentes a um curso ordenadas pela ordem."""
    sb = get_supabase_client()
    resposta = (
        sb.table("aulas")
        .select("*")
        .eq("curso_id", curso_id)
        .order("ordem", desc=False)
        .execute()
    )
    return resposta.data


def buscar_aula(aula_id: int):
    """Busca os detalhes de uma aula específica pelo ID."""
    sb = get_supabase_client()
    resposta = sb.table("aulas").select("*").eq("id", aula_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_aula(curso_id: int, titulo: str, url_video: str, ordem: int, duracao_minutos: int):
    """Cadastra uma nova aula em um curso."""
    sb = get_supabase_client()
    dados = {
        "curso_id": curso_id,
        "titulo": titulo,
        "url_video": url_video,
        "ordem": ordem,
        "duracao_minutos": duracao_minutos,
    }
    sb.table("aulas").insert(dados).execute()


# ==========================================
# PROGRESSO
# ==========================================

def marcar_aula_concluida(aluno_id: str, aula_id: int):
    """Registra a conclusão de uma aula por parte do aluno."""
    sb = get_supabase_client()
    dados = {"aluno_id": aluno_id, "aula_id": aula_id}
    sb.table("progresso_aulas").upsert(dados, on_conflict="aluno_id,aula_id").execute()


def listar_aulas_concluidas_pelo_aluno(aluno_id: str):
    """Retorna os IDs das aulas concluídas pelo aluno."""
    sb = get_supabase_client()
    resposta = (
        sb.table("progresso_aulas")
        .select("aula_id")
        .eq("aluno_id", aluno_id)
        .execute()
    )
    return [item["aula_id"] for item in resposta.data]


def calcular_progresso_curso(aluno_id: str, curso_id: int) -> float:
    """Calcula o percentual (0.0 a 1.0) de conclusão do curso pelo aluno."""
    aulas = listar_aulas_do_curso(curso_id)
    if not aulas:
        return 0.0

    aulas_concluidas = set(listar_aulas_concluidas_pelo_aluno(aluno_id))
    total_aulas = len(aulas)
    concluidas = sum(1 for a in aulas if a["id"] in aulas_concluidas)

    return concluidas / total_aulas


# ==========================================
# PROVAS E PERGUNTAS
# ==========================================

def buscar_prova_do_curso(curso_id: int):
    """Busca a avaliação atrelada a um curso."""
    sb = get_supabase_client()
    resposta = sb.table("provas").select("*").eq("curso_id", curso_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_prova(curso_id: int, titulo: str, nota_minima: float):
    """Cadastra uma nova avaliação para o curso."""
    sb = get_supabase_client()
    dados = {"curso_id": curso_id, "titulo": titulo, "nota_minima": nota_minima}
    sb.table("provas").insert(dados).execute()


def listar_perguntas(prova_id: int):
    """Retorna as perguntas de uma avaliação."""
    sb = get_supabase_client()
    resposta = (
        sb.table("perguntas")
        .select("*")
        .eq("prova_id", prova_id)
        .order("ordem", desc=False)
        .execute()
    )
    return resposta.data


def criar_pergunta(
    prova_id: int,
    enunciado: str,
    opcao_a: str,
    opcao_b: str,
    opcao_c: str,
    opcao_d: str,
    resposta_correta: str,
    ordem: int,
):
    """Cadastra uma pergunta para uma avaliação."""
    sb = get_supabase_client()
    dados = {
        "prova_id": prova_id,
        "enunciado": enunciado,
        "opcao_a": opcao_a,
        "opcao_b": opcao_b,
        "opcao_c": opcao_c,
        "opcao_d": opcao_d,
        "resposta_correta": resposta_correta,
        "ordem": ordem,
    }
    sb.table("perguntas").insert(dados).execute()


def salvar_resultado_prova(aluno_id: str, prova_id: int, nota: float, aprovado: bool):
    """Grava o resultado da tentativa de avaliação."""
    sb = get_supabase_client()
    dados = {
        "aluno_id": aluno_id,
        "prova_id": prova_id,
        "nota": nota,
        "aprovado": aprovado,
    }
    sb.table("resultados_provas").insert(dados).execute()


def buscar_ultimo_resultado(aluno_id: str, prova_id: int):
    """Retorna a tentativa mais recente feita pelo aluno nesta prova."""
    sb = get_supabase_client()
    resposta = (
        sb.table("resultados_provas")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("prova_id", prova_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def reabrir_prova_aluno(aluno_id: str, prova_id: int):
    """Remove os registros de resultado da prova para permitir uma nova tentativa."""
    sb = get_supabase_client()
    sb.table("resultados_provas").delete().eq("aluno_id", aluno_id).eq("prova_id", prova_id).execute()


# ==========================================
# ALUNOS E FILIAIS
# ==========================================

def listar_todos_alunos():
    """Retorna a lista de todos os alunos cadastrados."""
    sb = get_supabase_client()
    resposta = sb.table("usuarios").select("*").eq("is_admin", False).execute()
    return resposta.data


def contar_alunos_por_filial():
    """Retorna um dicionário agrupando alunos por filial."""
    alunos = listar_todos_alunos()
    grupos = {}
    for aluno in alunos:
        filial = aluno.get("empresa") or "Sem Filial Defina"
        if filial not in grupos:
            grupos[filial] = []
        grupos[filial].append(aluno)
    return grupos


# ==========================================
# MATERIAIS
# ==========================================

def listar_materiais():
    """Lista todos os materiais cadastrados."""
    sb = get_supabase_client()
    resposta = sb.table("materiais").select("*").order("created_at", desc=True).execute()
    return resposta.data


def listar_categorias_materiais():
    """Lista todas as categorias distintas de materiais."""
    materiais = listar_materiais()
    categorias = sorted(list({m["categoria"] for m in materiais if m.get("categoria")}))
    return categorias


def enviar_material(titulo: str, descricao: str, categoria: str, bytes_arquivo: bytes, nome_arquivo: str):
    """Faz upload do arquivo para o Bucket do Supabase e registra na tabela materiais."""
    sb = get_supabase_client()
    caminho_storage = f"materiais/{nome_arquivo}"

    sb.storage.from_("materiais").upload(
        path=caminho_storage,
        file=bytes_arquivo,
        file_options={"upsert": "true"},
    )

    dados = {
        "titulo": titulo,
        "descricao": descricao,
        "categoria": categoria,
        "caminho_storage": caminho_storage,
        "nome_arquivo": nome_arquivo,
    }
    sb.table("materiais").insert(dados).execute()


def excluir_material(material_id: int, caminho_storage: str):
    """Exclui o arquivo do Storage e apaga o registro do banco."""
    sb = get_supabase_client()
    try:
        sb.storage.from_("materiais").remove([caminho_storage])
    except Exception:
        pass
    sb.table("materiais").delete().eq("id", material_id).execute()


# ==========================================
# DÚVIDAS
# ==========================================

def listar_duvidas(apenas_nao_respondidas: bool = False):
    """Lista dúvidas enviadas pelos alunos."""
    sb = get_supabase_client()
    query = sb.table("duvidas").select("*").order("criado_em", desc=True)
    if apenas_nao_respondidas:
        query = query.eq("respondida", False)
    resposta = query.execute()
    return resposta.data


def marcar_duvida_respondida(duvida_id: int):
    """Marca uma dúvida como respondida."""
    sb = get_supabase_client()
    sb.table("duvidas").update({"respondida": True}).eq("id", duvida_id).execute()
