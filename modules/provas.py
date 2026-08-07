"""
Módulo de Provas/Avaliações.

Renderiza o questionário de múltipla escolha de UM módulo (não mais do
curso inteiro), calcula a nota automaticamente (0 a 10, proporcional aos
acertos) e — se aprovado — desbloqueia o próximo módulo do curso.

É chamado de dentro de modules/cursos.py, embutido na própria tela do
curso, logo abaixo dos vídeos daquele módulo (não é mais uma página à parte).
"""
import time

import streamlit as st

from database.repositorio import (
    listar_perguntas,
    salvar_resultado_prova,
    ultimo_resultado,
)


def renderizar_prova_modulo(aluno_id: str, prova: dict):
    """
    Desenha o formulário da avaliação de um módulo. Cuida sozinho de:
    - Perguntas ainda não cadastradas
    - Trava de tentativa única (só refaz se o admin liberar)
    - Cronometragem do tempo gasto
    Retorna True se o aluno acabou de ser aprovado nesta execução (para o
    chamador saber que precisa recarregar/desbloquear o próximo módulo).
    """
    perguntas = listar_perguntas(prova["id"])
    if not perguntas:
        st.info("Esta avaliação ainda não possui perguntas cadastradas.")
        return False

    resultado_anterior = ultimo_resultado(aluno_id, prova["id"])
    if resultado_anterior and resultado_anterior["aprovado"]:
        st.success(f"✅ Aprovado com nota {resultado_anterior['nota']:.1f}.")
        return False

    if resultado_anterior and not resultado_anterior.get("liberado_para_nova_tentativa"):
        st.error(
            f"Você já enviou esta avaliação e não atingiu a nota mínima "
            f"(sua nota: {resultado_anterior['nota']:.1f} de {prova['nota_minima']:.1f} necessários)."
        )
        st.info(
            "A nota fica registrada e não pode ser refeita livremente. "
            "Se quiser uma nova chance, entre em contato com a equipe responsável — "
            "após uma análise, a avaliação pode ser liberada novamente para você."
        )
        return False

    st.caption(
        f"A avaliação tem {len(perguntas)} pergunta(s). "
        f"Nota mínima para aprovação: {prova['nota_minima']:.1f} de 10."
    )

    # Marca o instante em que o aluno começou esta tentativa (para calcular
    # quanto tempo ele levou até enviar). Só é marcado uma vez por tentativa.
    chave_tempo = f"prova_iniciada_{prova['id']}"
    if chave_tempo not in st.session_state:
        st.session_state[chave_tempo] = time.time()

    respostas_aluno = {}
    with st.form(f"form_prova_{prova['id']}"):
        for i, pergunta in enumerate(perguntas, start=1):
            st.markdown(f"**{i}. {pergunta['enunciado']}**")
            opcoes = {
                "A": pergunta["opcao_a"],
                "B": pergunta["opcao_b"],
                "C": pergunta["opcao_c"],
                "D": pergunta["opcao_d"],
            }
            escolha = st.radio(
                label="Selecione uma alternativa:",
                options=list(opcoes.keys()),
                format_func=lambda letra, opcoes=opcoes: f"{letra}) {opcoes[letra]}",
                key=f"pergunta_{pergunta['id']}",
                index=None,
            )
            respostas_aluno[pergunta["id"]] = escolha
            st.write("")

        enviar = st.form_submit_button("Enviar Avaliação", type="primary", use_container_width=True)

    if not enviar:
        return False

    if any(resposta is None for resposta in respostas_aluno.values()):
        st.warning("Responda todas as perguntas antes de enviar.")
        return False

    acertos = sum(
        1 for pergunta in perguntas
        if respostas_aluno[pergunta["id"]] == pergunta["resposta_correta"]
    )
    nota = round((acertos / len(perguntas)) * 10, 1)
    aprovado = nota >= prova["nota_minima"]

    tempo_gasto = int(time.time() - st.session_state.get(chave_tempo, time.time()))
    st.session_state.pop(chave_tempo, None)  # limpa para a próxima tentativa (se for liberada)

    salvar_resultado_prova(aluno_id, prova["id"], nota, aprovado, tempo_gasto)

    st.divider()
    minutos, segundos = divmod(tempo_gasto, 60)
    st.metric("Sua nota", f"{nota:.1f} / 10", f"{acertos}/{len(perguntas)} acertos")
    st.caption(f"Tempo gasto nesta avaliação: {minutos}min {segundos}s")

    if aprovado:
        st.success("🎉 Parabéns, você foi APROVADO neste módulo!")
        st.balloons()
        return True
    else:
        st.error(
            f"Você não atingiu a nota mínima ({prova['nota_minima']:.1f}). "
            f"Revise as aulas deste módulo e entre em contato para uma nova tentativa."
        )
        return False
