"""
Player do YouTube com verificação real de tempo assistido.

Substitui o antigo cronômetro (que só contava o tempo desde que a página
abria, independente do aluno estar de fato vendo o vídeo) por um componente
que embute o player oficial do YouTube e só conta o tempo em que o vídeo
está genuinamente em reprodução — pausar, deixar parado, ou só deixar a
aba aberta em segundo plano não soma mais tempo "assistido".

É um componente "estático" do Streamlit (só um arquivo HTML/JS em
modules/components/youtube_tracker/index.html, sem precisar de build nem
de React) — ver esse arquivo para a implementação do player em si.
"""
import os
import re
from urllib.parse import urlparse, parse_qs

import streamlit.components.v1 as components

_DIR_COMPONENTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components", "youtube_tracker")
_youtube_tracker = components.declare_component("youtube_tracker", path=_DIR_COMPONENTE)


def extrair_video_id_youtube(url: str):
    """
    Extrai o ID do vídeo de uma URL do YouTube, aceitando os formatos mais
    comuns (watch?v=, youtu.be/, embed/, shorts/). Retorna None se a URL
    não for reconhecida como um link do YouTube (nesse caso o chamador deve
    usar st.video() normalmente, sem a verificação real de tempo assistido).
    """
    if not url:
        return None
    try:
        partes = urlparse(url.strip())
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
        elif partes.path.startswith("/embed/"):
            candidato = partes.path.split("/embed/", 1)[1].split("/")[0]
        elif partes.path.startswith("/shorts/"):
            candidato = partes.path.split("/shorts/", 1)[1].split("/")[0]

    # IDs de vídeo do YouTube são sempre 11 caracteres (letras, números, - e _).
    if candidato and re.fullmatch(r"[A-Za-z0-9_-]{11}", candidato):
        return candidato
    return None


def progresso_assistido_youtube(url_video: str, chave: str):
    """
    Renderiza o player e devolve quantos segundos de vídeo já foram
    efetivamente reproduzidos nesta sessão. Retorna None se a URL não for
    do YouTube — nesse caso o chamador deve usar st.video() normalmente.
    """
    video_id = extrair_video_id_youtube(url_video)
    if not video_id:
        return None

    valor = _youtube_tracker(videoId=video_id, key=chave, default=0)
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0
