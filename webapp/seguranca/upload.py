"""
Leitura segura de arquivo enviado pelo aluno.

`await arquivo.read()` puxa o arquivo inteiro para a memória de uma vez. Como
a plataforma roda num processo único (ver scripts/setup-vps.sh), um envio de
algumas centenas de megabytes derruba o serviço para todo mundo ao mesmo tempo
— e não é preciso ser mal-intencionado para isso: basta um celular novo com
foto em resolução máxima e uma conexão ruim.

Aqui o arquivo é lido em pedaços e a leitura para assim que passa do limite,
sem nunca acumular mais do que o permitido na memória.
"""
from fastapi import UploadFile

# Foto de perfil vira um quadrado de 400x400 no fim do processo; 8 MB cobre com
# folga qualquer foto de celular, inclusive HEIC.
LIMITE_FOTO_BYTES = 8 * 1024 * 1024

_PEDACO = 64 * 1024


class ArquivoGrandeDemaisError(Exception):
    """Envio acima do limite. Vira mensagem de tela, não erro 500."""


def _texto_do_limite(limite: int) -> str:
    return f"{limite // (1024 * 1024)} MB"


async def ler_upload_limitado(arquivo: UploadFile, limite: int = LIMITE_FOTO_BYTES) -> bytes:
    """Lê o arquivo até o limite. Passou disso, levanta ArquivoGrandeDemaisError.

    O `content-length` da requisição não serve como defesa: quem está atacando
    escolhe o que escrever nele. A conta é feita sobre o que realmente chega.
    """
    pedacos: list[bytes] = []
    total = 0
    while True:
        pedaco = await arquivo.read(_PEDACO)
        if not pedaco:
            break
        total += len(pedaco)
        if total > limite:
            raise ArquivoGrandeDemaisError(
                f"A imagem passou de {_texto_do_limite(limite)}. "
                "Escolha uma foto menor ou reduza a resolução."
            )
        pedacos.append(pedaco)
    return b"".join(pedacos)
