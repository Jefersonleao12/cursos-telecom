"""Instância única do Jinja2Templates, compartilhada por todos os routers."""
import hashlib
import os
from pathlib import Path

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="webapp/templates")


def _versao_estatica() -> str:
    """Identificador curto que muda sempre que o CSS/JS do site muda.

    Vai no fim das URLs de /static (`?v=...`) pra podermos mandar o navegador
    guardar esses arquivos por um ano inteiro sem risco: quando a gente
    publica uma versão nova, a URL muda junto e o navegador baixa de novo
    sozinho. Sem isso, ou o aluno rebaixa tudo a cada página (lento), ou fica
    preso numa versão antiga depois de um deploy (quebrado).
    """
    marca = hashlib.sha256()
    for caminho in sorted(Path("static").rglob("*")):
        if caminho.suffix in {".css", ".js"} and caminho.is_file():
            marca.update(caminho.name.encode())
            marca.update(str(caminho.stat().st_mtime_ns).encode())
    return marca.hexdigest()[:10]


VERSAO_ESTATICA = os.getenv("VERSAO_ESTATICA") or _versao_estatica()

templates.env.globals["versao_estatica"] = VERSAO_ESTATICA
