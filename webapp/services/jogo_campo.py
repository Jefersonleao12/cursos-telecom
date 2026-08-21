"""
"Simulador de Campo" — jogo de treinamento com Ordens de Serviço simuladas,
acessado por um card na tela Início. Cada O.S. tem 4 decisões (cenário +
pergunta + 3 alternativas embaralhadas); a cada 5 O.S. concluídas o aluno
ganha um selo, visível no Ranking; ao concluir todas, ganha o selo final.

O conteúdo (webapp/data/jogo_campo_missoes.py) fica separado da lógica de
jogo (aqui) e do progresso (database/repositorio.py: jogo_campo_*) —
adicionar mais O.S. no futuro é só crescer aquela lista, sem mexer aqui.
"""
import random

from database.repositorio import jogo_campo_obter_progresso, jogo_campo_salvar_progresso
from webapp.data.jogo_campo_missoes import MISSOES

_DECISOES_POR_MISSAO = 4  # todas as O.S. do lote atual têm 4 decisões
_SELOS_A_CADA = 5

_NOMES_SELOS = [
    "Selo Aprendiz de Campo",
    "Selo Técnico de Rotina",
    "Selo Técnico Experiente",
    "Selo Técnico Avançado",
    "Selo Técnico Sênior",
    "Selo Especialista de Campo",
    "Selo Referência Técnica",
    "Selo Veterano de Campo",
    "Selo Elite Norte Tel",
    "Selo Lenda de Campo",
]
_ICONES_SELOS = ["🥉", "🥉", "🥈", "🥈", "🥇", "🥇", "🏅", "🏅", "🎖️", "🎖️"]
_SELO_FINAL = {"nome": "Selo Mestre de Campo Norte Tel", "icone": "🏆"}


def _nome_selo(numero_tier: int) -> dict:
    """numero_tier começa em 1 (a cada 5 O.S. concluídas)."""
    indice = numero_tier - 1
    if indice < len(_NOMES_SELOS):
        return {"nome": _NOMES_SELOS[indice], "icone": _ICONES_SELOS[indice]}
    return {"nome": f"Selo de Campo — Nível {numero_tier}", "icone": "🎖️"}


def selos_conquistados(missoes_completadas: int) -> list[dict]:
    """Todos os selos já conquistados até agora (tiers de 5 em 5 + o final, se completou tudo)."""
    total_missoes = len(MISSOES)
    tiers = missoes_completadas // _SELOS_A_CADA
    selos = [_nome_selo(n) for n in range(1, tiers + 1)]
    if total_missoes and missoes_completadas >= total_missoes:
        selos.append(_SELO_FINAL)
    return selos


