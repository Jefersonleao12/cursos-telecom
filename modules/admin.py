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
    contar_alunos_por_filial,
    listar_materiais,
    listar_categorias_materiais,
    enviar_material,
    excluir_material,
    listar_duvidas,
    marcar_duvida_respondida,
)


def tela_admin():
    st.title("⚙️ Painel de Administração")

    aba_cursos, aba_aulas, aba_provas, aba_alunos, aba_filiais, aba_materiais, aba_duvidas = st.tabs(
        ["Cursos", "Aulas", "Provas e Perguntas", "Alunos", "Filiais", "Materiais", "Dúvidas"]
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

    # ---------------- FILIAIS ----------------
    with aba_filiais:
        st.subheader("Alunos por filial")
        grupos = contar_alunos_por_filial()

        if not grupos:
            st.info("Nenhum aluno cadastrado ainda.")
        else:
            total_alunos = sum(len(lista) for lista in grupos.values())
            st.caption(f"Total geral: {total_alunos} aluno(s) em {len(grupos)} filial(is).")

            # Resumo rápido: quantidade por filial, em colunas
            colunas = st.columns(3)
            for i, (nome_filial, lista_alunos) in enumerate(grupos.items()):
                with colunas[i % 3]:
                    st.metric(nome_filial, len(lista_alunos))

            st.divider()

            # Detalhe: lista de nomes dentro de cada filial (em expansores)
            for nome_filial, lista_alunos in grupos.items():
                with st.expander(f"📍 {nome_filial} — {len(lista_alunos)} aluno(s)"):
                    for aluno in lista_alunos:
                        st.write(f"- {aluno['nome_completo']} ({aluno['email']})")

    # ---------------- MATERIAIS ----------------
    with aba_materiais:
        st.subheader("Materiais cadastrados")
        materiais = listar_materiais()

        if materiais:
            for m in materiais:
                with st.container(border=True):
                    col_info, col_excluir = st.columns([4, 1])
                    with col_info:
                        st.write(f"**{m['titulo']}** — categoria: {m.get('categoria') or '-'}")
                        st.caption(f"Arquivo original: {m['nome_arquivo']}")
                    with col_excluir:
                        if st.button("🗑️ Excluir", key=f"excluir_material_{m['id']}", use_container_width=True):
                            excluir_material(m["id"], m["caminho_storage"])
                            st.success("Material excluído.")
                            st.rerun()
        else:
            st.caption("Nenhum material cadastrado ainda.")

        st.divider()
        st.subheader("Enviar novo material")

        categorias_existentes = listar_categorias_materiais()
        opcoes_categoria = categorias_existentes + ["+ Nova categoria..."]

        with st.form("form_novo_material", clear_on_submit=True):
            titulo_material = st.text_input("Título *")
            descricao_material = st.text_area("Descrição (opcional)")
            categoria_opcao = st.selectbox("Categoria *", opcoes_categoria)
            nova_categoria = ""
            if categoria_opcao == "+ Nova categoria...":
                nova_categoria = st.text_input("Nome da nova categoria *")
            arquivo = st.file_uploader(
                "Arquivo *",
                help="Fotos, PDFs, planilhas, documentos do Word, vídeos, etc.",
            )
            enviar = st.form_submit_button("Enviar material", type="primary")

        if enviar:
            categoria_final = (
                nova_categoria.strip() if categoria_opcao == "+ Nova categoria..." else categoria_opcao
            )
            if not titulo_material or not categoria_final or arquivo is None:
                st.warning("Preencha todos os campos obrigatórios (*) e escolha um arquivo.")
            else:
                enviar_material(
                    titulo_material, descricao_material, categoria_final,
                    arquivo.getvalue(), arquivo.name,
                )
                st.success(f"Material '{titulo_material}' enviado com sucesso!")
                st.rerun()

    # ---------------- DÚVIDAS ----------------
    with aba_duvidas:
        st.subheader("Dúvidas enviadas pelos alunos")
        apenas_pendentes = st.toggle("Mostrar só as pendentes", value=True)

        duvidas = listar_duvidas(apenas_nao_respondidas=apenas_pendentes)

        if not duvidas:
            st.info("Nenhuma dúvida pendente." if apenas_pendentes else "Nenhuma dúvida registrada ainda.")
        else:
            for d in duvidas:
                with st.container(border=True):
                    col_texto, col_acao = st.columns([4, 1])
                    with col_texto:
                        st.write(f"**{d['aluno_nome']}**")
                        st.caption(d["mensagem"])
                        st.caption(f"Enviada em: {d['criado_em'][:16].replace('T', ' ')}")
                    with col_acao:
                        if not d["respondida"]:
                            if st.button("✅ Marcar respondida", key=f"resp_duvida_{d['id']}", use_container_width=True):
                                marcar_duvida_respondida(d["id"])
                                st.rerun()
                        else:
                            st.caption("✅ Respondida")
