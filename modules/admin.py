"""
Módulo de Administração.

Permite que o instrutor/administrador cadastre cursos, aulas, provas e
perguntas sem precisar mexer diretamente no banco de dados, além de
acompanhar o progresso dos alunos. Só é exibido para contas com
is_admin = True (ver instruções no arquivo database/schema.sql).
"""
import streamlit as st
from datetime import datetime

from database.repositorio import (
    listar_cursos,
    criar_curso,
    editar_curso,
    excluir_curso,
    listar_aulas_do_curso,
    criar_aula,
    editar_aula,
    excluir_aula,
    buscar_prova_do_curso,
    criar_prova,
    listar_perguntas,
    criar_pergunta,
    listar_resultados_da_prova,
    liberar_nova_tentativa,
    listar_todos_alunos,
    calcular_progresso_curso,
    contar_alunos_por_filial,
    obter_tempos_curso,
    listar_materiais,
    listar_categorias_materiais,
    enviar_material,
    excluir_material,
    editar_material,
    listar_duvidas,
    marcar_duvida_respondida,
)


def _formatar_duracao(segundos: float) -> str:
    """Converte segundos em um texto curto tipo '2d 3h', '4h 12min' ou '18min'."""
    segundos = int(segundos)
    dias, resto = divmod(segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, _ = divmod(resto, 60)
    if dias > 0:
        return f"{dias}d {horas}h"
    if horas > 0:
        return f"{horas}h {minutos}min"
    return f"{minutos}min"


def _estilos_admin():
    st.markdown(
        """
        <style>
        .admin-header {
            background: linear-gradient(120deg, #0F2E56 0%, #143C6E 100%);
            border-radius: 16px;
            padding: 1.6rem 1.8rem;
            color: #FFFFFF;
            margin-bottom: 1.2rem;
        }
        .admin-header h1 { font-size: 1.5rem; margin: 0 0 .2rem 0; }
        .admin-header p { margin: 0; opacity: .85; font-size: .92rem; }
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E6ECF3;
            border-radius: 12px;
            padding: .9rem 1rem .7rem 1rem;
            box-shadow: 0 2px 8px rgba(20, 60, 110, 0.06);
        }
        button[data-baseweb="tab"] {
            font-size: .95rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _painel_visao_geral():
    cursos = listar_cursos()
    alunos = listar_todos_alunos()
    duvidas_pendentes = listar_duvidas(apenas_nao_respondidas=True)

    total_perguntas = sum(len(listar_perguntas(p["id"])) for p in [buscar_prova_do_curso(c["id"]) for c in cursos] if p)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Cursos", len(cursos))
    col2.metric("🧑‍🎓 Alunos cadastrados", len(alunos))
    col3.metric("❓ Dúvidas pendentes", len(duvidas_pendentes))
    col4.metric("📝 Perguntas de prova", total_perguntas)


def tela_admin():
    _estilos_admin()
    st.markdown(
        """
        <div class="admin-header">
            <h1>⚙️ Painel de Administração</h1>
            <p>Gerencie cursos, aulas, provas, materiais e acompanhe os alunos da plataforma.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _painel_visao_geral()
    st.write("")

    aba_cursos, aba_aulas, aba_provas, aba_alunos, aba_filiais, aba_materiais, aba_duvidas = st.tabs(
        ["📚 Cursos", "🎬 Aulas", "📝 Provas e Perguntas", "🧑‍🎓 Alunos", "📍 Filiais", "🗂️ Materiais", "❓ Dúvidas"]
    )

    # ---------------- CURSOS ----------------
    with aba_cursos:
        st.subheader("Cursos cadastrados")
        cursos_existentes = listar_cursos()
        if cursos_existentes:
            for curso in cursos_existentes:
                with st.container(border=True):
                    col_info, col_editar, col_excluir = st.columns([3, 1, 1])
                    with col_info:
                        st.write(f"**{curso['titulo']}** — Instrutor: {curso['instrutor']}")
                    with col_editar:
                        if st.button("✏️ Editar", key=f"editar_curso_btn_{curso['id']}", use_container_width=True):
                            st.session_state["curso_em_edicao"] = curso["id"]
                            st.rerun()
                    with col_excluir:
                        if st.button("🗑️ Excluir", key=f"excluir_curso_btn_{curso['id']}", use_container_width=True):
                            st.session_state["curso_para_excluir"] = curso["id"]
                            st.rerun()

                    # Confirmação de exclusão (evita apagar um curso sem querer,
                    # já que isso apaga junto aulas, provas e resultados dele).
                    if st.session_state.get("curso_para_excluir") == curso["id"]:
                        st.warning(
                            f"Tem certeza que quer excluir **{curso['titulo']}**? "
                            f"Isso apaga também as aulas, a prova e os resultados desse curso. Essa ação não pode ser desfeita."
                        )
                        col_sim, col_nao = st.columns(2)
                        with col_sim:
                            if st.button("Sim, excluir", key=f"confirma_excluir_curso_{curso['id']}", type="primary", use_container_width=True):
                                excluir_curso(curso["id"])
                                st.session_state.pop("curso_para_excluir", None)
                                st.success("Curso excluído.")
                                st.rerun()
                        with col_nao:
                            if st.button("Cancelar", key=f"cancela_excluir_curso_{curso['id']}", use_container_width=True):
                                st.session_state.pop("curso_para_excluir", None)
                                st.rerun()

                    # Formulário de edição (aparece só para o curso selecionado acima)
                    if st.session_state.get("curso_em_edicao") == curso["id"]:
                        with st.form(f"form_editar_curso_{curso['id']}"):
                            novo_titulo = st.text_input("Título do curso *", value=curso["titulo"])
                            nova_descricao = st.text_area("Descrição", value=curso.get("descricao") or "")
                            novo_instrutor = st.text_input("Nome do instrutor *", value=curso["instrutor"])
                            nova_carga = st.number_input(
                                "Carga horária (horas)", min_value=1, value=curso.get("carga_horaria") or 8
                            )
                            col_salvar, col_cancelar = st.columns(2)
                            with col_salvar:
                                salvar_edicao = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                            with col_cancelar:
                                cancelar_edicao = st.form_submit_button("Cancelar", use_container_width=True)

                        if salvar_edicao:
                            if not novo_titulo or not novo_instrutor:
                                st.warning("Preencha os campos obrigatórios (*).")
                            else:
                                editar_curso(curso["id"], novo_titulo, nova_descricao, novo_instrutor, int(nova_carga))
                                st.session_state.pop("curso_em_edicao", None)
                                st.success("Curso atualizado.")
                                st.rerun()
                        if cancelar_edicao:
                            st.session_state.pop("curso_em_edicao", None)
                            st.rerun()
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
                    with st.container(border=True):
                        col_info, col_editar, col_excluir = st.columns([3, 1, 1])
                        with col_info:
                            st.write(f"**{aula['ordem']}. {aula['titulo']}**")
                            st.caption(aula["url_video"])
                        with col_editar:
                            if st.button("✏️ Editar", key=f"editar_aula_btn_{aula['id']}", use_container_width=True):
                                st.session_state["aula_em_edicao"] = aula["id"]
                                st.rerun()
                        with col_excluir:
                            if st.button("🗑️ Excluir", key=f"excluir_aula_btn_{aula['id']}", use_container_width=True):
                                excluir_aula(aula["id"])
                                st.success("Aula excluída.")
                                st.rerun()

                        if st.session_state.get("aula_em_edicao") == aula["id"]:
                            with st.form(f"form_editar_aula_{aula['id']}"):
                                novo_titulo_aula = st.text_input("Título da aula *", value=aula["titulo"])
                                novo_url = st.text_input("Link do vídeo *", value=aula["url_video"])
                                nova_ordem = st.number_input("Ordem de exibição", min_value=1, value=aula["ordem"])
                                nova_duracao = st.number_input(
                                    "Duração (minutos)", min_value=0, value=aula.get("duracao_minutos") or 0
                                )
                                col_salvar, col_cancelar = st.columns(2)
                                with col_salvar:
                                    salvar_edicao_aula = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                                with col_cancelar:
                                    cancelar_edicao_aula = st.form_submit_button("Cancelar", use_container_width=True)

                            if salvar_edicao_aula:
                                if not novo_titulo_aula or not novo_url:
                                    st.warning("Preencha os campos obrigatórios (*).")
                                else:
                                    editar_aula(aula["id"], novo_titulo_aula, novo_url, int(nova_ordem), int(nova_duracao))
                                    st.session_state.pop("aula_em_edicao", None)
                                    st.success("Aula atualizada.")
                                    st.rerun()
                            if cancelar_edicao_aula:
                                st.session_state.pop("aula_em_edicao", None)
                                st.rerun()
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

                st.divider()
                st.subheader("Tentativas dos alunos")
                st.caption(
                    "Depois de UMA tentativa, o aluno não pode refazer a avaliação sozinho. "
                    "Se ele reprovou e pedir uma nova chance, libere aqui — vale só para a próxima tentativa dele."
                )

                todos_resultados = listar_resultados_da_prova(prova["id"])
                if not todos_resultados:
                    st.caption("Nenhum aluno fez esta avaliação ainda.")
                else:
                    # Mantém só a tentativa mais recente de cada aluno (a lista já
                    # vem ordenada da mais nova para a mais antiga).
                    mais_recente_por_aluno = {}
                    for r in todos_resultados:
                        mais_recente_por_aluno.setdefault(r["aluno_id"], r)

                    nomes_alunos = {a["id"]: a["nome_completo"] for a in listar_todos_alunos()}

                    for aluno_id, r in mais_recente_por_aluno.items():
                        nome = nomes_alunos.get(aluno_id, "Aluno removido")
                        with st.container(border=True):
                            col_info, col_acao = st.columns([3, 1])
                            with col_info:
                                status = "✅ Aprovado" if r["aprovado"] else "❌ Reprovado"
                                st.write(f"**{nome}** — {status} (nota {r['nota']:.1f})")
                                if r.get("tempo_gasto_segundos"):
                                    st.caption(f"Tempo gasto na prova: {_formatar_duracao(r['tempo_gasto_segundos'])}")
                            with col_acao:
                                if not r["aprovado"]:
                                    if r.get("liberado_para_nova_tentativa"):
                                        st.caption("🔓 Liberado — aguardando nova tentativa")
                                    else:
                                        if st.button(
                                            "🔓 Liberar nova tentativa",
                                            key=f"liberar_tentativa_{r['id']}",
                                            use_container_width=True,
                                        ):
                                            liberar_nova_tentativa(r["id"])
                                            st.success(f"Nova tentativa liberada para {nome}.")
                                            st.rerun()

    # ---------------- ALUNOS ----------------
    with aba_alunos:
        st.subheader("Alunos cadastrados")
        alunos = listar_todos_alunos()
        if not alunos:
            st.info("Nenhum aluno cadastrado ainda.")
        else:
            busca = st.text_input(
                "🔎 Buscar por nome, e-mail ou empresa",
                placeholder="Digite para filtrar a lista abaixo...",
            )
            if busca:
                termo = busca.strip().lower()
                alunos = [
                    a for a in alunos
                    if termo in a["nome_completo"].lower()
                    or termo in a["email"].lower()
                    or termo in (a.get("empresa") or "").lower()
                ]
                st.caption(f"{len(alunos)} aluno(s) encontrado(s).")

            cursos = listar_cursos()
            for aluno in alunos:
                with st.container(border=True):
                    st.write(f"**{aluno['nome_completo']}** — {aluno['email']}")
                    st.caption(f"Empresa: {aluno.get('empresa') or '-'} · Cargo: {aluno.get('cargo') or '-'}")
                    if cursos:
                        for curso in cursos:
                            p = calcular_progresso_curso(aluno["id"], curso["id"])
                            if p <= 0:
                                continue
                            linha = f"**{curso['titulo']}**: {int(p * 100)}%"
                            tempos = obter_tempos_curso(aluno["id"], curso["id"])
                            if tempos and tempos.get("finalizado_em"):
                                inicio = datetime.fromisoformat(tempos["iniciado_em"])
                                fim = datetime.fromisoformat(tempos["finalizado_em"])
                                linha += f" · concluído em {_formatar_duracao((fim - inicio).total_seconds())}"
                            elif tempos:
                                linha += " · em andamento"
                            st.caption(linha)

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
                    col_info, col_editar, col_excluir = st.columns([3, 1, 1])
                    with col_info:
                        st.write(f"**{m['titulo']}** — categoria: {m.get('categoria') or '-'}")
                        st.caption(f"Arquivo original: {m['nome_arquivo']}")
                    with col_editar:
                        if st.button("✏️ Editar", key=f"editar_material_btn_{m['id']}", use_container_width=True):
                            st.session_state["material_em_edicao"] = m["id"]
                            st.rerun()
                    with col_excluir:
                        if st.button("🗑️ Excluir", key=f"excluir_material_{m['id']}", use_container_width=True):
                            excluir_material(m["id"], m["caminho_storage"])
                            st.success("Material excluído.")
                            st.rerun()

                    if st.session_state.get("material_em_edicao") == m["id"]:
                        with st.form(f"form_editar_material_{m['id']}"):
                            novo_titulo_material = st.text_input("Título *", value=m["titulo"])
                            nova_descricao_material = st.text_area("Descrição", value=m.get("descricao") or "")
                            nova_categoria_material = st.text_input("Categoria *", value=m.get("categoria") or "")
                            st.caption("O arquivo em si não muda aqui — exclua e suba de novo se precisar trocar o arquivo.")
                            col_salvar, col_cancelar = st.columns(2)
                            with col_salvar:
                                salvar_edicao_material = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                            with col_cancelar:
                                cancelar_edicao_material = st.form_submit_button("Cancelar", use_container_width=True)

                        if salvar_edicao_material:
                            if not novo_titulo_material or not nova_categoria_material:
                                st.warning("Preencha os campos obrigatórios (*).")
                            else:
                                editar_material(m["id"], novo_titulo_material, nova_descricao_material, nova_categoria_material)
                                st.session_state.pop("material_em_edicao", None)
                                st.success("Material atualizado.")
                                st.rerun()
                        if cancelar_edicao_material:
                            st.session_state.pop("material_em_edicao", None)
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