def _selo_recem_conquistado(missoes_completadas: int):
    """Selo ganho EXATAMENTE nesta O.S. que acabou de fechar (ou None)."""
    total_missoes = len(MISSOES)
    if total_missoes and missoes_completadas == total_missoes:
        return _SELO_FINAL
    if missoes_completadas > 0 and missoes_completadas % _SELOS_A_CADA == 0:
        return _nome_selo(missoes_completadas // _SELOS_A_CADA)
    return None


def _opcoes_embaralhadas(aluno_id: str, missao_index: int, decisao_index: int, opcoes: list) -> list:
    """
    Ordem embaralhada, mas ESTÁVEL: o mesmo aluno vendo a mesma decisão
    sempre vê as alternativas na mesma ordem (senão um F5 na hora de
    responder mudaria a posição debaixo do dedo dele) — mas outro aluno,
    ou a mesma pessoa numa tentativa futura depois de reiniciar, pode ver
    uma ordem diferente, já que o "embaralhar" é um dos pedidos do jogo.
    """
    semente = f"{aluno_id}:{missao_index}:{decisao_index}"
    return random.Random(semente).sample(opcoes, len(opcoes))


def obter_tela(aluno_id: str) -> dict:
    """Monta o contexto pra renderizar a tela atual do jogo desse aluno."""
    progresso = jogo_campo_obter_progresso(aluno_id)
    tela = progresso["tela"]
    total_missoes = len(MISSOES)

    contexto = {
        "tela": tela,
        "xp": progresso["xp"],
        "missao_numero": progresso["missao_index"] + 1,
        "total_missoes": total_missoes,
        "decisao_numero": progresso["decisao_index"] + 1,
        "total_decisoes": _DECISOES_POR_MISSAO,
    }

    if tela in ("mission-intro", "decision", "feedback", "mission-end"):
        contexto["missao"] = MISSOES[progresso["missao_index"]]

    if tela == "decision":
        missao = contexto["missao"]
        decisao = missao["decisoes"][progresso["decisao_index"]]
        contexto["decisao"] = decisao
        contexto["opcoes"] = _opcoes_embaralhadas(
            aluno_id, progresso["missao_index"], progresso["decisao_index"], decisao["opcoes"]
        )

    if tela == "feedback":
        missao = contexto["missao"]
        decisao = missao["decisoes"][progresso["decisao_index"]]
        opcoes = _opcoes_embaralhadas(aluno_id, progresso["missao_index"], progresso["decisao_index"], decisao["opcoes"])
        contexto["opcao_escolhida"] = opcoes[progresso["opcao_escolhida"]]

    if tela == "mission-end":
        acertos = progresso["acertos_missao"]
        contexto["acertos_missao"] = acertos
        contexto["tier"] = _tier_da_missao(acertos)
        contexto["selo_novo"] = _selo_recem_conquistado(progresso["missoes_completadas"])
        contexto["ultima_os"] = progresso["missao_index"] + 1 >= total_missoes

    if tela == "game-end":
        total_decisoes = total_missoes * _DECISOES_POR_MISSAO
        contexto["acertos_totais"] = progresso["acertos_totais"]
        contexto["total_decisoes_jogo"] = total_decisoes
        contexto["selos"] = selos_conquistados(progresso["missoes_completadas"])
        contexto["ranking_tecnico"] = _classificacao_final(progresso["acertos_totais"], total_decisoes)

    return contexto


def _tier_da_missao(acertos: int) -> str:
    if acertos >= _DECISOES_POR_MISSAO:
        return "ideal"
    if acertos == _DECISOES_POR_MISSAO - 1:
        return "aceitavel"
    return "atencao"


_CLASSIFICACOES = [
    (0.9, "Técnico Master", "Nível de quem fecha O.S. sem deixar reincidência. Continue registrando as leituras — é isso que separa um bom técnico de um ótimo."),
    (0.75, "Técnico Sênior", "Bom domínio das situações de campo. Vale revisar o(s) ponto(s) que escorregaram antes do próximo plantão."),
    (0.5, "Técnico Júnior", "Base sólida, mas ainda com alguns chutes no meio do caminho. Releia os feedbacks das questões erradas antes de ir pra rua."),
    (0.0, "Estagiário de Campo", "Ainda dá pra fechar a O.S., mas vale revisar os conceitos com calma antes do próximo atendimento."),
]


def _classificacao_final(acertos_totais: int, total_decisoes: int) -> dict:
    proporcao = (acertos_totais / total_decisoes) if total_decisoes else 0.0
    for limite, titulo, texto in _CLASSIFICACOES:
        if proporcao >= limite:
            return {"titulo": titulo, "texto": texto}
    return {"titulo": _CLASSIFICACOES[-1][1], "texto": _CLASSIFICACOES[-1][2]}


def iniciar_jogo(aluno_id: str):
    """Tela de boas-vindas -> intro da primeira O.S. (não reseta progresso já existente)."""
    progresso = jogo_campo_obter_progresso(aluno_id)
    if progresso["tela"] != "welcome":
        return
    jogo_campo_salvar_progresso(aluno_id, tela="mission-intro", missao_index=0)


def iniciar_missao(aluno_id: str):
    """Intro da O.S. -> primeira decisão."""
    jogo_campo_salvar_progresso(aluno_id, tela="decision", decisao_index=0, acertos_missao=0)


def responder(aluno_id: str, opcao_index: int):
    """Aluno escolheu uma alternativa (posição JÁ na ordem embaralhada) -> tela de feedback."""
    progresso = jogo_campo_obter_progresso(aluno_id)
    missao = MISSOES[progresso["missao_index"]]
    decisao = missao["decisoes"][progresso["decisao_index"]]
    opcoes = _opcoes_embaralhadas(aluno_id, progresso["missao_index"], progresso["decisao_index"], decisao["opcoes"])

    if opcao_index < 0 or opcao_index >= len(opcoes):
        return  # requisição inválida (ex: índice de outra tela) — ignora

    escolhida = opcoes[opcao_index]
    campos = {"tela": "feedback", "opcao_escolhida": opcao_index}
    if escolhida["correta"]:
        campos["acertos_missao"] = progresso["acertos_missao"] + 1
        campos["acertos_totais"] = progresso["acertos_totais"] + 1
        campos["xp"] = progresso["xp"] + 25
    else:
        campos["xp"] = progresso["xp"] + 5
    jogo_campo_salvar_progresso(aluno_id, **campos)


def continuar(aluno_id: str):
    """Sai da tela de feedback -> próxima decisão, ou fecha a O.S. atual."""
    progresso = jogo_campo_obter_progresso(aluno_id)
    missao = MISSOES[progresso["missao_index"]]

    if progresso["decisao_index"] + 1 < len(missao["decisoes"]):
        jogo_campo_salvar_progresso(aluno_id, tela="decision", decisao_index=progresso["decisao_index"] + 1)
        return

    jogo_campo_salvar_progresso(
        aluno_id, tela="mission-end", missoes_completadas=progresso["missoes_completadas"] + 1
    )


def proxima_missao(aluno_id: str):
    """Sai da tela de fim de O.S. -> intro da próxima, ou relatório final do jogo."""
    progresso = jogo_campo_obter_progresso(aluno_id)
    proximo_index = progresso["missao_index"] + 1
    if proximo_index < len(MISSOES):
        jogo_campo_salvar_progresso(aluno_id, tela="mission-intro", missao_index=proximo_index)
    else:
        jogo_campo_salvar_progresso(aluno_id, tela="game-end")


def reiniciar(aluno_id: str):
    """
    Zera o jogo do aluno pra jogar de novo, e volta pra tela de boas-vindas.
    NÃO mexe em missoes_completadas: os selos já são permanentes (aparecem
    no Ranking), rejogar não pode fazer o aluno "perder" uma conquista.
    """
    jogo_campo_salvar_progresso(
        aluno_id,
        tela="welcome", missao_index=0, decisao_index=0, acertos_missao=0,
        acertos_totais=0, xp=0, opcao_escolhida=None,
    )
