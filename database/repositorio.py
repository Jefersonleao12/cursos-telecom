"""
Camada de acesso a dados (Repositório).

Concentra TODAS as consultas ao Supabase em um único lugar. Isso facilita a
manutenção: se um dia você quiser trocar de banco de dados ou entender como
alguma tela busca suas informações, é só olhar aqui.

Sem dependência de nenhum framework de UI (nem Streamlit, nem FastAPI) —
compartilhado pelas duas apps que coexistem durante a migração.
"""
import io
import time
import uuid
from datetime import datetime, timezone

from database.cache import cache_com_ttl
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


def buscar_aluno_por_cpf(cpf: str):
    """Retorna o registro do aluno pelo CPF (só dígitos), ou None se não existir. Usado no login."""
    from utils.helpers import somente_digitos

    sb = get_supabase_client()
    resposta = sb.table("alunos").select("*").eq("cpf", somente_digitos(cpf)).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_aluno_admin(nome_completo: str, cpf: str, email: str, telefone: str, filial: str, cargo: str):
    """
    Cria um novo aluno pelo painel de administração — não existe mais
    autocadastro pelo próprio aluno. A senha inicial é o próprio CPF (sem
    pontuação); o aluno pode trocá-la depois em 'Meu Perfil', se quiser.
    Marca deve_definir_foto=True pra pedir a foto de perfil uma única vez,
    no primeiro acesso. Retorna o registro criado.
    """
    from utils.helpers import somente_digitos

    sb = get_supabase_client()
    cpf_normalizado = somente_digitos(cpf)
    novo = {
        "nome_completo": nome_completo.strip(),
        "cpf": cpf_normalizado,
        "email": email.lower().strip(),
        "senha_hash": gerar_hash_senha_cpf(cpf_normalizado),
        "empresa": "Norte Tel",
        "cargo": cargo.strip() if cargo else None,
        "filial": filial.strip() if filial else None,
        "telefone": somente_digitos(telefone) if telefone else None,
        "is_admin": False,
        "deve_definir_foto": True,
    }
    resposta = sb.table("alunos").insert(novo).execute()
    return resposta.data[0]


