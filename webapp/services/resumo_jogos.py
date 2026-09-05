"""
Resumo de progresso dos 3 simuladores (Campo, Suporte clássico, Suporte
por IA) — usado tanto pela Início (só os números, num card compacto)
quanto pela Sala de Simulação (o card completo de cada um). Ficou
separado de webapp/routers/inicio.py pra não duplicar essa lógica nos
dois lugares.
"""
from database.repositorio import (
    jogo_campo_obter_progresso,
    jogo_suporte_ia_obter_progresso,
    jogo_suporte_obter_progresso,
)
from webapp.data.jogo_campo_missoes import MISSOES as JOGO_MISSOES
from webapp.data.jogo_suporte_atendimentos import ATENDIMENTOS as SUPORTE_ATENDIMENTOS
from webapp.services.jogo_campo import selos_conquistados
from webapp.services.jogo_suporte import selos_conquistados as suporte_selos_conquistados


def resumo_do_jogo(aluno_id: str) -> dict:
    progresso = jogo_campo_obter_progresso(aluno_id)
    total_missoes = len(JOGO_MISSOES)
    return {
        "comecou": progresso["tela"] != "welcome" or progresso["missoes_completadas"] > 0,
        "concluiu_tudo": total_missoes > 0 and progresso["missoes_completadas"] >= total_missoes,
        "missoes_completadas": progresso["missoes_completadas"],
        "total_missoes": total_missoes,
        "quantidade_selos": len(selos_conquistados(progresso["missoes_completadas"])),
    }


def resumo_do_suporte(aluno_id: str) -> dict:
    progresso = jogo_suporte_obter_progresso(aluno_id)
    total_atendimentos = len(SUPORTE_ATENDIMENTOS)
    return {
        "comecou": progresso["tela"] != "welcome" or progresso["atendimentos_completados"] > 0,
        "concluiu_tudo": total_atendimentos > 0 and progresso["atendimentos_completados"] >= total_atendimentos,
        "atendimentos_completados": progresso["atendimentos_completados"],
        "total_atendimentos": total_atendimentos,
        "quantidade_selos": len(suporte_selos_conquistados(progresso["atendimentos_completados"])),
    }


def resumo_do_suporte_ia(aluno_id: str) -> dict:
    """Igual resumo_do_suporte, mas pro modo beta em chat livre com IA
    (webapp/services/jogo_suporte_ia.py) — não tem selo próprio ainda."""
    progresso = jogo_suporte_ia_obter_progresso(aluno_id)
    total_atendimentos = len(SUPORTE_ATENDIMENTOS)
    return {
        "comecou": progresso["tela"] != "welcome" or progresso["atendimentos_completados"] > 0,
        "concluiu_tudo": total_atendimentos > 0 and progresso["atendimentos_completados"] >= total_atendimentos,
        "atendimentos_completados": progresso["atendimentos_completados"],
        "total_atendimentos": total_atendimentos,
    }
