"""
Identifica o "host" de um link de vídeo de aula e monta a URL de embed
certa pra cada um.

A partir de agora os cursos novos usam vídeos hospedados no Google Drive
(em vez de YouTube não listado, como antes) — mas cursos antigos podem
ainda ter links do YouTube cadastrados, então os dois formatos continuam
suportados aqui. Diferente da app antiga (modules/youtube_tracker.py), a
nova app NÃO tenta medir o tempo REAL de reprodução dentro do player (nem
o Drive nem uma versão simplificada do YouTube oferecem esse dado sem um
componente de JavaScript dedicado) — o controle de "assistiu o suficiente"
virou uma responsabilidade do servidor (ver registrar_inicio_aula em
database/repositorio.py), não do player. Funciona igual para qualquer
host de vídeo.
"""
import re
from urllib.parse import parse_qs, urlparse

_REGEX_ID_YOUTUBE = re.compile(r"[A-Za-z0-9_-]{11}")
_REGEX_ID_DRIVE = re.compile(r"[A-Za-z0-9_-]{10,}")


def _extrair_id_youtube(url: str):
    try:
        partes = urlparse(url)
    except ValueError:
        return None
    if not partes.hostname and not url.lower().startswith(("http://", "https://")):
        try:
            partes = urlparse(f"https://{url}")
        except ValueError:
            return None

    host = (partes.hostname or "").lower().removeprefix("www.").removeprefix("m.")
    candidato = None

    if host == "youtu.be":
        candidato = partes.path.lstrip("/").split("/")[0]
    elif host in ("youtube.com", "youtube-nocookie.com"):
        if partes.path == "/watch":
            valores = parse_qs(partes.query).get("v")
            candidato = valores[0] if valores else None
        else:
            for prefixo in ("/embed/", "/shorts/", "/live/"):
                if partes.path.startswith(prefixo):
                    candidato = partes.path[len(prefixo):].split("/")[0]
                    break

    if not candidato:
        return None
    correspondencia = _REGEX_ID_YOUTUBE.match(candidato)
    return correspondencia.group(0) if correspondencia else None


def _extrair_id_drive(url: str):
    try:
        partes = urlparse(url)
    except ValueError:
        return None
    if not partes.hostname and not url.lower().startswith(("http://", "https://")):
        try:
            partes = urlparse(f"https://{url}")
        except ValueError:
            return None

    host = (partes.hostname or "").lower().removeprefix("www.")
    if host != "drive.google.com":
        return None

    # Formatos aceitos: /file/d/ID/view, /file/d/ID/preview, ou
    # ?id=ID (links "uc?id=" / "open?id=").
    if partes.path.startswith("/file/d/"):
        candidato = partes.path[len("/file/d/"):].split("/")[0]
    else:
        valores = parse_qs(partes.query).get("id")
        candidato = valores[0] if valores else None

    if not candidato:
        return None
    correspondencia = _REGEX_ID_DRIVE.match(candidato)
    return correspondencia.group(0) if correspondencia else None


def info_embed_video(url: str) -> dict:
    """
    Retorna {"tipo": "youtube"|"drive"|"outro", "embed_url": str|None}.
    "outro" cobre qualquer link de vídeo direto (mp4 etc.) — nesse caso
    embed_url é None e o template usa a própria url original num <video>.
    """
    if not url:
        return {"tipo": "outro", "embed_url": None}

    video_id = _extrair_id_youtube(url)
    if video_id:
        return {"tipo": "youtube", "embed_url": f"https://www.youtube-nocookie.com/embed/{video_id}"}

    drive_id = _extrair_id_drive(url)
    if drive_id:
        return {"tipo": "drive", "embed_url": f"https://drive.google.com/file/d/{drive_id}/preview"}

    return {"tipo": "outro", "embed_url": None}
