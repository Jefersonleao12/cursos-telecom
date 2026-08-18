"""
Calcula o estado de desbloqueio de módulos/aulas de um curso e o "gate" de
tempo mínimo assistido de uma aula — porta a lógica de
modules/cursos.py:tela_detalhe_curso() e _bloco_aula(), separada da
renderização (aqui só devolve dados; quem desenha é o router + template).
"""
from datetime import datetime, timezone

from database.repositorio import (
    aulas_concluidas_do_modulo,
    buscar_prova_do_modulo,
    buscar_progresso_aula,
    listar_aulas_do_modulo,
    listar_modulos_do_curso,
    listar_perguntas,
    modulo_esta_completo,
    registrar_inicio_aula,
    ultimo_resultado,
)


def calcular_estado_curso(aluno_id: str, curso_id: int) -> list[dict]:
    """
    Um item por módulo do curso, na ordem, com o desbloqueio sequencial já
    calculado: um módulo só é 'desbloqueado' se o anterior estiver
    completo, e dentro dele cada aula só é 'desbloqueada' se a anterior já
    tiver sido concluída.
    """
    modulos = listar_modulos_do_curso(curso_id)
    resultado = []
    modulo_anterior_completo = True

    for indice, modulo in enumerate(modulos, start=1):
        desbloqueado = modulo_anterior_completo
        completo = modulo_esta_completo(aluno_id, modulo["id"]) if desbloqueado else False

        aulas_estado = []
        todas_aulas_concluidas = False
        prova = None
        perguntas_prova = []
        resultado_prova = None

        if desbloqueado:
            aulas = listar_aulas_do_modulo(modulo["id"])
            concluidas_modulo = set(aulas_concluidas_do_modulo(aluno_id, modulo["id"]))
            aula_anterior_concluida = True
            for aula in aulas:
                aula_concluida = aula["id"] in concluidas_modulo
                aulas_estado.append(
                    {"aula": aula, "concluida": aula_concluida, "desbloqueada": aula_anterior_concluida}
                )
                aula_anterior_concluida = aula_concluida

            todas_aulas_concluidas = bool(aulas_estado) and all(a["concluida"] for a in aulas_estado)
            if todas_aulas_concluidas:
                prova = buscar_prova_do_modulo(modulo["id"])
                if prova:
                    perguntas_prova = listar_perguntas(prova["id"])
                    resultado_prova = ultimo_resultado(aluno_id, prova["id"])

        resultado.append(
            {
                "indice": indice,
                "modulo": modulo,
                "desbloqueado": desbloqueado,
                "completo": completo,
                "aulas": aulas_estado,
                "todas_aulas_concluidas": todas_aulas_concluidas,
                "prova": prova,
                "perguntas_prova": perguntas_prova,
                "resultado_prova": resultado_prova,
            }
        )
        modulo_anterior_completo = completo

    return resultado


def calcular_gate_video(aluno_id: str, aula: dict) -> int:
    """
    Garante que o cronômetro desta aula já começou a contar (no servidor,
    não no navegador do aluno) e devolve quantos segundos ainda faltam
    antes de liberar o botão "concluir" — 0 já significa liberado.
    """
    registrar_inicio_aula(aluno_id, aula["id"])

    duracao_min = aula.get("duracao_minutos") or 0
    segundos_exigidos = int(duracao_min * 60 * 0.9)
    if segundos_exigidos <= 0:
        return 0

    progresso = buscar_progresso_aula(aluno_id, aula["id"])
    iniciada_em = progresso.get("iniciada_em") if progresso else None
    if not iniciada_em:
        return segundos_exigidos

    inicio = datetime.fromisoformat(iniciada_em.replace("Z", "+00:00"))
    decorridos = (datetime.now(timezone.utc) - inicio).total_seconds()
    faltam = segundos_exigidos - decorridos
    return max(0, round(faltam))


def pode_concluir_aula(aluno_id: str, aula: dict) -> bool:
    """
    Confere se o aluno já pode marcar esta aula como concluída — chamada
    de novo, no SERVIDOR, no momento de processar o POST (não basta o
    botão ter aparecido liberado na tela, que só reflete o estado de
    alguns segundos atrás).
    """
    return calcular_gate_video(aluno_id, aula) <= 0
