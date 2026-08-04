"""
Camada de acesso a dados (Repositório).

Concentra TODAS as consultas ao Supabase em um único lugar. Isso facilita a
manutenção: se um dia você quiser trocar de banco de dados ou entender como
alguma tela busca suas informações, é só olhar aqui.
"""
import uuid
from datetime import datetime, timezone

from database.supabase_client import get_supabase_client


# ---------------------------------------------------------------------------
# ALUNOS
# ---------------------------------------------------------------------------

def buscar_aluno_por_email(email: str):
    """Retorna o registro do aluno pelo e-mail, ou None se não existir."""
    sb = get_supabase_client()
    resposta = sb.table("alunos").select("*").eq("email", email.lower().strip()).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_aluno(nome_completo: str, email: str, senha_hash: str, empresa: str, cargo: str, filial: str = None):
    """Cria um novo aluno no banco. Retorna o registro criado (já com o id gerado)."""
    sb = get_supabase_client()
    novo = {
        "nome_completo": nome_completo.strip(),
        "email": email.lower().strip(),
        "senha_hash": senha_hash,
        "empresa": empresa.strip() if empresa else None,
        "cargo": cargo.strip() if cargo else None,
        "filial": filial.strip() if filial else None,
        "is_admin": False,
    }
    resposta = sb.table("alunos").insert(novo).execute()
    return resposta.data[0]


def listar_todos_alunos():
    """Usado no painel administrativo para listar todos os alunos cadastrados."""
    sb = get_supabase_client()
    resposta = sb.table("alunos").select("*").order("criado_em", desc=True).execute()
    return resposta.data


def contar_alunos_por_filial():
    """
    Usado no painel administrativo: retorna um dicionário
    {"Nome da Filial": [lista de alunos daquela filial]}, ordenado por
    quantidade de alunos (da filial com mais alunos para a com menos).
    Alunos sem filial definida (cadastros antigos) entram em "Sem filial".
    """
    alunos = listar_todos_alunos()
    grupos: dict = {}
    for aluno in alunos:
        nome_filial = aluno.get("filial") or "Sem filial"
        grupos.setdefault(nome_filial, []).append(aluno)
    # Ordena as filiais da com mais alunos para a com menos
    return dict(sorted(grupos.items(), key=lambda item: len(item[1]), reverse=True))


# ---------------------------------------------------------------------------
# CURSOS
# ---------------------------------------------------------------------------

def listar_cursos():
    sb = get_supabase_client()
    resposta = sb.table("cursos").select("*").order("criado_em", desc=True).execute()
    return resposta.data


def buscar_curso(curso_id: int):
    sb = get_supabase_client()
    resposta = sb.table("cursos").select("*").eq("id", curso_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_curso(titulo: str, descricao: str, instrutor: str, carga_horaria: int):
    sb = get_supabase_client()
    novo = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "instrutor": instrutor.strip(),
        "carga_horaria": carga_horaria,
    }
    resposta = sb.table("cursos").insert(novo).execute()
    return resposta.data[0]


# ---------------------------------------------------------------------------
# AULAS
# ---------------------------------------------------------------------------

def listar_aulas_do_curso(curso_id: int):
    sb = get_supabase_client()
    resposta = (
        sb.table("aulas")
        .select("*")
        .eq("curso_id", curso_id)
        .order("ordem")
        .execute()
    )
    return resposta.data


def criar_aula(curso_id: int, titulo: str, url_video: str, ordem: int, duracao_minutos: int):
    sb = get_supabase_client()
    nova = {
        "curso_id": curso_id,
        "titulo": titulo.strip(),
        "url_video": url_video.strip(),
        "ordem": ordem,
        "duracao_minutos": duracao_minutos,
    }
    resposta = sb.table("aulas").insert(nova).execute()
    return resposta.data[0]


# ---------------------------------------------------------------------------
# PROGRESSO DE AULAS
# ---------------------------------------------------------------------------

def marcar_aula_concluida(aluno_id: str, aula_id: int):
    """Marca (ou atualiza) uma aula como concluída para o aluno."""
    sb = get_supabase_client()
    registro = {
        "aluno_id": aluno_id,
        "aula_id": aula_id,
        "concluida": True,
        "concluida_em": datetime.now(timezone.utc).isoformat(),
    }
    sb.table("progresso_aulas").upsert(registro, on_conflict="aluno_id,aula_id").execute()


