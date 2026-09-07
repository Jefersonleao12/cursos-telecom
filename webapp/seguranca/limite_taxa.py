"""
Limite de tentativas (rate limit) em memória.

Por que em memória e não em Redis: a plataforma roda num processo único de
propósito (ver o comentário do systemd em scripts/setup-vps.sh — o cache de
consultas só é invalidado dentro do processo que escreve). Como só existe um
processo, um contador em memória vê TODAS as tentativas e é suficiente. Se um
dia a app passar a rodar com vários workers, este módulo precisa migrar pro
mesmo Redis do cache, senão o limite passa a valer por processo e o atacante
ganha N vezes mais tentativas.

O que este módulo protege:

- Login. Sem ele, a senha inicial de todo aluno é o próprio CPF, e o CPF é
  também o nome de usuário: quem tiver uma lista de CPFs da empresa entra em
  qualquer conta que ainda não trocou a senha, testando à vontade.
- "Esqueci minha senha". Sem ele, dá pra disparar WhatsApp pro administrador
  em looping e queimar a cota da API.
- Chat do Simulador por IA. Cada mensagem é uma chamada paga ao Gemini.

Duas contagens andam juntas, porque protegem de coisas diferentes:

- por CHAVE (o CPF, o id do aluno): impede insistir numa conta específica.
- por IP: impede varrer muitas contas diferentes a partir do mesmo lugar,
  que passaria despercebido pela contagem por chave.
"""
import threading
import time
from collections import deque
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Politica:
    """Quantas tentativas cabem na janela, e por quanto tempo bloqueia depois."""
    tentativas: int
    janela_segundos: int
    bloqueio_segundos: int


# Cinco erros seguidos numa mesma conta já é muito para quem sabe a própria
# senha, e é pouquíssimo para quem está adivinhando. Quinze minutos de espera
# derrubam a velocidade de um ataque de milhares de tentativas por minuto para
# vinte por hora, sem incomodar quem só errou de verdade.
LOGIN_POR_CPF = Politica(tentativas=5, janela_segundos=15 * 60, bloqueio_segundos=15 * 60)

# O limite por IP é mais folgado porque uma filial inteira pode sair pelo mesmo
# endereço — mas ainda corta a varredura de muitos CPFs a partir de um ponto só.
LOGIN_POR_IP = Politica(tentativas=30, janela_segundos=15 * 60, bloqueio_segundos=15 * 60)

# Redefinição de senha aciona WhatsApp para o administrador: poucos por hora.
REDEFINICAO_POR_CPF = Politica(tentativas=3, janela_segundos=60 * 60, bloqueio_segundos=60 * 60)
REDEFINICAO_POR_IP = Politica(tentativas=10, janela_segundos=60 * 60, bloqueio_segundos=60 * 60)

# Cada mensagem do chat com IA é uma chamada paga. Um atendimento inteiro cabe
# de sobra em 40 mensagens; acima disso é script, não aluno.
IA_POR_ALUNO = Politica(tentativas=40, janela_segundos=10 * 60, bloqueio_segundos=10 * 60)

# Teto de chaves guardadas. Sem isso, quem manda CPFs aleatórios em massa faz o
# próprio contador consumir a memória do servidor — a proteção viraria o ataque.
_MAX_CHAVES = 20_000


@dataclass
class _Registro:
    carimbos: deque = field(default_factory=deque)
    bloqueado_ate: float = 0.0


class ControleDeTentativas:
    """Contador de tentativas por chave, com bloqueio temporário."""

    def __init__(self, politica: Politica, nome: str):
        self.politica = politica
        self.nome = nome
        self._registros: dict[str, _Registro] = {}
        self._trava = threading.Lock()

    # -- consulta ---------------------------------------------------------
    def segundos_de_bloqueio(self, chave: str) -> int:
        """0 se pode tentar; senão, quantos segundos ainda faltam."""
        agora = time.monotonic()
        with self._trava:
            registro = self._registros.get(chave)
            if registro is None or registro.bloqueado_ate <= agora:
                return 0
            return int(registro.bloqueado_ate - agora) + 1

    # -- escrita ----------------------------------------------------------
    def registrar_falha(self, chave: str) -> int:
        """Conta mais uma tentativa frustrada. Devolve os segundos de bloqueio
        resultantes (0 se ainda há tentativas sobrando)."""
        agora = time.monotonic()
        limite_janela = agora - self.politica.janela_segundos
        with self._trava:
            self._limpar_expirados(agora)
            registro = self._registros.setdefault(chave, _Registro())
            while registro.carimbos and registro.carimbos[0] < limite_janela:
                registro.carimbos.popleft()
            registro.carimbos.append(agora)
            if len(registro.carimbos) >= self.politica.tentativas:
                registro.bloqueado_ate = agora + self.politica.bloqueio_segundos
                registro.carimbos.clear()
                return self.politica.bloqueio_segundos
            return 0

    def registrar_sucesso(self, chave: str) -> None:
        """Zera o histórico da chave — quem acertou a senha não deve carregar
        os erros de digitação de antes."""
        with self._trava:
            self._registros.pop(chave, None)

    # -- manutenção -------------------------------------------------------
    def _limpar_expirados(self, agora: float) -> None:
        """Descarta chaves que não têm mais nada a dizer. Chamado a cada falha,
        que é justamente quando o dicionário cresce."""
        if len(self._registros) < _MAX_CHAVES:
            return
        limite_janela = agora - self.politica.janela_segundos
        mortas = [
            chave for chave, reg in self._registros.items()
            if reg.bloqueado_ate <= agora and (not reg.carimbos or reg.carimbos[-1] < limite_janela)
        ]
        for chave in mortas:
            del self._registros[chave]
        # Ainda cheio depois da limpeza: é ataque de volume. Prefere-se perder
        # o histórico mais antigo a deixar a memória crescer sem limite.
        if len(self._registros) >= _MAX_CHAVES:
            excedente = len(self._registros) - _MAX_CHAVES // 2
            for chave in list(self._registros)[:excedente]:
                del self._registros[chave]


login_por_cpf = ControleDeTentativas(LOGIN_POR_CPF, "login/cpf")
login_por_ip = ControleDeTentativas(LOGIN_POR_IP, "login/ip")
redefinicao_por_cpf = ControleDeTentativas(REDEFINICAO_POR_CPF, "redefinicao/cpf")
redefinicao_por_ip = ControleDeTentativas(REDEFINICAO_POR_IP, "redefinicao/ip")
ia_por_aluno = ControleDeTentativas(IA_POR_ALUNO, "ia/aluno")


def texto_de_espera(segundos: int) -> str:
    """Formata o tempo restante do jeito que se fala, para a mensagem de tela."""
    if segundos >= 90:
        minutos = (segundos + 59) // 60
        return f"{minutos} minutos"
    if segundos > 60:
        return "1 minuto"
    return f"{max(segundos, 1)} segundos"
