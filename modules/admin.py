"""
Módulo de Administração.

Permite que o instrutor/administrador cadastre cursos, aulas, provas e
perguntas sem precisar mexer diretamente no banco de dados, além de
acompanhar o progresso dos alunos. Só é exibido para contas com
is_admin = True (ver instruções no arquivo database/schema.sql).
"""
import streamlit as st

from database.repositorio import (
    listar_cursos,
    criar_curso,
    listar_aulas_do_curso,
    criar_aula,
    buscar_prova_do_curso,
    criar_prova,
    listar_perguntas,
    criar_pergunta,
    listar_todos_alunos,
    calcular_progresso_curso,
)


def tela_admin():
    st.title("⚙️ Painel de Administração")

    aba_cursos, aba_aulas, aba_provas, aba_alunos = st.tabs(
        ["Cursos", "Aulas", "Provas e Perguntas", "Alunos"]
    )

    # ---------------- CURSOS ----------------
    with aba_cursos:
        st.subheader("Cursos cadastrados")
        cursos_existentes = listar_cursos()
        if cursos_existentes:
            for curso in cursos_existentes:
                st.write(f"**{curso['titulo']}** — Instrutor: {curso['instrutor']}")
        else:
            st.caption("Nenhum curso cadastrado ainda.")

        st.divider()
        st.subheader("Cadastrar novo curso")
        with st.form("form_novo_curso", clear_on_submit=True):
            titulo = st.text_input("Título do curso *")
            descricao = st.text_area("Descrição")
            instrutor = st.text_input("Nome do instrutor *")
            carga_horaria = st.number_input("Carga horária (horas)", min_value=1, value=8)
            salvar = st.form_submit_button("Salvar curso", type="primary")

        if salvar:
            if not titulo or not instrutor:
                st.warning("Preencha os campos obrigatórios (*).")
            else:
                criar_curso(titulo, descricao, instrutor, int(carga_horaria))
                st.success(f"Curso '{titulo}' cadastrado com sucesso!")
                st.rerun()

    # ---------------- AULAS ----------------
    with aba_aulas:
        cursos = listar_cursos()
        if not cursos:
            st.info("Cadastre um curso primeiro, na aba 'Cursos'.")
        else:
            opcoes_curso = {c["titulo"]: c["id"] for c in cursos}
            titulo_escolhido = st.selectbox("Selecione o curso", list(opcoes_curso.keys()), key="sel_curso_aula")
            curso_id = opcoes_curso[titulo_escolhido]

            st.subheader("Aulas deste curso")
            aulas = listar_aulas_do_curso(curso_id)
            if aulas:
                for aula in aulas:
                    st.write(f"{aula['ordem']}. {aula['titulo']} — {aula['url_video']}")
            else:
                st.caption("Nenhuma aula cadastrada ainda.")

            st.divider()
            st.subheader("Cadastrar nova aula")
            with st.form("form_nova_aula", clear_on_submit=True):
                titulo_aula = st.text_input("Título da aula *")
                url_video = st.text_input(
                    "Link do vídeo (YouTube não listado) *",
                    placeholder="https://www.youtube.com/watch?v=XXXXXXXXXXX",
                )
                ordem = st.number_input("Ordem de exibição", min_value=1, value=len(aulas) + 1)
                duracao = st.number_input("Duração (minutos)", min_value=0, value=10)
                salvar_aula = st.form_submit_button("Salvar aula", type="primary")

            if salvar_aula:
                if not titulo_aula or not url_video:
                    st.warning("Preencha os campos obrigatórios (*).")
                else:
                    criar_aula(curso_id, titulo_aula, url_video, int(ordem), int(duracao))
                    st.success(f"Aula '{titulo_aula}' cadastrada com sucesso!")
                    st.rerun()

    # ---------------- PROVAS E PERGUNTAS ----------------
    with aba_provas:
        cursos = listar_cursos()
        if not cursos:
            st.info("Cadastre um curso primeiro, na aba 'Cursos'.")
        else:
            opcoes_curso = {c["titulo"]: c["id"] for c in cursos}
            titulo_escolhido = st.selectbox(
                "Selecione o curso", list(opcoes_curso.keys()), key="sel_curso_prova"
            )
            curso_id = opcoes_curso[titulo_escolhido]

            prova = buscar_prova_do_curso(curso_id)

            if prova is None:
                st.info("Este curso ainda não tem avaliação. Cadastre uma abaixo.")
                with st.form("form_nova_prova", clear_on_submit=True):
                    titulo_prova = st.text_input("Título da avaliação *", value="Avaliação Final")
                    nota_minima = st.number_input(
                        "Nota mínima para aprovação (0 a 10)",
                        min_value=0.0, max_value=10.0, value=7.0, step=0.5,
                    )
                    criar_prova_btn = st.form_submit_button("Criar avaliação", type="primary")
                if criar_prova_btn:
                    if not titulo_prova:
                        st.warning("Informe o título da avaliação.")
                    else:
                        criar_prova(curso_id, titulo_prova, nota_minima)
                        st.success("Avaliação criada! Agora adicione as perguntas abaixo.")
                        st.rerun()
            else:
                st.success(f"Avaliação atual: **{prova['titulo']}** (nota mínima {prova['nota_minima']:.1f})")

                perguntas = listar_perguntas(prova["id"])
                st.write(f"**{len(perguntas)} pergunta(s) cadastrada(s)**")
                for i, p in enumerate(perguntas, start=1):
                    st.caption(f"{i}. {p['enunciado']} (resposta correta: {p['resposta_correta']})")

                st.divider()
                st.subheader("Adicionar pergunta")
                with st.form("form_nova_pergunta", clear_on_submit=True):
                    enunciado = st.text_area("Enunciado da pergunta *")
                    opcao_a = st.text_input("Alternativa A *")
                    opcao_b = st.text_input("Alternativa B *")
                    opcao_c = st.text_input("Alternativa C *")
                    opcao_d = st.text_input("Alternativa D *")
                    correta = st.selectbox("Alternativa correta *", ["A", "B", "C", "D"])
                    ordem_pergunta = st.number_input("Ordem", min_value=1, value=len(perguntas) + 1)
                    salvar_pergunta = st.form_submit_button("Salvar pergunta", type="primary")

                if salvar_pergunta:
                    campos = [enunciado, opcao_a, opcao_b, opcao_c, opcao_d]
                    if not all(campos):
                        st.warning("Preencha todos os campos obrigatórios (*).")
                    else:
                        criar_pergunta(
                            prova["id"], enunciado, opcao_a, opcao_b, opcao_c, opcao_d,
                            correta, int(ordem_pergunta),
                        )
                        st.success("Pergunta adicionada com sucesso!")
                        st.rerun()

    # ---------------- ALUNOS ----------------
    with aba_alunos:
        st.subheader("Alunos cadastrados")
        alunos = listar_todos_alunos()
        if not alunos:
            st.info("Nenhum aluno cadastrado ainda.")
        else:
            cursos = listar_cursos()
            for aluno in alunos:
                with st.container(border=True):
                    st.write(f"**{aluno['nome_completo']}** — {aluno['email']}")
                    st.caption(f"Empresa: {aluno.get('empresa') or '-'} · Cargo: {aluno.get('cargo') or '-'}")
                    if cursos:
                        linhas_progresso = []
                        for curso in cursos:
                            p = calcular_progresso_curso(aluno["id"], curso["id"])
                            if p > 0:
                                linhas_progresso.append(f"{curso['titulo']}: {int(p * 100)}%")
                        if linhas_progresso:
                            st.caption(" · ".join(linhas_progresso))
