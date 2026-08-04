"""
Módulo de Cursos e Aulas.

Mostra a lista de cursos disponíveis, o player de vídeo de cada aula
(usando o próprio st.video, que já suporta links do YouTube) e a barra
de progresso do curso.
"""
import streamlit as st

from database.repositorio import (
    listar_cursos,
    buscar_curso,
    listar_aulas_do_curso,
    aulas_concluidas_do_aluno,
    calcular_progresso_curso,
    marcar_aula_concluida,
)


def tela_lista_cursos():
    st.title("📚 Meus Cursos")

    cursos = listar_cursos()
    if not cursos:
        st.info("Nenhum curso disponível no momento. Volte em breve!")
        return

    aluno_id = st.session_state["aluno_id"]

for curso in cursos:
        progresso = calcular_progresso_curso(aluno_id, curso["id"])
        with st.container(border=True):
            col_info, col_botao = st.columns([3, 1])
            
            with col_info:
                st.markdown(f"### {curso['titulo']}")
                st.caption(f"Instrutor: {curso['instrutor']}")
                
                # Descrição minimizada por padrão
                if curso.get("descricao"):
                    with st.expander("📖 Ver descrição do curso", expanded=False):
                        st.write(curso["descricao"])
                
                st.progress(progresso, text=f"{int(progresso * 100)}% concluído")
                
            with col_botao:
                st.write("")
                st.write("")
                if st.button("Acessar curso", key=f"acessar_{curso['id']}", use_container_width=True):
                    st.session_state["curso_atual_id"] = curso["id"]
                    st.session_state["pagina_atual"] = "detalhe_curso"
                    st.rerun()

def tela_detalhe_curso():
    curso_id = st.session_state.get("curso_atual_id")
    curso = buscar_curso(curso_id)

    if curso is None:
        st.error("Curso não encontrado.")
        return

    if st.button("← Voltar para Meus Cursos"):
        st.session_state["pagina_atual"] = "lista_cursos"
        st.rerun()

    st.title(curso["titulo"])
    st.caption(f"Instrutor: {curso['instrutor']} · Carga horária: {curso.get('carga_horaria', '-')}h")
    if curso.get("descricao"):
        st.write(curso["descricao"])

    aluno_id = st.session_state["aluno_id"]
    aulas = listar_aulas_do_curso(curso_id)

    if not aulas:
        st.info("Este curso ainda não possui aulas cadastradas.")
        return

    concluidas = set(aulas_concluidas_do_aluno(aluno_id, curso_id))
    progresso = len(concluidas) / len(aulas)
    st.progress(progresso, text=f"Progresso do curso: {int(progresso * 100)}%")

    st.divider()

    for aula in aulas:
        aula_concluida = aula["id"] in concluidas
        icone = "✅" if aula_concluida else "▶️"
        with st.expander(f"{icone} Aula {aula['ordem']}: {aula['titulo']}", expanded=not aula_concluida):
            st.video(aula["url_video"])
            if aula_concluida:
                st.success("Você já concluiu esta aula.")
            else:
                if st.button("Marcar aula como concluída", key=f"concluir_{aula['id']}"):
                    marcar_aula_concluida(aluno_id, aula["id"])
                    st.rerun()

    st.divider()
    if progresso >= 1.0:
        st.success("🎉 Você concluiu todas as aulas! Agora faça a avaliação final para obter seu certificado.")
        if st.button("Ir para a Avaliação", type="primary"):
            st.session_state["pagina_atual"] = "prova"
            st.rerun()
    else:
        st.info("Conclua todas as aulas para liberar a avaliação final do curso.")