def gerar_hash_senha_cpf(cpf: str) -> str:
    """Gera o hash bcrypt de um CPF (só dígitos) para usar como senha."""
    import bcrypt as _bcrypt

    return _bcrypt.hashpw(cpf.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def editar_aluno_admin(
    aluno_id: str, nome_completo: str, cpf: str, email: str, telefone: str, filial: str, cargo: str,
    resetar_senha_para_cpf: bool = False,
):
    """
    Atualiza os dados de um aluno já cadastrado (painel de administração) —
    usado tanto para correções gerais quanto para completar o CPF de contas
    criadas antes dessa mudança. Se resetar_senha_para_cpf=True, a senha
    também é redefinida para o novo CPF (usado ao migrar uma conta antiga).
    """
    from utils.helpers import somente_digitos

    sb = get_supabase_client()
    cpf_normalizado = somente_digitos(cpf) if cpf else None
    dados = {
        "nome_completo": nome_completo.strip(),
        "cpf": cpf_normalizado,
        "email": email.lower().strip(),
        "telefone": somente_digitos(telefone) if telefone else None,
        "filial": filial.strip() if filial else None,
        "cargo": cargo.strip() if cargo else None,
    }
    if resetar_senha_para_cpf and cpf_normalizado:
        dados["senha_hash"] = gerar_hash_senha_cpf(cpf_normalizado)
        dados["deve_trocar_senha"] = False
    sb.table("alunos").update(dados).eq("id", aluno_id).execute()
    buscar_aluno_por_id.clear()


def desmarcar_definir_foto(aluno_id: str):
    """Usado depois que o aluno define a foto de perfil pela 1ª vez (obrigatório no 1º acesso)."""
    sb = get_supabase_client()
    sb.table("alunos").update({"deve_definir_foto": False}).eq("id", aluno_id).execute()
    buscar_aluno_por_id.clear()


@cache_com_ttl(ttl=10)
def buscar_aluno_por_id(aluno_id: str):
    """Retorna o registro do aluno pelo id, ou None se não existir.

    Usado para restaurar a sessão do aluno (a cada requisição, na app
    nova — ver webapp/middleware.py — ou após um F5 na app antiga). TTL
    curto (10s) porque toda escrita relevante na tabela alunos já chama
    `.clear()` nesta função (ver ativar/desativar acesso, trocar senha
    etc.) — o cache existe só pra evitar bater no banco a cada requisição
    HTTP, não pra esconder mudanças reais por muito tempo.
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

def atualizar_perfil_aluno(aluno_id: str, empresa: str, cargo: str, filial: str, telefone: str = None):
    sb = get_supabase_client()
    dados = {
        "empresa": empresa.strip() if empresa else None,
        "cargo": cargo.strip() if cargo else None,
        "filial": filial.strip() if filial else None,
        "telefone": telefone.strip() if telefone else None,
    }
    sb.table("alunos").update(dados).eq("id", aluno_id).execute()
    buscar_aluno_por_id.clear()


def trocar_senha_aluno(aluno_id: str, novo_hash_senha: str):
    """Usado quando o próprio aluno troca a senha (Meu Perfil, ou após receber uma senha temporária)."""
    sb = get_supabase_client()
    sb.table("alunos").update(
        {"senha_hash": novo_hash_senha, "deve_trocar_senha": False}
    ).eq("id", aluno_id).execute()
    buscar_aluno_por_id.clear()


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
    url_base = sb.storage.from_(_BUCKET_FOTOS_PERFIL).get_public_url(caminho)
    # Como o caminho do arquivo é sempre o mesmo (pra sempre substituir a
    # foto antiga), a URL "pura" também seria sempre idêntica — e o
    # navegador, achando que já conhece essa URL, mostra a versão antiga
    # que tinha em cache em vez de buscar a nova. Colar um "carimbo" de
    # tempo na URL força o navegador a tratá-la como um arquivo novo.
    url = f"{url_base}?v={int(time.time())}"
    sb.table("alunos").update({"foto_url": url}).eq("id", aluno_id).execute()
    buscar_aluno_por_id.clear()
    return url


# ---------------------------------------------------------------------------
# GESTÃO DE CONTA (ações do admin sobre a conta de um aluno)
# ---------------------------------------------------------------------------

def definir_acesso_aluno(aluno_id: str, ativo: bool):
    """Ativa ou desativa o acesso de um aluno (login passa a ser bloqueado se ativo=False)."""
    sb = get_supabase_client()
    sb.table("alunos").update({"ativo": ativo}).eq("id", aluno_id).execute()
    buscar_aluno_por_id.clear()


def definir_admin_aluno(aluno_id: str, is_admin: bool):
    sb = get_supabase_client()
    sb.table("alunos").update({"is_admin": is_admin}).eq("id", aluno_id).execute()
    buscar_aluno_por_id.clear()


def solicitar_redefinicao_senha(cpf: str):
    """
    Usado na tela de login ('Esqueci minha senha'). Marca a conta para que o
    admin veja o pedido no painel e gere uma senha temporária. Retorna o
    aluno encontrado, ou None se o CPF não existir (a tela sempre mostra a
    mesma mensagem de sucesso nos dois casos, para não revelar quais CPFs
    têm cadastro).
    """
    sb = get_supabase_client()
    aluno = buscar_aluno_por_cpf(cpf)
    if aluno is None:
        return None
    sb.table("alunos").update({"solicitou_redefinicao_senha": True}).eq("id", aluno["id"]).execute()
    buscar_aluno_por_id.clear()
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
    buscar_aluno_por_id.clear()

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

@cache_com_ttl(ttl=20)
def listar_cursos():
    sb = get_supabase_client()
    resposta = sb.table("cursos").select("*").order("criado_em", desc=True).execute()
    return resposta.data


@cache_com_ttl(ttl=20)
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

@cache_com_ttl(ttl=20)
def listar_modulos_do_curso(curso_id: int):
    sb = get_supabase_client()
    resposta = sb.table("modulos").select("*").eq("curso_id", curso_id).order("ordem").execute()
    return resposta.data


@cache_com_ttl(ttl=20)
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

@cache_com_ttl(ttl=20)
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


@cache_com_ttl(ttl=20)
def listar_aulas_do_curso(curso_id: int):
    """Todas as aulas do curso, de TODOS os módulos juntos — usado para
    calcular o progresso geral do curso (barra de progresso no topo)."""
    sb = get_supabase_client()
    resposta = sb.table("aulas").select("*").eq("curso_id", curso_id).execute()
    return resposta.data


@cache_com_ttl(ttl=20)
def buscar_aula(aula_id: int):
    sb = get_supabase_client()
    resposta = sb.table("aulas").select("*").eq("id", aula_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


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
    buscar_aula.clear()


def excluir_aula(aula_id: int):
    sb = get_supabase_client()
    sb.table("aulas").delete().eq("id", aula_id).execute()
    listar_aulas_do_modulo.clear()
    listar_aulas_do_curso.clear()
    buscar_aula.clear()


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
    _consultar_aulas_concluidas.clear()


def buscar_progresso_aula(aluno_id: str, aula_id: int):
    """Retorna o registro de progresso do aluno nesta aula, ou None se ele
    nunca chegou a abri-la."""
    sb = get_supabase_client()
    resposta = (
        sb.table("progresso_aulas")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("aula_id", aula_id)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def registrar_inicio_aula(aluno_id: str, aula_id: int):
    """
    Registra (uma única vez) o instante em que o aluno começou a assistir
    esta aula. Usado pela app nova (webapp/) para checar no SERVIDOR se já
    se passou tempo suficiente antes de liberar a conclusão da aula, em vez
    de confiar só num cronômetro rodando no navegador do aluno (fácil de
    burlar mudando o relógio do sistema ou chamando a rota direto). Não faz
    nada se já existir um registro — não reinicia o cronômetro toda vez que
    o aluno reabre a aula.
    """
    existente = buscar_progresso_aula(aluno_id, aula_id)
    if existente and existente.get("iniciada_em"):
        return
    sb = get_supabase_client()
    sb.table("progresso_aulas").upsert(
        {
            "aluno_id": aluno_id,
            "aula_id": aula_id,
            "iniciada_em": datetime.now(timezone.utc).isoformat(),
        },
        on_conflict="aluno_id,aula_id",
    ).execute()


@cache_com_ttl(ttl=15)
def _consultar_aulas_concluidas(aluno_id: str, ids_aulas: tuple):
    """
    Função interna (cacheada): dado um conjunto de IDs de aula, devolve quais
    delas o aluno já concluiu. É chamada repetidas vezes a cada tela (uma vez
    por módulo, de cada curso, sempre que a página de Início ou a lista de
    cursos é desenhada) — cachear evita bater no Supabase várias vezes pela
    mesma informação em poucos segundos, deixando a navegação bem mais rápida.
    """
    if not ids_aulas:
        return []
    sb = get_supabase_client()
    resposta = (
        sb.table("progresso_aulas")
        .select("aula_id")
        .eq("aluno_id", aluno_id)
        .eq("concluida", True)
        .in_("aula_id", list(ids_aulas))
        .execute()
    )
    return [linha["aula_id"] for linha in resposta.data]


def _ids_aulas_concluidas(aluno_id: str, ids_aulas: list):
    """Função interna: dado uma lista de IDs de aula, devolve quais delas o aluno já concluiu."""
    return _consultar_aulas_concluidas(aluno_id, tuple(sorted(ids_aulas)))


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


def progresso_e_conclusao_em_lote(alunos: list, cursos: list) -> tuple[dict, dict]:
    """
    Progresso (0.0 a 1.0) e conclusão de curso pra CADA combinação
    aluno × curso — usado pelo Ranking, pelo Dashboard do admin e pela
    lista de Alunos do admin, telas que precisam ver o progresso de todo
    mundo ao mesmo tempo.

    Chama a função progresso_ranking_dados() direto no Postgres (ver
    database/schema.sql) em vez de calcular isso em Python: uma consulta
    ao banco por combinação aluno×curso virava dezenas/centenas de idas e
    vindas de rede (visivelmente lento mesmo com CPU/rede sobrando); trazer
    as tabelas cruas inteiras pro servidor e calcular em Python já resolvia
    isso (~5-7 consultas fixas), mas deixar o próprio banco fazer a conta
    reduz pra 1 consulta só, não importa quantos alunos/cursos existam.

    Retorna dois dicts indexados por [aluno_id][curso_id]:
    - progresso: percentual (0.0 a 1.0) de aulas concluídas no curso
    - concluido: True se TODOS os módulos do curso estão completos
    """
    sb = get_supabase_client()
    linhas = sb.rpc("progresso_ranking_dados").execute().data

    progresso: dict = {a["id"]: {} for a in alunos}
    concluido: dict = {a["id"]: {} for a in alunos}
    for linha in linhas:
        aluno_id = linha["aluno_id"]
        if aluno_id not in progresso:
            continue  # aluno fora da lista pedida (ex: já filtrado por busca/ativo)
        progresso[aluno_id][linha["curso_id"]] = float(linha["progresso"])
        concluido[aluno_id][linha["curso_id"]] = bool(linha["concluido"])

    # A função no banco cobre todo aluno × todo curso, mas por garantia
    # (ex: curso criado depois da última consulta) preenche o que faltar.
    for aluno in alunos:
        for curso in cursos:
            progresso[aluno["id"]].setdefault(curso["id"], 0.0)
            concluido[aluno["id"]].setdefault(curso["id"], False)

    return progresso, concluido


@cache_com_ttl(ttl=60)
def calcular_ranking_alunos():
    """
    Ranking dos alunos por progresso nos cursos, usado na tela "Top Alunos"
    (visível pra todo mundo, não só o admin, como incentivo).

    Usa progresso_e_conclusao_em_lote() pra evitar o padrão N+1 de
    consultas (ver o comentário lá). Como um ranking não precisa estar
    atualizado no segundo exato, cacheamos o resultado inteiro por 1
    minuto por cima disso.

    Ordena por: 1) mais cursos concluídos, 2) maior progresso médio nos
    cursos disponíveis, 3) nome (desempate estável). Só entram alunos ativos
    que já começaram pelo menos um curso — quem nunca abriu nada não aparece
    no ranking (não tem "0º lugar" pra ninguém).

    Retorna a lista ORDENADA COMPLETA (não só os primeiros) — quem chama
    decide quantos exibir e também consegue achar a posição de um aluno
    específico dentro dela.
    """
    alunos = [a for a in listar_todos_alunos() if a.get("ativo", True)]
    cursos = listar_cursos()
    if not alunos or not cursos:
        return []

    progresso, concluido = progresso_e_conclusao_em_lote(alunos, cursos)

    ranking = []
    for aluno in alunos:
        aluno_id = aluno["id"]
        progressos = list(progresso[aluno_id].values())
        progresso_medio = sum(progressos) / len(progressos) if progressos else 0.0
        if progresso_medio <= 0:
            continue  # não começou nenhum curso ainda: fica fora do ranking

        cursos_concluidos = sum(1 for v in concluido[aluno_id].values() if v)
        ranking.append({
            "aluno_id": aluno_id,
            "nome_completo": aluno["nome_completo"],
            "empresa": aluno.get("empresa"),
            "filial": aluno.get("filial"),
            "foto_url": aluno.get("foto_url"),
            "cursos_concluidos": cursos_concluidos,
            "progresso_medio": progresso_medio,
        })

    ranking.sort(key=lambda r: (-r["cursos_concluidos"], -r["progresso_medio"], r["nome_completo"]))
    return ranking


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


def todos_tempos_curso() -> dict:
    """
    Igual obter_tempos_curso, mas pra TODOS os alunos/cursos de uma vez só
    (uma consulta), indexado por (aluno_id, curso_id) — usado em telas que
    precisam disso pra vários alunos (ex: lista de Alunos do admin), pra
    não fazer uma consulta por combinação.
    """
    sb = get_supabase_client()
    resposta = sb.table("progresso_cursos").select("*").execute()
    return {(linha["aluno_id"], linha["curso_id"]): linha for linha in resposta.data}


# ---------------------------------------------------------------------------
# PROVAS E PERGUNTAS
# ---------------------------------------------------------------------------

@cache_com_ttl(ttl=20)
def buscar_prova_do_modulo(modulo_id: int):
    sb = get_supabase_client()
    resposta = sb.table("provas").select("*").eq("modulo_id", modulo_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


@cache_com_ttl(ttl=20)
def buscar_prova_do_curso(curso_id: int):
    """Compatibilidade: retorna a primeira prova encontrada entre os módulos do curso."""
    sb = get_supabase_client()
    resposta = sb.table("provas").select("*").eq("curso_id", curso_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


@cache_com_ttl(ttl=20)
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


@cache_com_ttl(ttl=20)
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
    melhor_resultado.clear()
    return resposta.data[0]


@cache_com_ttl(ttl=15)
def melhor_resultado(aluno_id: str, prova_id: int):
    """
    Retorna o melhor resultado (maior nota) que o aluno já obteve nesta prova.
    Cacheado porque é consultado uma vez por módulo com prova, de cada curso,
    toda vez que a Início ou a lista de cursos calcula o progresso do aluno.
    """
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
# MATERIAIS (links para arquivos/pastas do Google Drive, organizados por
# categoria — cada material é um card com ícone + título clicável)
# ---------------------------------------------------------------------------

def criar_material(titulo: str, descricao: str, categoria: str, link_url: str, icone: str):
    """Grava um novo material (link) na tabela 'materiais'. Retorna o registro criado."""
    sb = get_supabase_client()
    novo = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "categoria": categoria.strip(),
        "link_url": link_url.strip(),
        "icone": icone or "🔗",
    }
    resposta = sb.table("materiais").insert(novo).execute()
    listar_materiais.clear()
    listar_categorias_materiais.clear()
    return resposta.data[0]


@cache_com_ttl(ttl=20)
def listar_materiais():
    """Lista todos os materiais, do mais recente para o mais antigo."""
    sb = get_supabase_client()
    resposta = sb.table("materiais").select("*").order("criado_em", desc=True).execute()
    return resposta.data


@cache_com_ttl(ttl=20)
def listar_categorias_materiais():
    """Lista as categorias já usadas (sem repetir), em ordem alfabética."""
    materiais = listar_materiais()
    categorias = sorted({m["categoria"] for m in materiais if m.get("categoria")})
    return categorias


def excluir_material(material_id):
    """Remove o registro do material (o arquivo em si continua no Drive do admin)."""
    sb = get_supabase_client()
    sb.table("materiais").delete().eq("id", material_id).execute()
    listar_materiais.clear()
    listar_categorias_materiais.clear()


def editar_material(material_id, titulo: str, descricao: str, categoria: str, link_url: str, icone: str):
    """Atualiza os dados do material (título/descrição/categoria/link/ícone)."""
    sb = get_supabase_client()
    dados = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "categoria": categoria.strip(),
        "link_url": link_url.strip(),
        "icone": icone or "🔗",
    }
    sb.table("materiais").update(dados).eq("id", material_id).execute()
    listar_materiais.clear()
    listar_categorias_materiais.clear()


# ---------------------------------------------------------------------------
# DÚVIDAS (perguntas do dia a dia enviadas pelos alunos na página inicial)
# ---------------------------------------------------------------------------

def enviar_duvida(aluno_id: str, aluno_nome: str, mensagem: str, telefone: str = None):
    """Salva a dúvida no banco (funciona como registro/backup). O telefone é
    o que estiver salvo no perfil do aluno no momento do envio — facilita o
    admin entrar em contato sem precisar procurar o cadastro dele."""
    sb = get_supabase_client()
    registro = {
        "aluno_id": aluno_id,
        "aluno_nome": aluno_nome,
        "telefone": telefone.strip() if telefone else None,
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


@cache_com_ttl(ttl=20)
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


# ---------------------------------------------------------------------------
# DESTAQUES (carrossel de fotos na tela de Início — técnicos da equipe,
# trajetória de carreira dentro da empresa etc.)
# ---------------------------------------------------------------------------

# Nome do "bucket" no Supabase Storage onde as fotos do carrossel ficam
# guardadas. Precisa ser criado uma vez no painel do Supabase (Storage ->
# New bucket), marcado como "Public bucket", igual aos outros buckets do projeto.
_BUCKET_DESTAQUES = "destaques"


def _processar_foto_destaque(arquivo_bytes: bytes) -> bytes:
    """Recorta a imagem num formato widescreen (4:3) e redimensiona, para
    todas as fotos do carrossel ficarem com a mesma proporção."""
    from PIL import Image

    imagem = Image.open(io.BytesIO(arquivo_bytes)).convert("RGB")
    proporcao_alvo = 4 / 3
    largura, altura = imagem.size
    proporcao_atual = largura / altura

    if proporcao_atual > proporcao_alvo:
        # imagem mais larga que o alvo: corta as laterais
        nova_largura = int(altura * proporcao_alvo)
        esquerda = (largura - nova_largura) // 2
        imagem = imagem.crop((esquerda, 0, esquerda + nova_largura, altura))
    else:
        # imagem mais alta que o alvo: corta em cima/embaixo
        nova_altura = int(largura / proporcao_alvo)
        topo = (altura - nova_altura) // 2
        imagem = imagem.crop((0, topo, largura, topo + nova_altura))

    imagem = imagem.resize((800, 600))
    buffer = io.BytesIO()
    imagem.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()


def criar_destaque(titulo: str, descricao: str, arquivo_bytes: bytes, ordem: int):
    """Sobe a foto para o Storage e cria o registro do destaque. Retorna o registro criado."""
    sb = get_supabase_client()
    foto_processada = _processar_foto_destaque(arquivo_bytes)
    caminho_storage = f"{uuid.uuid4().hex}.jpg"

    sb.storage.from_(_BUCKET_DESTAQUES).upload(
        caminho_storage, foto_processada, file_options={"content-type": "image/jpeg"}
    )
    foto_url = sb.storage.from_(_BUCKET_DESTAQUES).get_public_url(caminho_storage)

    novo = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "foto_url": foto_url,
        "caminho_storage": caminho_storage,
        "ordem": ordem,
    }
    resposta = sb.table("destaques").insert(novo).execute()
    listar_destaques_ativos.clear()
    listar_todos_destaques.clear()
    return resposta.data[0]


def editar_destaque(
    destaque_id, titulo: str, descricao: str, ordem: int, ativo: bool,
    caminho_storage_atual: str, novo_arquivo_bytes: bytes = None,
):
    """
    Atualiza título/descrição/ordem/ativo. Se novo_arquivo_bytes for informado,
    troca também a foto (removendo a antiga do Storage e subindo a nova).
    """
    sb = get_supabase_client()
    dados = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else None,
        "ordem": ordem,
        "ativo": ativo,
    }

    if novo_arquivo_bytes is not None:
        foto_processada = _processar_foto_destaque(novo_arquivo_bytes)
        novo_caminho = f"{uuid.uuid4().hex}.jpg"
        sb.storage.from_(_BUCKET_DESTAQUES).upload(
            novo_caminho, foto_processada, file_options={"content-type": "image/jpeg"}
        )
        try:
            sb.storage.from_(_BUCKET_DESTAQUES).remove([caminho_storage_atual])
        except Exception:
            pass  # segue mesmo se a foto antiga já não existir mais
        dados["caminho_storage"] = novo_caminho
        dados["foto_url"] = sb.storage.from_(_BUCKET_DESTAQUES).get_public_url(novo_caminho)

    sb.table("destaques").update(dados).eq("id", destaque_id).execute()
    listar_destaques_ativos.clear()
    listar_todos_destaques.clear()


def excluir_destaque(destaque_id, caminho_storage: str):
    """Remove a foto do Storage e o registro correspondente do banco."""
    sb = get_supabase_client()
    try:
        sb.storage.from_(_BUCKET_DESTAQUES).remove([caminho_storage])
    except Exception:
        pass
    sb.table("destaques").delete().eq("id", destaque_id).execute()
    listar_destaques_ativos.clear()
    listar_todos_destaques.clear()


@cache_com_ttl(ttl=20)
def listar_destaques_ativos():
    """Usado na tela de Início — só os destaques que o admin não desativou, em ordem."""
    sb = get_supabase_client()
    resposta = (
        sb.table("destaques")
        .select("*")
        .eq("ativo", True)
        .order("ordem")
        .execute()
    )
    return resposta.data


@cache_com_ttl(ttl=20)
def listar_todos_destaques():
    """Usado no painel admin — mostra ativos e inativos, para gerenciar."""
    sb = get_supabase_client()
    resposta = sb.table("destaques").select("*").order("ordem").execute()
    return resposta.data
