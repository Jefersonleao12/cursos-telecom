"""
Camada de acesso a dados (Repositório).

Concentra TODAS as consultas ao Supabase em um único lugar. Isso facilita a
manutenção: se um dia você quiser trocar de banco de dados ou entender como
alguma tela busca suas informações, é só olhar aqui.
"""
import io
import uuid
from datetime import datetime, timezone

import streamlit as st

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


def buscar_aluno_por_id(aluno_id: str):
    """Retorna o registro do aluno pelo id, ou None se não existir.

    Usado para restaurar a sessão do aluno após um F5 / recarregamento de
    página, a partir do token de sessão guardado na URL (ver modules/auth.py).
    """
    sb = get_supabase_client()
    resposta = sb.table("alunos").select("*").eq("id", aluno_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def listar_todos_alunos():
    """Usado no painel administrativo para listar todos os alunos cadastrados."""
    sb = get_supabase_client()
    resposta = sb.table("alunos").select("*").order("criado_em", desc=True).execute()
    return resposta.data


# ---------------------------------------------------------------------------
# PERFIL DO ALUNO (o próprio aluno atualizando seus dados/senha)
# ---------------------------------------------------------------------------

def atualizar_perfil_aluno(aluno_id: str, empresa: str, cargo: str, filial: str):
    sb = get_supabase_client()
    dados = {
        "empresa": empresa.strip() if empresa else None,
        "cargo": cargo.strip() if cargo else None,
        "filial": filial.strip() if filial else None,
    }
    sb.table("alunos").update(dados).eq("id", aluno_id).execute()


def trocar_senha_aluno(aluno_id: str, novo_hash_senha: str):
    """Usado quando o próprio aluno troca a senha (Meu Perfil, ou após receber uma senha temporária)."""
    sb = get_supabase_client()
    sb.table("alunos").update(
        {"senha_hash": novo_hash_senha, "deve_trocar_senha": False}
    ).eq("id", aluno_id).execute()


# Nome do bucket no Supabase Storage onde ficam as fotos de perfil.
_BUCKET_FOTOS_PERFIL = "fotos-perfil"


def _processar_foto_perfil(arquivo_bytes: bytes) -> bytes:
    """Recorta a imagem em um quadrado centralizado e redimensiona, para
    todas as fotos ficarem com a mesma proporção (400x400) na plataforma."""
    from PIL import Image

    imagem = Image.open(io.BytesIO(arquivo_bytes)).convert("RGB")
    lado = min(imagem.size)
    esquerda = (imagem.width - lado) // 2
    topo = (imagem.height - lado) // 2
    imagem_quadrada = imagem.crop((esquerda, topo, esquerda + lado, topo + lado))
    imagem_quadrada = imagem_quadrada.resize((400, 400))

    buffer = io.BytesIO()
    imagem_quadrada.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()


def atualizar_foto_perfil(aluno_id: str, arquivo_bytes: bytes) -> str:
    """
    Processa (recorta/redimensiona) e sobe a foto de perfil do aluno para o
    Storage, sempre no mesmo caminho (substitui a foto antiga, se houver).
    Salva o link público na tabela alunos e devolve esse link.
    """
    sb = get_supabase_client()
    foto_processada = _processar_foto_perfil(arquivo_bytes)
    caminho = f"{aluno_id}.jpg"

    try:
        sb.storage.from_(_BUCKET_FOTOS_PERFIL).remove([caminho])
    except Exception:
        pass  # ainda não existia uma foto anterior — tudo bem

    sb.storage.from_(_BUCKET_FOTOS_PERFIL).upload(
        caminho, foto_processada, file_options={"content-type": "image/jpeg"}
    )
    url = sb.storage.from_(_BUCKET_FOTOS_PERFIL).get_public_url(caminho)
    sb.table("alunos").update({"foto_url": url}).eq("id", aluno_id).execute()
    return url


# ---------------------------------------------------------------------------
# GESTÃO DE CONTA (ações do admin sobre a conta de um aluno)
# ---------------------------------------------------------------------------

def definir_acesso_aluno(aluno_id: str, ativo: bool):
    """Ativa ou desativa o acesso de um aluno (login passa a ser bloqueado se ativo=False)."""
    sb = get_supabase_client()
    sb.table("alunos").update({"ativo": ativo}).eq("id", aluno_id).execute()


def definir_admin_aluno(aluno_id: str, is_admin: bool):
    sb = get_supabase_client()
    sb.table("alunos").update({"is_admin": is_admin}).eq("id", aluno_id).execute()


def solicitar_redefinicao_senha(email: str):
    """
    Usado na tela de login ('Esqueci minha senha'). Marca a conta para que o
    admin veja o pedido no painel e gere uma senha temporária. Retorna o
    aluno encontrado, ou None se o e-mail não existir (a tela sempre mostra
    a mesma mensagem de sucesso nos dois casos, para não revelar quais
    e-mails têm cadastro).
    """
    sb = get_supabase_client()
    aluno = buscar_aluno_por_email(email)
    if aluno is None:
        return None
    sb.table("alunos").update({"solicitou_redefinicao_senha": True}).eq("id", aluno["id"]).execute()
    return aluno


def listar_solicitacoes_redefinicao_senha():
    sb = get_supabase_client()
    resposta = (
        sb.table("alunos")
        .select("*")
        .eq("solicitou_redefinicao_senha", True)
        .order("nome_completo")
        .execute()
    )
    return resposta.data


def gerar_senha_temporaria(aluno_id: str) -> str:
    """
    Usado pelo admin (painel) para resetar a senha de um aluno — seja porque
    ele pediu 'esqueci minha senha', seja por iniciativa do próprio admin.
    Gera uma senha temporária aleatória, já salva o hash dela no banco, marca
    que o aluno precisa trocá-la no próximo login, e devolve a senha em texto
    puro (só para o admin ver na hora e repassar ao aluno — não fica salva
    em lugar nenhum em texto puro).
    """
    import secrets as _secrets
    import string as _string
    import bcrypt as _bcrypt

    alfabeto = _string.ascii_uppercase + _string.ascii_lowercase + _string.digits
    senha_temporaria = "".join(_secrets.choice(alfabeto) for _ in range(8))
    hash_senha = _bcrypt.hashpw(senha_temporaria.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")

    sb = get_supabase_client()
    sb.table("alunos").update(
        {
            "senha_hash": hash_senha,
            "deve_trocar_senha": True,
            "solicitou_redefinicao_senha": False,
        }
    ).eq("id", aluno_id).execute()

    return senha_temporaria


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

@st.cache_data(ttl=20, show_spinner=False)
def listar_cursos():
    sb = get_supabase_client()
    resposta = sb.table("cursos").select("*").order("criado_em", desc=True).execute()
    return resposta.data


@st.cache_data(ttl=20, show_spinner=False)
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
    listar_cursos.clear()
    return resposta.data[0]


def editar_curso(curso_id: int, titulo: str, descricao: str, instrutor: str, carga_horaria: int):
    sb = get_supabase_client()
    dados = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "instrutor": instrutor.strip(),
        "carga_horaria": carga_horaria,
    }
    sb.table("cursos").update(dados).eq("id", curso_id).execute()
    listar_cursos.clear()
    buscar_curso.clear()


def excluir_curso(curso_id: int):
    """Exclui o curso e, em cascata, suas aulas, provas, resultados e certificados."""
    sb = get_supabase_client()
    sb.table("cursos").delete().eq("id", curso_id).execute()
    listar_cursos.clear()
    buscar_curso.clear()


# ---------------------------------------------------------------------------
# MÓDULOS (assuntos dentro de um curso)
# ---------------------------------------------------------------------------

@st.cache_data(ttl=20, show_spinner=False)
def listar_modulos_do_curso(curso_id: int):
    sb = get_supabase_client()
    resposta = sb.table("modulos").select("*").eq("curso_id", curso_id).order("ordem").execute()
    return resposta.data


@st.cache_data(ttl=20, show_spinner=False)
def buscar_modulo(modulo_id: int):
    sb = get_supabase_client()
    resposta = sb.table("modulos").select("*").eq("id", modulo_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_modulo(curso_id: int, titulo: str, ordem: int):
    sb = get_supabase_client()
    novo = {"curso_id": curso_id, "titulo": titulo.strip(), "ordem": ordem}
    resposta = sb.table("modulos").insert(novo).execute()
    listar_modulos_do_curso.clear()
    return resposta.data[0]


def editar_modulo(modulo_id: int, titulo: str, ordem: int):
    sb = get_supabase_client()
    sb.table("modulos").update({"titulo": titulo.strip(), "ordem": ordem}).eq("id", modulo_id).execute()
    listar_modulos_do_curso.clear()
    buscar_modulo.clear()


def excluir_modulo(modulo_id: int):
    """Exclui o módulo e, em cascata, suas aulas, prova e resultados."""
    sb = get_supabase_client()
    sb.table("modulos").delete().eq("id", modulo_id).execute()
    listar_modulos_do_curso.clear()
    buscar_modulo.clear()


# ---------------------------------------------------------------------------
# AULAS (agora pertencem a um módulo)
# ---------------------------------------------------------------------------

@st.cache_data(ttl=20, show_spinner=False)
def listar_aulas_do_modulo(modulo_id: int):
    sb = get_supabase_client()
    resposta = (
        sb.table("aulas")
        .select("*")
        .eq("modulo_id", modulo_id)
        .order("ordem")
        .execute()
    )
    return resposta.data


@st.cache_data(ttl=20, show_spinner=False)
def listar_aulas_do_curso(curso_id: int):
    """Todas as aulas do curso, de TODOS os módulos juntos — usado para
    calcular o progresso geral do curso (barra de progresso no topo)."""
    sb = get_supabase_client()
    resposta = sb.table("aulas").select("*").eq("curso_id", curso_id).execute()
    return resposta.data


def criar_aula(modulo_id: int, curso_id: int, titulo: str, url_video: str, ordem: int, duracao_minutos: int):
    sb = get_supabase_client()
    nova = {
        "modulo_id": modulo_id,
        "curso_id": curso_id,
        "titulo": titulo.strip(),
        "url_video": url_video.strip(),
        "ordem": ordem,
        "duracao_minutos": duracao_minutos,
    }
    resposta = sb.table("aulas").insert(nova).execute()
    listar_aulas_do_modulo.clear()
    listar_aulas_do_curso.clear()
    return resposta.data[0]


def editar_aula(aula_id: int, titulo: str, url_video: str, ordem: int, duracao_minutos: int):
    sb = get_supabase_client()
    dados = {
        "titulo": titulo.strip(),
        "url_video": url_video.strip(),
        "ordem": ordem,
        "duracao_minutos": duracao_minutos,
    }
    sb.table("aulas").update(dados).eq("id", aula_id).execute()
    listar_aulas_do_modulo.clear()
    listar_aulas_do_curso.clear()


def excluir_aula(aula_id: int):
    sb = get_supabase_client()
    sb.table("aulas").delete().eq("id", aula_id).execute()
    listar_aulas_do_modulo.clear()
    listar_aulas_do_curso.clear()


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


def _ids_aulas_concluidas(aluno_id: str, ids_aulas: list):
    """Função interna: dado uma lista de IDs de aula, devolve quais delas o aluno já concluiu."""
    if not ids_aulas:
        return []
    sb = get_supabase_client()
    resposta = (
        sb.table("progresso_aulas")
        .select("aula_id")
        .eq("aluno_id", aluno_id)
        .eq("concluida", True)
        .in_("aula_id", ids_aulas)
        .execute()
    )
    return [linha["aula_id"] for linha in resposta.data]


def aulas_concluidas_do_aluno(aluno_id: str, curso_id: int):
    """Retorna a lista de IDs de aulas já concluídas pelo aluno, dentro de um curso (todos os módulos)."""
    ids_aulas = [a["id"] for a in listar_aulas_do_curso(curso_id)]
    return _ids_aulas_concluidas(aluno_id, ids_aulas)


def aulas_concluidas_do_modulo(aluno_id: str, modulo_id: int):
    """Retorna a lista de IDs de aulas já concluídas pelo aluno, dentro de um módulo específico."""
    ids_aulas = [a["id"] for a in listar_aulas_do_modulo(modulo_id)]
    return _ids_aulas_concluidas(aluno_id, ids_aulas)


def calcular_progresso_curso(aluno_id: str, curso_id: int) -> float:
    """Retorna o percentual (0.0 a 1.0) de aulas concluídas em um curso (visão geral)."""
    aulas = listar_aulas_do_curso(curso_id)
    if not aulas:
        return 0.0
    concluidas = aulas_concluidas_do_aluno(aluno_id, curso_id)
    return len(concluidas) / len(aulas)


def modulo_esta_completo(aluno_id: str, modulo_id: int) -> bool:
    """
    Um módulo está completo quando: todas as suas aulas foram concluídas E
    (se o módulo tiver uma prova) o aluno foi aprovado nela. Módulos sem
    nenhuma aula cadastrada ainda contam como incompletos.
    """
    aulas = listar_aulas_do_modulo(modulo_id)
    if not aulas:
        return False
    concluidas = aulas_concluidas_do_modulo(aluno_id, modulo_id)
    if len(concluidas) < len(aulas):
        return False

    prova = buscar_prova_do_modulo(modulo_id)
    if prova:
        resultado = melhor_resultado(aluno_id, prova["id"])
        if not resultado or not resultado["aprovado"]:
            return False

    return True


def curso_totalmente_concluido(aluno_id: str, curso_id: int) -> bool:
    """O curso só é considerado concluído quando TODOS os seus módulos estão completos."""
    modulos = listar_modulos_do_curso(curso_id)
    if not modulos:
        return False
    return all(modulo_esta_completo(aluno_id, m["id"]) for m in modulos)


def nota_final_curso(aluno_id: str, curso_id: int):
    """
    Nota final do curso para o certificado: a média das notas obtidas nas
    provas dos módulos que têm avaliação. Se nenhum módulo tiver prova
    (curso só com vídeos), devolve None — o certificado mostra 'Concluído'
    em vez de uma nota numérica nesse caso.
    """
    modulos = listar_modulos_do_curso(curso_id)
    notas = []
    for modulo in modulos:
        prova = buscar_prova_do_modulo(modulo["id"])
        if prova:
            resultado = melhor_resultado(aluno_id, prova["id"])
            if resultado:
                notas.append(float(resultado["nota"]))
    if not notas:
        return None
    return sum(notas) / len(notas)


# ---------------------------------------------------------------------------
# TEMPO DE CONCLUSÃO DO CURSO (quando começou, quando terminou)
# ---------------------------------------------------------------------------

def registrar_inicio_curso(aluno_id: str, curso_id: int):
    """
    Registra o instante em que o aluno começou o curso (primeira vez que
    abriu a tela do curso). Não faz nada se já existir um registro — ou
    seja, é seguro chamar isso toda vez que a tela é aberta.
    """
    sb = get_supabase_client()
    existente = (
        sb.table("progresso_cursos")
        .select("id")
        .eq("aluno_id", aluno_id)
        .eq("curso_id", curso_id)
        .execute()
    )
    if not existente.data:
        sb.table("progresso_cursos").insert(
            {"aluno_id": aluno_id, "curso_id": curso_id}
        ).execute()


def finalizar_progresso_curso(aluno_id: str, curso_id: int):
    """Marca o instante em que o aluno concluiu o curso (foi aprovado na prova final)."""
    sb = get_supabase_client()
    sb.table("progresso_cursos").update(
        {"finalizado_em": datetime.now(timezone.utc).isoformat()}
    ).eq("aluno_id", aluno_id).eq("curso_id", curso_id).is_("finalizado_em", "null").execute()


def obter_tempos_curso(aluno_id: str, curso_id: int):
    """Retorna o registro de início/fim do curso para este aluno (ou None)."""
    sb = get_supabase_client()
    resposta = (
        sb.table("progresso_cursos")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("curso_id", curso_id)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


# ---------------------------------------------------------------------------
# PROVAS E PERGUNTAS
# ---------------------------------------------------------------------------

@st.cache_data(ttl=20, show_spinner=False)
def buscar_prova_do_modulo(modulo_id: int):
    sb = get_supabase_client()
    resposta = sb.table("provas").select("*").eq("modulo_id", modulo_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


@st.cache_data(ttl=20, show_spinner=False)
def buscar_prova_do_curso(curso_id: int):
    """Compatibilidade: retorna a primeira prova encontrada entre os módulos do curso."""
    sb = get_supabase_client()
    resposta = sb.table("provas").select("*").eq("curso_id", curso_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


@st.cache_data(ttl=20, show_spinner=False)
def listar_provas_do_curso(curso_id: int):
    """Todas as provas do curso, uma por módulo (útil para o dashboard/admin)."""
    sb = get_supabase_client()
    resposta = sb.table("provas").select("*").eq("curso_id", curso_id).execute()
    return resposta.data


def criar_prova(modulo_id: int, curso_id: int, titulo: str, nota_minima: float):
    sb = get_supabase_client()
    nova = {
        "modulo_id": modulo_id,
        "curso_id": curso_id,
        "titulo": titulo.strip(),
        "nota_minima": nota_minima,
    }
    resposta = sb.table("provas").insert(nova).execute()
    buscar_prova_do_modulo.clear()
    buscar_prova_do_curso.clear()
    listar_provas_do_curso.clear()
    return resposta.data[0]


def editar_prova(prova_id: int, titulo: str, nota_minima: float):
    sb = get_supabase_client()
    sb.table("provas").update(
        {"titulo": titulo.strip(), "nota_minima": nota_minima}
    ).eq("id", prova_id).execute()
    buscar_prova_do_modulo.clear()
    buscar_prova_do_curso.clear()
    listar_provas_do_curso.clear()


def excluir_prova(prova_id: int):
    """Exclui a prova e, em cascata, suas perguntas e resultados."""
    sb = get_supabase_client()
    sb.table("provas").delete().eq("id", prova_id).execute()
    buscar_prova_do_modulo.clear()
    buscar_prova_do_curso.clear()
    listar_provas_do_curso.clear()


@st.cache_data(ttl=20, show_spinner=False)
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
    listar_perguntas.clear()
    return resposta.data[0]


def editar_pergunta(pergunta_id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta, ordem):
    sb = get_supabase_client()
    dados = {
        "enunciado": enunciado.strip(),
        "opcao_a": opcao_a.strip(),
        "opcao_b": opcao_b.strip(),
        "opcao_c": opcao_c.strip(),
        "opcao_d": opcao_d.strip(),
        "resposta_correta": resposta_correta.upper().strip(),
        "ordem": ordem,
    }
    sb.table("perguntas").update(dados).eq("id", pergunta_id).execute()
    listar_perguntas.clear()


def excluir_pergunta(pergunta_id):
    sb = get_supabase_client()
    sb.table("perguntas").delete().eq("id", pergunta_id).execute()
    listar_perguntas.clear()


# ---------------------------------------------------------------------------
# RESULTADOS DE PROVAS
# ---------------------------------------------------------------------------

def salvar_resultado_prova(aluno_id: str, prova_id: int, nota: float, aprovado: bool, tempo_gasto_segundos: int = None):
    sb = get_supabase_client()
    registro = {
        "aluno_id": aluno_id,
        "prova_id": prova_id,
        "nota": nota,
        "aprovado": aprovado,
        "tempo_gasto_segundos": tempo_gasto_segundos,
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


def ultimo_resultado(aluno_id: str, prova_id: int):
    """
    Retorna a tentativa MAIS RECENTE do aluno nesta prova (não necessariamente
    a de maior nota). É essa tentativa que decide se ele pode ou não tentar de
    novo: uma vez enviada, a nota fica travada até um admin liberar.
    """
    sb = get_supabase_client()
    resposta = (
        sb.table("resultados_provas")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("prova_id", prova_id)
        .order("realizada_em", desc=True)
        .limit(1)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def listar_resultados_da_prova(prova_id: int):
    """Lista todas as tentativas desta prova (todos os alunos), mais recentes primeiro."""
    sb = get_supabase_client()
    resposta = (
        sb.table("resultados_provas")
        .select("*")
        .eq("prova_id", prova_id)
        .order("realizada_em", desc=True)
        .execute()
    )
    return resposta.data


def liberar_nova_tentativa(resultado_id):
    """
    Usado pelo admin: libera para o aluno refazer a prova mesmo já tendo um
    resultado reprovado salvo. Essa liberação vale só para a PRÓXIMA
    tentativa — depois que ele enviar de novo, volta a ficar travado.
    """
    sb = get_supabase_client()
    sb.table("resultados_provas").update(
        {"liberado_para_nova_tentativa": True}
    ).eq("id", resultado_id).execute()


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


def listar_todos_certificados():
    """Usado no dashboard do admin, para contar total emitido e ranking por curso."""
    sb = get_supabase_client()
    resposta = sb.table("certificados").select("*").execute()
    return resposta.data


def listar_todos_resultados_provas():
    """Usado no dashboard do admin, para calcular a taxa média de aprovação."""
    sb = get_supabase_client()
    resposta = sb.table("resultados_provas").select("*").execute()
    return resposta.data


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
    listar_materiais.clear()
    listar_categorias_materiais.clear()
    return resposta.data[0]


@st.cache_data(ttl=20, show_spinner=False)
def listar_materiais():
    """Lista todos os materiais, do mais recente para o mais antigo."""
    sb = get_supabase_client()
    resposta = sb.table("materiais").select("*").order("criado_em", desc=True).execute()
    return resposta.data


@st.cache_data(ttl=20, show_spinner=False)
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
    listar_materiais.clear()
    listar_categorias_materiais.clear()


def editar_material(material_id, titulo: str, descricao: str, categoria: str):
    """Atualiza só os dados (título/descrição/categoria) — o arquivo continua o mesmo."""
    sb = get_supabase_client()
    dados = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "categoria": categoria.strip(),
    }
    sb.table("materiais").update(dados).eq("id", material_id).execute()
    listar_materiais.clear()
    listar_categorias_materiais.clear()


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


# ---------------------------------------------------------------------------
# AVISOS (comunicados gerais do admin para todos os alunos)
# ---------------------------------------------------------------------------

def criar_aviso(titulo: str, mensagem: str):
    sb = get_supabase_client()
    novo = {"titulo": titulo.strip(), "mensagem": mensagem.strip()}
    resposta = sb.table("avisos").insert(novo).execute()
    listar_avisos_ativos.clear()
    return resposta.data[0]


@st.cache_data(ttl=20, show_spinner=False)
def listar_avisos_ativos():
    """Usado na tela de Início — mostra só os avisos que o admin não desativou."""
    sb = get_supabase_client()
    resposta = (
        sb.table("avisos")
        .select("*")
        .eq("ativo", True)
        .order("criado_em", desc=True)
        .execute()
    )
    return resposta.data


def listar_todos_avisos():
    """Usado no painel admin — mostra ativos e inativos, para gerenciar."""
    sb = get_supabase_client()
    resposta = sb.table("avisos").select("*").order("criado_em", desc=True).execute()
    return resposta.data


def desativar_aviso(aviso_id):
    sb = get_supabase_client()
    sb.table("avisos").update({"ativo": False}).eq("id", aviso_id).execute()
    listar_avisos_ativos.clear()
