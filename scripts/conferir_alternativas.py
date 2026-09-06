"""Mede se as alternativas dos simuladores entregam a resposta de graça.

Rode sempre que adicionar ou editar casos do Simulador de Campo ou do
Simulador de Suporte:

    python3 scripts/conferir_alternativas.py

Três atalhos já foram encontrados e corrigidos nesses dados, e todos voltam
com facilidade quando se escreve um caso novo às pressas:

1. POSIÇÃO — a correta ficava sempre em primeiro lugar. Hoje o embaralhamento
   por aluno resolve isso na hora de exibir, então aqui não há o que medir.
2. TAMANHO — a correta era a mais longa em quase todas as decisões, e dava
   pra gabaritar escolhendo a opção mais comprida sem ler nenhuma. O alvo é
   o acaso puro (uma em três); o aceitável vai de 20% a 55%. O piso importa
   tanto quanto o teto: se a mais longa NUNCA fosse a certa, bastaria
   descartá-la pra ficar com 50% de chance.
3. FECHO REPETIDO — quando um mesmo trecho de texto aparece só em alternativa
   errada, ele vira marca de gabarito. Qualquer frase final que se repita
   três vezes ou mais e nunca apareça numa correta é sinalizada aqui.

O script não altera nada: só imprime o diagnóstico e devolve código de saída
diferente de zero se algum limite estourar.
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from webapp.data.jogo_campo_missoes import MISSOES
from webapp.data.jogo_suporte_atendimentos import ATENDIMENTOS

PISO, TETO = 0.20, 0.55
MIN_REPETICOES_FECHO = 3


def _decisoes(casos):
    for caso in casos:
        for indice, decisao in enumerate(caso["decisoes"]):
            yield caso["id"], indice, decisao


def _partes(decisao):
    correta = next(o for o in decisao["opcoes"] if o.get("correta"))
    erradas = [o for o in decisao["opcoes"] if not o.get("correta")]
    return correta, erradas


def conferir_tamanho(nome, casos):
    mais_longa = []
    total = 0
    for id_caso, indice, decisao in _decisoes(casos):
        correta, erradas = _partes(decisao)
        total += 1
        if len(correta["texto"]) >= max(len(o["texto"]) for o in erradas):
            mais_longa.append(f"{id_caso} d{indice}")

    fracao = len(mais_longa) / total
    print(f"{nome}: {total} decisões — a correta é a mais longa em "
          f"{len(mais_longa)} ({fracao:.0%}); a faixa aceitável é "
          f"{PISO:.0%} a {TETO:.0%}")
    if fracao > TETO:
        print("  !! acima do teto: alongue o distrator mais forte de algumas decisões")
        return False
    if fracao < PISO:
        print("  !! abaixo do piso: 'a mais longa nunca é a certa' também é dica")
        return False
    return True


def conferir_fechos(nome, casos):
    """Procura frases finais que só aparecem em alternativa errada."""
    def ultima_frase(texto):
        partes = re.split(r"(?<=[.!?])\s+", texto.strip())
        return partes[-1] if partes else ""

    em_erradas, em_corretas = Counter(), Counter()
    for _, _, decisao in _decisoes(casos):
        correta, erradas = _partes(decisao)
        em_corretas[ultima_frase(correta["texto"])] += 1
        for o in erradas:
            em_erradas[ultima_frase(o["texto"])] += 1

    marcas = [(frase, n) for frase, n in em_erradas.items()
              if n >= MIN_REPETICOES_FECHO and not em_corretas[frase]]
    if not marcas:
        print(f"{nome}: nenhum fecho repetido marcando alternativa errada")
        return True
    print(f"{nome}: !! {len(marcas)} fecho(s) aparecem só em alternativa errada")
    for frase, n in sorted(marcas, key=lambda p: -p[1]):
        print(f"     {n}x  {frase[:80]}")
    return False


def main():
    ok = True
    for nome, casos in (("Campo", MISSOES), ("Suporte", ATENDIMENTOS)):
        ok &= conferir_tamanho(nome, casos)
        ok &= conferir_fechos(nome, casos)
    print("\nTudo dentro do esperado." if ok else "\nHá atalhos a corrigir.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
