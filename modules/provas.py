"""
Módulo de Provas/Avaliações.

Aplica o questionário de múltipla escolha, calcula a nota automaticamente
(0 a 10, proporcional aos acertos) e libera a emissão do certificado em
caso de aprovação.
"""
import streamlit as st

from database.repositorio import (
    buscar_curso,
    buscar_prova_do_curso,
    listar_perguntas,
    salvar_resultado_prova,
    melhor_resultado,
    calcular_progresso_curso,
)


def tela_prova():
    curso_id = st.session_state.get("curso_atual_id")
    curso = buscar_curso(curso_id)
    aluno_id = st.session_state["aluno_id"]

    if st.button("← Voltar para o curso"):
        st.session_state["pagina_atual"] = "detalhe_curso"
        st.rerun()

    st.title(f"📝 Avaliação: {curso['titulo']}")

    progresso = calcular_progresso_curso(aluno_id, curso_id)
    if progresso < 1.0:
        st.warning("Você precisa concluir todas as aulas do curso antes de fazer a avaliação.")
        return

    prova = buscar_prova_do_curso(curso_id)
    if prova is None:
        st.info("Este curso ainda não possui uma avaliação cadastrada.")
        return

    perguntas = listar_perguntas(prova["id"])
    if not perguntas:
        st.info("Esta avaliação ainda não possui perguntas cadastradas.")
        return

    resultado_anterior = melhor_resultado(aluno_id, prova["id"])
    if resultado_anterior and resultado_anterior["aprovado"]:
        st.success(
            f"Você já foi aprovado nesta avaliação com nota "
            f"{resultado_anterior['nota']:.1f}. Vá até 'Meus Certificados' para baixar o seu certificado."
        )
        return

    st.caption(
        f"A avaliação tem {len(perguntas)} pergunta(s). "
        f"Nota mínima para aprovação: {prova['nota_minima']:.1f} de 10."
    )

    respostas_aluno = {}
    with st.form("form_prova"):
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

    if enviar:
        if any(resposta is None for resposta in respostas_aluno.values()):
            st.warning("Responda todas as perguntas antes de enviar.")
            return

        acertos = sum(
            1 for pergunta in perguntas
            if respostas_aluno[pergunta["id"]] == pergunta["resposta_correta"]
        )
        # Cálculo automático da nota, numa escala de 0 a 10
        nota = round((acertos / len(perguntas)) * 10, 1)
        aprovado = nota >= prova["nota_minima"]

        salvar_resultado_prova(aluno_id, prova["id"], nota, aprovado)

        st.divider()
        st.metric("Sua nota", f"{nota:.1f} / 10", f"{acertos}/{len(perguntas)} acertos")

        if aprovado:
            st.success("🎉 Parabéns, você foi APROVADO! Seu certificado já está disponível para download.")
            st.session_state["pagina_atual"] = "certificados"
            st.balloons()
        else:
            st.error(
                f"Você não atingiu a nota mínima ({prova['nota_minima']:.1f}). "
                f"Revise as aulas e tente novamente."
            )