def aulas_concluidas_do_aluno(aluno_id: str, curso_id: int):
    """Retorna a lista de IDs de aulas já concluídas pelo aluno, dentro de um curso."""
    sb = get_supabase_client()
    aulas_do_curso = listar_aulas_do_curso(curso_id)
    ids_aulas = [a["id"] for a in aulas_do_curso]
    if not ids_aulas:
        return []
    resposta = (
        sb.table("progresso_aulas")
        .select("aula_id")
        .eq("aluno_id", aluno_id)
        .eq("concluida", True)
        .in_("aula_id", ids_aulas)
        .execute()
    )
    return [linha["aula_id"] for linha in resposta.data]


def calcular_progresso_curso(aluno_id: str, curso_id: int) -> float:
    """Retorna o percentual (0.0 a 1.0) de aulas concluídas em um curso."""
    aulas = listar_aulas_do_curso(curso_id)
    if not aulas:
        return 0.0
    concluidas = aulas_concluidas_do_aluno(aluno_id, curso_id)
    return len(concluidas) / len(aulas)


# ---------------------------------------------------------------------------
# PROVAS E PERGUNTAS
# ---------------------------------------------------------------------------

def buscar_prova_do_curso(curso_id: int):
    sb = get_supabase_client()
    resposta = sb.table("provas").select("*").eq("curso_id", curso_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_prova(curso_id: int, titulo: str, nota_minima: float):
    sb = get_supabase_client()
    nova = {"curso_id": curso_id, "titulo": titulo.strip(), "nota_minima": nota_minima}
    resposta = sb.table("provas").insert(nova).execute()
    return resposta.data[0]


def listar_perguntas(prova_id: int):
    sb = get_supabase_client()
    resposta = (
        sb.table("perguntas")
        .select("*")
        .eq("prova_id", prova_id)
        .order("ordem")
        .execute()
    )
    return resposta.data


def criar_pergunta(prova_id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta, ordem):
    sb = get_supabase_client()
    nova = {
        "prova_id": prova_id,
        "enunciado": enunciado.strip(),
        "opcao_a": opcao_a.strip(),
        "opcao_b": opcao_b.strip(),
        "opcao_c": opcao_c.strip(),
        "opcao_d": opcao_d.strip(),
        "resposta_correta": resposta_correta.upper().strip(),
        "ordem": ordem,
    }
    resposta = sb.table("perguntas").insert(nova).execute()
    return resposta.data[0]


# ---------------------------------------------------------------------------
# RESULTADOS DE PROVAS
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# RESULTADOS DE PROVAS
# ---------------------------------------------------------------------------

def salvar_resultado_prova(aluno_id: str, prova_id: int, nota: float, aprovado: bool):
    sb = get_supabase_client()
    registro = {
        "aluno_id": aluno_id,
        "prova_id": prova_id,
        "nota": nota,
        "aprovado": aprovado,
    }
    resposta = sb.table("resultados_provas").insert(registro).execute()
    return resposta.data[0]


def melhor_resultado(aluno_id: str, prova_id: int):
    """Retorna o melhor resultado (maior nota) que o aluno já obteve nesta prova."""
    sb = get_supabase_client()
    resposta = (
        sb.table("resultados_provas")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("prova_id", prova_id)
        .order("nota", desc=True)
        .limit(1)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def buscar_ultimo_resultado(aluno_id: str, prova_id: int):
    """
    Retorna a tentativa mais recente feita pelo aluno nesta prova,
    independentemente de ele ter sido aprovado ou reprovado.
    Usado para travar o formulário no 'provas.py'.
    """
    sb = get_supabase_client()
    resposta = (
        sb.table("resultados_provas")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("prova_id", prova_id)
        .order("id", desc=True)
        .limit(1)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def reabrir_prova_aluno(aluno_id: str, prova_id: int):
    """
    Remove todos os registros de resultado da prova para o aluno.
    Usado pelo painel do Administrador após análise para liberar um novo envio.
    """
    sb = get_supabase_client()
    sb.table("resultados_provas") \
        .delete() \
        .eq("aluno_id", aluno_id) \
        .eq("prova_id", prova_id) \
        .execute()


# ---------------------------------------------------------------------------
# CERTIFICADOS
# ---------------------------------------------------------------------------

def buscar_certificado(aluno_id: str, curso_id: int):
    sb = get_supabase_client()
    resposta = (
        sb.table("certificados")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("curso_id", curso_id)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def emitir_certificado(aluno_id: str, curso_id: int, codigo_verificacao: str):
    sb = get_supabase_client()
    registro = {
        "aluno_id": aluno_id,
        "curso_id": curso_id,
        "codigo_verificacao": codigo_verificacao,
    }
    resposta = sb.table("certificados").insert(registro).execute()
    return resposta.data[0]


# ---------------------------------------------------------------------------
# MATERIAIS (fotos, documentos e arquivos para download pelos alunos)
# ---------------------------------------------------------------------------

# Nome do "bucket" (pasta) no Supabase Storage onde os arquivos ficam guardados.
# Precisa ser criado uma vez no painel do Supabase (Storage -> New bucket),
# marcado como "Public bucket" para que os links de download funcionem.
_BUCKET_MATERIAIS = "materiais"


def enviar_material(titulo: str, descricao: str, categoria: str, arquivo_bytes: bytes, nome_arquivo: str):
    """
    Sobe o arquivo para o Supabase Storage e grava o registro (título, categoria,
    descrição etc.) na tabela 'materiais'. Retorna o registro criado.
    """
    sb = get_supabase_client()

    extensao = nome_arquivo.rsplit(".", 1)[-1].lower() if "." in nome_arquivo else ""
    # Prefixamos com um código único para nunca haver conflito de nomes no Storage,
    # mesmo que dois arquivos diferentes se chamem igual (ex: "manual.pdf").
    caminho_storage = f"{uuid.uuid4().hex}_{nome_arquivo}"

    sb.storage.from_(_BUCKET_MATERIAIS).upload(
        caminho_storage,
        arquivo_bytes,
        file_options={"content-type": "application/octet-stream"},
    )

    novo = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "categoria": categoria.strip(),
        "nome_arquivo": nome_arquivo,
        "caminho_storage": caminho_storage,
        "tipo_arquivo": extensao,
        "tamanho_bytes": len(arquivo_bytes),
    }
    resposta = sb.table("materiais").insert(novo).execute()
    return resposta.data[0]


def listar_materiais():
    """Lista todos os materiais, do mais recente para o mais antigo."""
    sb = get_supabase_client()
    resposta = sb.table("materiais").select("*").order("criado_em", desc=True).execute()
    return resposta.data


def listar_categorias_materiais():
    """Lista as categorias já usadas (sem repetir), em ordem alfabética."""
    materiais = listar_materiais()
    categorias = sorted({m["categoria"] for m in materiais if m.get("categoria")})
    return categorias


def url_publica_material(caminho_storage: str) -> str:
    """Devolve o link direto de download do arquivo no Supabase Storage."""
    sb = get_supabase_client()
    return sb.storage.from_(_BUCKET_MATERIAIS).get_public_url(caminho_storage)


def excluir_material(material_id, caminho_storage: str):
    """Remove o arquivo do Storage e o registro correspondente do banco."""
    sb = get_supabase_client()
    sb.storage.from_(_BUCKET_MATERIAIS).remove([caminho_storage])
    sb.table("materiais").delete().eq("id", material_id).execute()


# ---------------------------------------------------------------------------
# DÚVIDAS (perguntas do dia a dia enviadas pelos alunos na página inicial)
# ---------------------------------------------------------------------------

def enviar_duvida(aluno_id: str, aluno_nome: str, mensagem: str):
    """Salva a dúvida no banco (funciona como registro/backup)."""
    sb = get_supabase_client()
    registro = {
        "aluno_id": aluno_id,
        "aluno_nome": aluno_nome,
        "mensagem": mensagem.strip(),
    }
    resposta = sb.table("duvidas").insert(registro).execute()
    return resposta.data[0]


def listar_duvidas(apenas_nao_respondidas: bool = False):
    """Lista as dúvidas enviadas, da mais recente para a mais antiga."""
    sb = get_supabase_client()
    consulta = sb.table("duvidas").select("*")
    if apenas_nao_respondidas:
        consulta = consulta.eq("respondida", False)
    resposta = consulta.order("criado_em", desc=True).execute()
    return resposta.data


def marcar_duvida_respondida(duvida_id):
    sb = get_supabase_client()
    sb.table("duvidas").update({"respondida": True}).eq("id", duvida_id).execute()
