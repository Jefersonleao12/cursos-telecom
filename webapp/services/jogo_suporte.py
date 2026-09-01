"""
"Simulador de Suporte" — jogo de treinamento de atendimento ao cliente
(irmão do Simulador de Campo). Cada atendimento tem uma ou mais decisões
(fala do cliente + 3 respostas possíveis, uma correta) — a quantidade
varia por atendimento, ver webapp/data/jogo_suporte_atendimentos.py; a
cada 5 atendimentos concluídos o aluno ganha um selo, visível no Ranking;
ao concluir todos, ganha o selo final.

Diferente do Simulador de Campo, aqui existe um medidor de humor do
cliente: cada resposta escolhida soma ou subtrai pontos de humor
(0-100), começando no humor_inicial do atendimento. O humor não muda a
pontuação (XP já é decidido pela resposta ser certa ou errada) — é um
indicador visual de como o atendimento está indo, e vira parte do
relatório final do atendimento.

O conteúdo (webapp/data/jogo_suporte_atendimentos.py) fica separado da
lógica de jogo (aqui) e do progresso (database/repositorio.py:
jogo_suporte_*) — adicionar mais atendimentos no futuro é só crescer
aquela lista, sem mexer aqui.
"""
import random

from database.repositorio import jogo_suporte_obter_progresso, jogo_suporte_salvar_progresso
from webapp.data.jogo_suporte_atendimentos import ATENDIMENTOS

_SELOS_A_CADA = 5
_HUMOR_MIN = 0
_HUMOR_MAX = 100

_NOMES_SELOS = [
    "Selo Aprendiz de Atendimento",
    "Selo Atendente de Rotina",
    "Selo Atendente Experiente",
    "Selo Atendente Avançado",
    "Selo Atendente Sênior",
    "Selo Especialista em Suporte",
    "Selo Referência em Atendimento",
    "Selo Veterano de Suporte",
    "Selo Elite Norte Tel",
    "Selo Lenda do Suporte",
]
_ICONES_SELOS = ["🥉", "🥉", "🥈", "🥈", "🥇", "🥇", "🏅", "🏅", "🎖️", "🎖️"]
_SELO_FINAL = {"nome": "Selo Mestre de Atendimento Norte Tel", "icone": "🏆"}


def _nome_selo(numero_tier: int) -> dict:
    """numero_tier começa em 1 (a cada 5 atendimentos concluídos)."""
    indice = numero_tier - 1
    if indice < len(_NOMES_SELOS):
        return {"nome": _NOMES_SELOS[indice], "icone": _ICONES_SELOS[indice]}
    return {"nome": f"Selo de Suporte — Nível {numero_tier}", "icone": "🎖️"}


def selos_conquistados(atendimentos_completados: int) -> list[dict]:
    """Todos os selos já conquistados até agora (tiers de 5 em 5 + o final, se completou tudo)."""
    total_atendimentos = len(ATENDIMENTOS)
    tiers = atendimentos_completados // _SELOS_A_CADA
    selos = [_nome_selo(n) for n in range(1, tiers + 1)]
    if total_atendimentos and atendimentos_completados >= total_atendimentos:
        selos.append(_SELO_FINAL)
    return selos


