"""
De onde veio a requisição.

A app não fica exposta na internet: quem atende as portas 80/443 é o Caddy,
que repassa para 127.0.0.1 (ver scripts/setup-vps.sh). Por isso
`request.client.host` é sempre "127.0.0.1" — inútil para limitar por origem.
O endereço real do visitante chega no cabeçalho X-Forwarded-For, escrito pelo
Caddy.

Só que cabeçalho é texto que qualquer cliente pode inventar. Se a app
acreditasse nele sempre, bastaria mandar um X-Forwarded-For diferente a cada
tentativa para o limite por IP virar enfeite. A regra aqui é: acredita no
cabeçalho apenas quando quem entregou a conexão é o proxy local; vindo de
qualquer outro lugar, vale o endereço real do socket.
"""
import ipaddress

from starlette.requests import Request

_CABECALHO = "x-forwarded-for"


def _e_local(endereco: str) -> bool:
    try:
        ip = ipaddress.ip_address(endereco)
    except ValueError:
        return False
    return ip.is_loopback


def ip_do_cliente(request: Request) -> str:
    """Endereço a usar nas contagens por origem. Nunca devolve vazio, para não
    juntar todo mundo numa mesma chave por acidente."""
    peer = request.client.host if request.client else ""

    if peer and _e_local(peer):
        encaminhado = request.headers.get(_CABECALHO, "")
        if encaminhado:
            # O Caddy acrescenta o cliente real no fim da lista; os valores
            # anteriores podem ter vindo do próprio cliente e não valem nada.
            candidato = encaminhado.split(",")[-1].strip()
            try:
                ipaddress.ip_address(candidato)
            except ValueError:
                pass
            else:
                return candidato

    return peer or "desconhecido"
