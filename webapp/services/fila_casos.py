"""Ordem em que cada aluno recebe os casos dos simuladores.

Antes os três simuladores entregavam os casos sempre na mesma ordem, igual
pra todo mundo. Na prática isso vira gabarito passado de boca em boca: quem
faz primeiro conta pro colega qual é a resposta da O.S. 1, da 2, da 3...
Agora cada aluno recebe a sua própria ordem, sorteada.

Duas garantias importantes:

1) A ordem é SORTEADA, mas FIXA pra cada aluno. Ela é gravada junto com o
   progresso na primeira vez, então o aluno pode fechar e voltar depois que
   continua exatamente de onde parou — não é um sorteio novo a cada tela.

2) Conteúdo novo não bagunça quem já começou. Quando você cadastra casos
   novos, eles entram no FIM da fila de quem já está jogando (ver
   fila_completa), em ordem sorteada entre si. Sem isso, um caso novo
   entrando no meio empurraria os outros e o aluno acabaria repetindo um
   caso já feito ou pulando um que ainda não viu.
"""
import hashlib
import random


def _sorteio_do_aluno(aluno_id: str, marca: str) -> random.Random:
    """Sorteador próprio de cada aluno, sempre igual pra ele.

    Usa o id do aluno (e o nome do simulador) como semente, então o mesmo
    aluno recebe sempre a mesma sequência — mesmo que o servidor reinicie.
    """
    semente = hashlib.sha256(f"{marca}:{aluno_id}".encode()).hexdigest()
    return random.Random(int(semente[:16], 16))


def nova_fila(aluno_id: str, total: int, marca: str) -> list:
    """Ordem sorteada dos casos pra este aluno, do primeiro ao último.

    Sorteada a partir do id do aluno, então dá sempre o mesmo resultado. É
    usada como rede de segurança pra quem já estava jogando antes de existir
    fila guardada: sem ela, cada abertura de tela devolveria uma ordem
    diferente e o aluno veria um caso diferente a cada clique.
    """
    indices = list(range(total))
    _sorteio_do_aluno(aluno_id, marca).shuffle(indices)
    return indices


def nova_fila_sorteada(total: int) -> list:
    """Ordem realmente sorteada na hora, sem depender do aluno.

    Usada quando o aluno COMEÇA (ou recomeça) um simulador: o resultado é
    gravado junto com o progresso, então não muda mais durante a partida —
    mas quem jogar de novo pega uma sequência diferente da anterior.
    """
    indices = list(range(total))
    random.shuffle(indices)
    return indices


def fila_completa(fila, aluno_id: str, total: int, marca: str) -> list:
    """A fila guardada do aluno, já contando os casos cadastrados depois.

    - Sem fila guardada (aluno começando agora): sorteia uma nova.
    - Com fila guardada: mantém ela intacta e acrescenta no fim, também
      sorteados, os casos que ainda não estão nela.
    - Ignora índices que não existem mais (caso um dia um caso seja removido).
    """
    if not fila:
        return nova_fila(aluno_id, total, marca)

    fila = [i for i in fila if 0 <= i < total]
    faltando = [i for i in range(total) if i not in set(fila)]
    if faltando:
        _sorteio_do_aluno(aluno_id, f"{marca}:extras").shuffle(faltando)
        fila = fila + faltando
    return fila