def _selo_recem_conquistado(atendimentos_completados: int):
    """Selo ganho EXATAMENTE neste atendimento que acabou de fechar (ou None)."""
    total_atendimentos = len(ATENDIMENTOS)
    if total_atendimentos and atendimentos_completados == total_atendimentos:
        return _SELO_FINAL
    if atendimentos_completados > 0 and atendimentos_completados % _SELOS_A_CADA == 0:
        return _nome_selo(atendimentos_completados // _SELOS_A_CADA)
    return None


def _opcoes_embaralhadas(aluno_id: str, atendimento_index: int, decisao_index: int, opcoes: list) -> list:
    """Ordem embaralhada, mas ESTÁVEL por aluno+atendimento+decisão (ver mesma lógica no Simulador de Campo)."""
    semente = f"{aluno_id}:suporte:{atendimento_index}:{decisao_index}"
    return random.Random(semente).sample(opcoes, len(opcoes))


def _atendimento_atual(progresso: dict) -> dict:
    return ATENDIMENTOS[progresso["atendimento_index"]]


def _tier_humor(humor: int) -> str:
    if humor >= 70:
        return "satisfeito"
    if humor >= 40:
        return "neutro"
    return "insatisfeito"


def obter_tela(aluno_id: str) -> dict:
    """Monta o contexto pra renderizar a tela atual do jogo desse aluno."""
    progresso = jogo_suporte_obter_progresso(aluno_id)
    tela = progresso["tela"]
    total_atendimentos = len(ATENDIMENTOS)

    contexto = {
        "tela": tela,
        "xp": progresso["xp"],
        "atendimento_numero": progresso["atendimento_index"] + 1,
        "total_atendimentos": total_atendimentos,
        "decisao_numero": progresso["decisao_index"] + 1,
        "humor_atual": progresso["humor_atual"],
        "humor_tier": _tier_humor(progresso["humor_atual"]),
    }

    if tela in ("atendimento-intro", "decision", "feedback", "atendimento-end"):
        contexto["atendimento"] = _atendimento_atual(progresso)
        contexto["total_decisoes"] = len(contexto["atendimento"]["decisoes"])

    if tela == "decision":
        atendimento = contexto["atendimento"]
        decisao = atendimento["decisoes"][progresso["decisao_index"]]
        contexto["decisao"] = decisao
        contexto["opcoes"] = _opcoes_embaralhadas(aluno_id, progresso["atendimento_index"], progresso["decisao_index"], decisao["opcoes"])

    if tela == "feedback":
        atendimento = contexto["atendimento"]
        decisao = atendimento["decisoes"][progresso["decisao_index"]]
        contexto["decisao"] = decisao
        opcoes = _opcoes_embaralhadas(aluno_id, progresso["atendimento_index"], progresso["decisao_index"], decisao["opcoes"])
        contexto["opcao_escolhida"] = opcoes[progresso["opcao_escolhida"]]

    if tela == "atendimento-end":
        contexto["acertos_atendimento"] = progresso["acertos_atendimento"]
        contexto["tier"] = _tier_humor(progresso["humor_atual"])
        contexto["selo_novo"] = _selo_recem_conquistado(progresso["atendimentos_completados"])
        contexto["ultimo_atendimento"] = progresso["atendimento_index"] + 1 >= total_atendimentos

    if tela == "game-end":
        total_decisoes = sum(len(a["decisoes"]) for a in ATENDIMENTOS)
        contexto["acertos_totais"] = progresso["acertos_totais"]
        contexto["total_decisoes_jogo"] = total_decisoes
        contexto["selos"] = selos_conquistados(progresso["atendimentos_completados"])
        contexto["classificacao_final"] = _classificacao_final(progresso["acertos_totais"], total_decisoes)

    return contexto


_CLASSIFICACOES = [
    (0.9, "Atendente Master", "Nível de quem resolve e ainda deixa o cliente satisfeito. Continue lendo a situação de cada cliente antes de responder — é isso que separa um bom atendente de um ótimo."),
    (0.75, "Atendente Sênior", "Bom domínio das situações de atendimento. Vale revisar o(s) ponto(s) que escorregaram antes do próximo plantão."),
    (0.5, "Atendente Júnior", "Base sólida, mas ainda com algumas respostas no impulso. Releia os feedbacks das questões erradas antes do próximo atendimento."),
    (0.0, "Estagiário de Suporte", "Ainda dá pra fechar o atendimento, mas vale revisar os conceitos com calma antes do próximo chamado."),
]


def _classificacao_final(acertos_totais: int, total_decisoes: int) -> dict:
    proporcao = (acertos_totais / total_decisoes) if total_decisoes else 0.0
    for limite, titulo, texto in _CLASSIFICACOES:
        if proporcao >= limite:
            return {"titulo": titulo, "texto": texto}
    return {"titulo": _CLASSIFICACOES[-1][1], "texto": _CLASSIFICACOES[-1][2]}


def _entrar_em_atendimento(aluno_id: str, atendimento_index: int):
    """Prepara o progresso do aluno pra tela de intro de um atendimento novo."""
    atendimento = ATENDIMENTOS[atendimento_index]
    jogo_suporte_salvar_progresso(
        aluno_id,
        tela="atendimento-intro",
        atendimento_index=atendimento_index,
        decisao_index=0,
        acertos_atendimento=0,
        humor_atual=atendimento["humor_inicial"],
    )


def iniciar_jogo(aluno_id: str):
    """Tela de boas-vindas -> intro do primeiro atendimento (não reseta progresso já existente)."""
    progresso = jogo_suporte_obter_progresso(aluno_id)
    if progresso["tela"] != "welcome":
        return
    _entrar_em_atendimento(aluno_id, atendimento_index=0)


def iniciar_atendimento(aluno_id: str):
    """Intro do atendimento -> primeira decisão (o aluno 'assume' o chat)."""
    jogo_suporte_salvar_progresso(aluno_id, tela="decision", decisao_index=0, acertos_atendimento=0)


def responder(aluno_id: str, opcao_index: int):
    """Aluno escolheu uma alternativa (posição JÁ na ordem embaralhada) -> tela de feedback."""
    progresso = jogo_suporte_obter_progresso(aluno_id)
    atendimento = _atendimento_atual(progresso)
    decisao = atendimento["decisoes"][progresso["decisao_index"]]
    opcoes = _opcoes_embaralhadas(aluno_id, progresso["atendimento_index"], progresso["decisao_index"], decisao["opcoes"])

    if opcao_index < 0 or opcao_index >= len(opcoes):
        return  # requisição inválida (ex: índice de outra tela) — ignora

    escolhida = opcoes[opcao_index]
    novo_humor = max(_HUMOR_MIN, min(_HUMOR_MAX, progresso["humor_atual"] + escolhida["humor_delta"]))
    campos = {"tela": "feedback", "opcao_escolhida": opcao_index, "humor_atual": novo_humor}
    if escolhida["correta"]:
        campos["acertos_atendimento"] = progresso["acertos_atendimento"] + 1
        campos["acertos_totais"] = progresso["acertos_totais"] + 1
        campos["xp"] = progresso["xp"] + 25
    else:
        campos["xp"] = progresso["xp"] + 5
    jogo_suporte_salvar_progresso(aluno_id, **campos)


def continuar(aluno_id: str):
    """Sai da tela de feedback -> próxima decisão, ou fecha o atendimento atual."""
    progresso = jogo_suporte_obter_progresso(aluno_id)
    atendimento = _atendimento_atual(progresso)

    if progresso["decisao_index"] + 1 < len(atendimento["decisoes"]):
        jogo_suporte_salvar_progresso(aluno_id, tela="decision", decisao_index=progresso["decisao_index"] + 1)
        return

    jogo_suporte_salvar_progresso(
        aluno_id,
        tela="atendimento-end",
        atendimentos_completados=progresso["atendimentos_completados"] + 1,
    )


def proximo_atendimento(aluno_id: str):
    """Sai da tela de fim de atendimento -> intro do próximo, ou relatório final do jogo."""
    progresso = jogo_suporte_obter_progresso(aluno_id)
    proximo_index = progresso["atendimento_index"] + 1
    if proximo_index < len(ATENDIMENTOS):
        _entrar_em_atendimento(aluno_id, proximo_index)
    else:
        jogo_suporte_salvar_progresso(aluno_id, tela="game-end")


def reiniciar(aluno_id: str):
    """
    Zera o jogo do aluno pra jogar de novo, e volta pra tela de boas-vindas.
    NÃO mexe em atendimentos_completados: os selos já são permanentes
    (aparecem no Ranking), rejogar não pode fazer o aluno "perder" uma conquista.
    """
    jogo_suporte_salvar_progresso(
        aluno_id,
        tela="welcome", atendimento_index=0, decisao_index=0, acertos_atendimento=0,
        acertos_totais=0, xp=0, humor_atual=50, opcao_escolhida=None,
    )
