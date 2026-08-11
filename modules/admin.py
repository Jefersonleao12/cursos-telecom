"""
Módulo de Administração.

Permite que o instrutor/administrador cadastre cursos, aulas, provas e
perguntas sem precisar mexer diretamente no banco de dados, além de
acompanhar o progresso dos alunos. Só é exibido para contas com
is_admin = True (ver instruções no arquivo database/schema.sql).
"""
import re
import streamlit as st
from datetime import datetime

from modules.whatsapp import diagnosticar_configuracao

from database.repositorio import (
    listar_cursos,
    criar_curso,
    editar_curso,
    excluir_curso,
    listar_modulos_do_curso,
    buscar_modulo,
    criar_modulo,
    editar_modulo,
    excluir_modulo,
    listar_aulas_do_modulo,
    criar_aula,
    editar_aula,
    excluir_aula,
    buscar_prova_do_modulo,
    criar_prova,
    editar_prova,
    excluir_prova,
    listar_perguntas,
    criar_pergunta,
    editar_pergunta,
    excluir_pergunta,
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
    definir_acesso_aluno,
    definir_admin_aluno,
    gerar_senha_temporaria,
    listar_todos_certificados,
    listar_provas_do_curso,
    listar_todos_resultados_provas,
    criar_aviso,
    listar_todos_avisos,
    desativar_aviso,
    criar_destaque,
    editar_destaque,
    excluir_destaque,
    listar_todos_destaques,
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

    total_perguntas = sum(
        len(listar_perguntas(p["id"]))
        for c in cursos
        for p in listar_provas_do_curso(c["id"])
    )

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

    aba_dashboard, aba_cursos, aba_modulos, aba_aulas, aba_provas, aba_alunos, aba_filiais, aba_materiais, aba_duvidas, aba_avisos, aba_destaques = st.tabs(
        ["📊 Dashboard", "📚 Cursos", "🧩 Módulos", "🎬 Aulas", "📝 Provas e Perguntas", "🧑‍🎓 Alunos", "📍 Filiais", "🗂️ Materiais", "❓ Dúvidas", "📢 Avisos", "🌟 Destaques"]
    )

    # ---------------- DASHBOARD ----------------
    with aba_dashboard:
        cursos_todos = listar_cursos()
        alunos_todos = listar_todos_alunos()
        certificados_todos = listar_todos_certificados()
        resultados_todos = listar_todos_resultados_provas()

        alunos_ativos = [a for a in alunos_todos if a.get("ativo", True)]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🧑‍🎓 Alunos ativos", len(alunos_ativos))
        col2.metric("📚 Cursos", len(cursos_todos))
        col3.metric("🏆 Certificados de capacitação emitidos", len(certificados_todos))

        if resultados_todos:
            taxa_aprovacao = sum(1 for r in resultados_todos if r["aprovado"]) / len(resultados_todos) * 100
        else:
            taxa_aprovacao = 0
        col4.metric("✅ Taxa média de aprovação", f"{taxa_aprovacao:.0f}%")

        st.write("")
        col_grafico1, col_grafico2 = st.columns(2)

        with col_grafico1:
            st.subheader("Alunos por filial")
            grupos_filial = contar_alunos_por_filial()
            if grupos_filial:
                dados_grafico = {nome: len(lista) for nome, lista in grupos_filial.items()}
                st.bar_chart(dados_grafico)
            else:
                st.caption("Nenhum aluno cadastrado ainda.")

        with col_grafico2:
            st.subheader("Certificados de capacitação por curso")
            if certificados_todos and cursos_todos:
                nomes_curso = {c["id"]: c["titulo"] for c in cursos_todos}
                contagem_por_curso = {}
                for cert in certificados_todos:
                    nome = nomes_curso.get(cert["curso_id"], "Curso removido")
                    contagem_por_curso[nome] = contagem_por_curso.get(nome, 0) + 1
                st.bar_chart(contagem_por_curso)
            else:
                st.caption("Nenhum certificado de capacitação emitido ainda.")

        st.write("")
        st.subheader("Progresso médio por curso")
        if cursos_todos and alunos_todos:
            for curso in cursos_todos:
                progressos = [calcular_progresso_curso(a["id"], curso["id"]) for a in alunos_todos]
                progressos_iniciados = [p for p in progressos if p > 0]
                if progressos_iniciados:
                    media = sum(progressos_iniciados) / len(progressos_iniciados)
                    st.progress(media, text=f"{curso['titulo']}: {int(media * 100)}% em média ({len(progressos_iniciados)} aluno(s) iniciaram)")
        else:
            st.caption("Ainda não há dados suficientes.")

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
    # ---------------- MÓDULOS ----------------
    with aba_modulos:
        st.caption("Cada curso é dividido em módulos (assuntos). O aluno assiste os vídeos de um módulo, faz a prova dele (se houver) e só então o próximo módulo é liberado.")
        cursos = listar_cursos()
        if not cursos:
            st.info("Cadastre um curso primeiro, na aba 'Cursos'.")
        else:
            opcoes_curso_mod = {c["titulo"]: c["id"] for c in cursos}
            titulo_escolhido_mod = st.selectbox("Selecione o curso", list(opcoes_curso_mod.keys()), key="sel_curso_modulo")
            curso_id_mod = opcoes_curso_mod[titulo_escolhido_mod]

            st.subheader("Módulos deste curso")
            modulos = listar_modulos_do_curso(curso_id_mod)
            if modulos:
                for modulo in modulos:
                    with st.container(border=True):
                        col_info, col_editar, col_excluir = st.columns([3, 1, 1])
                        with col_info:
                            st.write(f"**{modulo['ordem']}. {modulo['titulo']}**")
                        with col_editar:
                            if st.button("✏️ Editar", key=f"editar_modulo_btn_{modulo['id']}", use_container_width=True):
                                st.session_state["modulo_em_edicao"] = modulo["id"]
                                st.rerun()
                        with col_excluir:
                            if st.button("🗑️ Excluir", key=f"excluir_modulo_btn_{modulo['id']}", use_container_width=True):
                                st.session_state["modulo_para_excluir"] = modulo["id"]
                                st.rerun()

                        if st.session_state.get("modulo_para_excluir") == modulo["id"]:
                            st.warning(
                                f"Tem certeza que quer excluir **{modulo['titulo']}**? "
                                f"Isso apaga também as aulas, a prova e os resultados desse módulo."
                            )
                            col_sim, col_nao = st.columns(2)
                            with col_sim:
                                if st.button("Sim, excluir", key=f"confirma_excluir_modulo_{modulo['id']}", type="primary", use_container_width=True):
                                    excluir_modulo(modulo["id"])
                                    st.session_state.pop("modulo_para_excluir", None)
                                    st.success("Módulo excluído.")
                                    st.rerun()
                            with col_nao:
                                if st.button("Cancelar", key=f"cancela_excluir_modulo_{modulo['id']}", use_container_width=True):
                                    st.session_state.pop("modulo_para_excluir", None)
                                    st.rerun()

                        if st.session_state.get("modulo_em_edicao") == modulo["id"]:
                            with st.form(f"form_editar_modulo_{modulo['id']}"):
                                novo_titulo_modulo = st.text_input("Título do módulo *", value=modulo["titulo"])
                                nova_ordem_modulo = st.number_input("Ordem", min_value=1, value=modulo["ordem"])
                                col_salvar, col_cancelar = st.columns(2)
                                with col_salvar:
                                    salvar_edicao_modulo = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                                with col_cancelar:
                                    cancelar_edicao_modulo = st.form_submit_button("Cancelar", use_container_width=True)

                            if salvar_edicao_modulo:
                                if not novo_titulo_modulo:
                                    st.warning("Informe o título do módulo.")
                                else:
                                    editar_modulo(modulo["id"], novo_titulo_modulo, int(nova_ordem_modulo))
                                    st.session_state.pop("modulo_em_edicao", None)
                                    st.success("Módulo atualizado.")
                                    st.rerun()
                            if cancelar_edicao_modulo:
                                st.session_state.pop("modulo_em_edicao", None)
                                st.rerun()
            else:
                st.caption("Nenhum módulo cadastrado ainda neste curso.")

            st.divider()
            st.subheader("Adicionar módulo")
            with st.form("form_novo_modulo", clear_on_submit=True):
                titulo_modulo = st.text_input("Título do módulo *", placeholder="Ex: Módulo 1 - Fundamentos de Fibra Óptica")
                ordem_modulo = st.number_input("Ordem de exibição", min_value=1, value=len(modulos) + 1)
                salvar_modulo = st.form_submit_button("Salvar módulo", type="primary")

            if salvar_modulo:
                if not titulo_modulo:
                    st.warning("Informe o título do módulo.")
                else:
                    criar_modulo(curso_id_mod, titulo_modulo, int(ordem_modulo))
                    st.success(f"Módulo '{titulo_modulo}' cadastrado com sucesso!")
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

            modulos_do_curso = listar_modulos_do_curso(curso_id)
            if not modulos_do_curso:
                st.warning("Este curso ainda não tem nenhum módulo. Cadastre um na aba '🧩 Módulos' primeiro.")
            else:
                opcoes_modulo = {f"{m['ordem']}. {m['titulo']}": m["id"] for m in modulos_do_curso}
                modulo_escolhido_label = st.selectbox("Selecione o módulo", list(opcoes_modulo.keys()), key="sel_modulo_aula")
                modulo_id = opcoes_modulo[modulo_escolhido_label]

                st.subheader("Aulas deste módulo")
                aulas = listar_aulas_do_modulo(modulo_id)
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
                    st.caption("Nenhuma aula cadastrada ainda neste módulo.")

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
                        criar_aula(modulo_id, curso_id, titulo_aula, url_video, int(ordem), int(duracao))
                        st.success(f"Aula '{titulo_aula}' cadastrada com sucesso!")
                        st.rerun()

    # ---------------- PROVAS E PERGUNTAS ----------------
    with aba_provas:
        cursos = listar_cursos()
        if not cursos:
            st.info("Cadastre um curso primeiro, na aba 'Cursos'.")
        else:
            opcoes_curso_prova = {c["titulo"]: c["id"] for c in cursos}
            titulo_escolhido_prova = st.selectbox(
                "Selecione o curso", list(opcoes_curso_prova.keys()), key="sel_curso_prova"
            )
            curso_id_prova = opcoes_curso_prova[titulo_escolhido_prova]

            modulos_do_curso_prova = listar_modulos_do_curso(curso_id_prova)
            if not modulos_do_curso_prova:
                st.warning("Este curso ainda não tem nenhum módulo. Cadastre um na aba '🧩 Módulos' primeiro.")
            else:
                opcoes_modulo_prova = {f"{m['ordem']}. {m['titulo']}": m["id"] for m in modulos_do_curso_prova}
                modulo_escolhido_prova_label = st.selectbox(
                    "Selecione o módulo", list(opcoes_modulo_prova.keys()), key="sel_modulo_prova"
                )
                modulo_id_prova = opcoes_modulo_prova[modulo_escolhido_prova_label]

                prova = buscar_prova_do_modulo(modulo_id_prova)

                if prova is None:
                    st.info("Este módulo ainda não tem avaliação. Cadastre uma abaixo (opcional — um módulo também pode ter só vídeos, sem prova).")
                    with st.form("form_nova_prova", clear_on_submit=True):
                        titulo_prova = st.text_input("Título da avaliação *", value="Avaliação do módulo")
                        nota_minima = st.number_input(
                            "Nota mínima para aprovação (0 a 10)",
                            min_value=0.0, max_value=10.0, value=7.0, step=0.5,
                        )
                        criar_prova_btn = st.form_submit_button("Criar avaliação", type="primary")
                    if criar_prova_btn:
                        if not titulo_prova:
                            st.warning("Informe o título da avaliação.")
                        else:
                            criar_prova(modulo_id_prova, curso_id_prova, titulo_prova, nota_minima)
                            st.success("Avaliação criada! Agora adicione as perguntas abaixo.")
                            st.rerun()
                else:
                    col_prova_info, col_prova_editar, col_prova_excluir = st.columns([3, 1, 1])
                    with col_prova_info:
                        st.success(f"Avaliação atual: **{prova['titulo']}** (nota mínima {prova['nota_minima']:.1f})")
                    with col_prova_editar:
                        if st.button("✏️ Editar prova", key=f"editar_prova_btn_{prova['id']}", use_container_width=True):
                            st.session_state["prova_em_edicao"] = prova["id"]
                            st.rerun()
                    with col_prova_excluir:
                        if st.button("🗑️ Excluir prova", key=f"excluir_prova_btn_{prova['id']}", use_container_width=True):
                            st.session_state["prova_para_excluir"] = prova["id"]
                            st.rerun()

                    if st.session_state.get("prova_para_excluir") == prova["id"]:
                        st.warning("Tem certeza? Isso apaga todas as perguntas e resultados desta avaliação.")
                        col_sim, col_nao = st.columns(2)
                        with col_sim:
                            if st.button("Sim, excluir prova", key=f"confirma_excluir_prova_{prova['id']}", type="primary", use_container_width=True):
                                excluir_prova(prova["id"])
                                st.session_state.pop("prova_para_excluir", None)
                                st.success("Avaliação excluída.")
                                st.rerun()
                        with col_nao:
                            if st.button("Cancelar", key=f"cancela_excluir_prova_{prova['id']}", use_container_width=True):
                                st.session_state.pop("prova_para_excluir", None)
                                st.rerun()

                    if st.session_state.get("prova_em_edicao") == prova["id"]:
                        with st.form(f"form_editar_prova_{prova['id']}"):
                            novo_titulo_prova = st.text_input("Título da avaliação *", value=prova["titulo"])
                            nova_nota_minima = st.number_input(
                                "Nota mínima para aprovação (0 a 10)",
                                min_value=0.0, max_value=10.0, value=float(prova["nota_minima"]), step=0.5,
                            )
                            col_salvar, col_cancelar = st.columns(2)
                            with col_salvar:
                                salvar_edicao_prova = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                            with col_cancelar:
                                cancelar_edicao_prova = st.form_submit_button("Cancelar", use_container_width=True)

                        if salvar_edicao_prova:
                            if not novo_titulo_prova:
                                st.warning("Informe o título da avaliação.")
                            else:
                                editar_prova(prova["id"], novo_titulo_prova, nova_nota_minima)
                                st.session_state.pop("prova_em_edicao", None)
                                st.success("Avaliação atualizada.")
                                st.rerun()
                        if cancelar_edicao_prova:
                            st.session_state.pop("prova_em_edicao", None)
                            st.rerun()

                    perguntas = listar_perguntas(prova["id"])
                    st.write(f"**{len(perguntas)} pergunta(s) cadastrada(s)**")
                    for i, p in enumerate(perguntas, start=1):
                        with st.container(border=True):
                            col_pergunta, col_editar_p, col_excluir_p = st.columns([3, 1, 1])
                            with col_pergunta:
                                st.caption(f"{i}. {p['enunciado']} (resposta correta: {p['resposta_correta']})")
                            with col_editar_p:
                                if st.button("✏️", key=f"editar_pergunta_btn_{p['id']}", use_container_width=True, help="Editar pergunta"):
                                    st.session_state["pergunta_em_edicao"] = p["id"]
                                    st.rerun()
                            with col_excluir_p:
                                if st.button("🗑️", key=f"excluir_pergunta_btn_{p['id']}", use_container_width=True, help="Excluir pergunta"):
                                    excluir_pergunta(p["id"])
                                    st.success("Pergunta excluída.")
                                    st.rerun()

                            if st.session_state.get("pergunta_em_edicao") == p["id"]:
                                with st.form(f"form_editar_pergunta_{p['id']}"):
                                    novo_enunciado = st.text_area("Enunciado da pergunta *", value=p["enunciado"])
                                    nova_opcao_a = st.text_input("Alternativa A *", value=p["opcao_a"])
                                    nova_opcao_b = st.text_input("Alternativa B *", value=p["opcao_b"])
                                    nova_opcao_c = st.text_input("Alternativa C *", value=p["opcao_c"])
                                    nova_opcao_d = st.text_input("Alternativa D *", value=p["opcao_d"])
                                    nova_correta = st.selectbox(
                                        "Alternativa correta *", ["A", "B", "C", "D"],
                                        index=["A", "B", "C", "D"].index(p["resposta_correta"]),
                                    )
                                    nova_ordem_pergunta = st.number_input("Ordem", min_value=1, value=p["ordem"])
                                    col_salvar_p, col_cancelar_p = st.columns(2)
                                    with col_salvar_p:
                                        salvar_edicao_pergunta = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                                    with col_cancelar_p:
                                        cancelar_edicao_pergunta = st.form_submit_button("Cancelar", use_container_width=True)

                                if salvar_edicao_pergunta:
                                    campos_edicao = [novo_enunciado, nova_opcao_a, nova_opcao_b, nova_opcao_c, nova_opcao_d]
                                    if not all(campos_edicao):
                                        st.warning("Preencha todos os campos obrigatórios (*).")
                                    else:
                                        editar_pergunta(
                                            p["id"], novo_enunciado, nova_opcao_a, nova_opcao_b, nova_opcao_c, nova_opcao_d,
                                            nova_correta, int(nova_ordem_pergunta),
                                        )
                                        st.session_state.pop("pergunta_em_edicao", None)
                                        st.success("Pergunta atualizada.")
                                        st.rerun()
                                if cancelar_edicao_pergunta:
                                    st.session_state.pop("pergunta_em_edicao", None)
                                    st.rerun()

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

            # Destaque no topo: pedidos de "esqueci minha senha" pendentes
            pedidos_senha = [a for a in alunos if a.get("solicitou_redefinicao_senha")]
            if pedidos_senha:
                st.warning(f"🔑 {len(pedidos_senha)} aluno(s) pediram redefinição de senha — veja abaixo.")

            for aluno in alunos:
                destaque = " 🔑" if aluno.get("solicitou_redefinicao_senha") else ""
                inativo_label = " · 🚫 acesso desativado" if not aluno.get("ativo", True) else ""
                with st.container(border=True):
                    col_foto, col_texto = st.columns([1, 8])
                    with col_foto:
                        if aluno.get("foto_url"):
                            st.image(aluno["foto_url"], width=52)
                        else:
                            st.markdown(
                                "<div style='width:52px; height:52px; border-radius:50%; "
                                "background:#EAF1FB; display:flex; align-items:center; justify-content:center; "
                                "font-size:1.4rem;'>👤</div>",
                                unsafe_allow_html=True,
                            )
                    with col_texto:
                        st.write(f"**{aluno['nome_completo']}**{destaque} — {aluno['email']}{inativo_label}")
                        st.caption(
                            f"Empresa: {aluno.get('empresa') or '-'} · Cargo: {aluno.get('cargo') or '-'} · "
                            f"Filial: {aluno.get('filial') or '-'}"
                        )
                    if aluno.get("is_admin"):
                        st.caption("⭐ Administrador")

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

                    st.write("")
                    col_admin, col_acesso, col_senha = st.columns(3)
                    with col_admin:
                        if aluno.get("is_admin"):
                            if st.button("⭐ Remover admin", key=f"remover_admin_{aluno['id']}", use_container_width=True):
                                definir_admin_aluno(aluno["id"], False)
                                st.rerun()
                        else:
                            if st.button("⭐ Tornar admin", key=f"tornar_admin_{aluno['id']}", use_container_width=True):
                                definir_admin_aluno(aluno["id"], True)
                                st.rerun()
                    with col_acesso:
                        if aluno.get("ativo", True):
                            if st.button("🚫 Desativar acesso", key=f"desativar_{aluno['id']}", use_container_width=True):
                                definir_acesso_aluno(aluno["id"], False)
                                st.rerun()
                        else:
                            if st.button("✅ Reativar acesso", key=f"reativar_{aluno['id']}", use_container_width=True):
                                definir_acesso_aluno(aluno["id"], True)
                                st.rerun()
                    with col_senha:
                        rotulo_senha = "🔑 Gerar nova senha" if not aluno.get("solicitou_redefinicao_senha") else "🔑 Atender pedido"
                        if st.button(rotulo_senha, key=f"gerar_senha_{aluno['id']}", type="primary" if aluno.get("solicitou_redefinicao_senha") else "secondary", use_container_width=True):
                            st.session_state[f"nova_senha_gerada_{aluno['id']}"] = gerar_senha_temporaria(aluno["id"])
                            st.rerun()

                    senha_gerada = st.session_state.get(f"nova_senha_gerada_{aluno['id']}")
                    if senha_gerada:
                        st.success(
                            f"Senha temporária para **{aluno['nome_completo']}**: `{senha_gerada}` "
                            f"— repasse por telefone/WhatsApp. Ele será obrigado a trocar no próximo login."
                        )
                        if st.button("Ok, já anotei", key=f"limpar_senha_{aluno['id']}"):
                            st.session_state.pop(f"nova_senha_gerada_{aluno['id']}", None)
                            st.rerun()

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

        with st.expander("🔔 Testar notificação por WhatsApp"):
            st.caption(
                "Toda dúvida enviada por um aluno tenta avisar você automaticamente "
                "no WhatsApp (via CallMeBot). Use o botão abaixo para conferir se "
                "isso está configurado corretamente — a dúvida em si sempre fica "
                "salva aqui mesmo se a notificação falhar."
            )
            if st.button("Enviar mensagem de teste"):
                with st.spinner("Enviando..."):
                    sucesso, detalhe = diagnosticar_configuracao()
                if sucesso:
                    st.success(detalhe)
                else:
                    st.error(detalhe)

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
                        if d.get("telefone"):
                            st.caption(f"📱 {d['telefone']}")
                        st.caption(d["mensagem"])
                        st.caption(f"Enviada em: {d['criado_em'][:16].replace('T', ' ')}")
                    with col_acao:
                        numero_whatsapp = re.sub(r"\D", "", d.get("telefone") or "")
                        if numero_whatsapp and not numero_whatsapp.startswith("55"):
                            numero_whatsapp = f"55{numero_whatsapp}"  # DDI Brasil, exigido pelo link do WhatsApp
                        if numero_whatsapp:
                            st.link_button(
                                "💬 WhatsApp", f"https://wa.me/{numero_whatsapp}", use_container_width=True
                            )
                        if not d["respondida"]:
                            if st.button("✅ Marcar respondida", key=f"resp_duvida_{d['id']}", use_container_width=True):
                                marcar_duvida_respondida(d["id"])
                                st.rerun()
                        else:
                            st.caption("✅ Respondida")

    # ---------------- AVISOS ----------------
    with aba_avisos:
        st.subheader("Avisos gerais")
        st.caption("Aparecem para todos os alunos na tela de Início, em destaque.")

        avisos = listar_todos_avisos()
        if avisos:
            for aviso in avisos:
                with st.container(border=True):
                    col_texto, col_acao = st.columns([4, 1])
                    with col_texto:
                        status_aviso = "" if aviso["ativo"] else " (desativado)"
                        st.write(f"**{aviso['titulo']}**{status_aviso}")
                        st.caption(aviso["mensagem"])
                    with col_acao:
                        if aviso["ativo"]:
                            if st.button("Desativar", key=f"desativar_aviso_{aviso['id']}", use_container_width=True):
                                desativar_aviso(aviso["id"])
                                st.rerun()
        else:
            st.caption("Nenhum aviso cadastrado ainda.")

        st.divider()
        st.subheader("Criar novo aviso")
        with st.form("form_novo_aviso", clear_on_submit=True):
            titulo_aviso = st.text_input("Título *", placeholder="Ex: Novo curso disponível!")
            mensagem_aviso = st.text_area("Mensagem *", placeholder="Escreva o comunicado para os alunos...")
            publicar_aviso = st.form_submit_button("Publicar aviso", type="primary")

        if publicar_aviso:
            if not titulo_aviso or not mensagem_aviso:
                st.warning("Preencha o título e a mensagem.")
            else:
                criar_aviso(titulo_aviso, mensagem_aviso)
                st.success("Aviso publicado! Já aparece na tela de Início dos alunos.")
                st.rerun()

    # ---------------- DESTAQUES ----------------
    with aba_destaques:
        st.subheader("Carrossel de destaques")
        st.caption(
            "Fotos que aparecem em carrossel na tela de Início dos alunos — ex: técnicos "
            "da equipe, trajetória de carreira dentro da empresa. A foto é recortada "
            "automaticamente no formato do carrossel (4:3)."
        )

        destaques = listar_todos_destaques()
        if destaques:
            for destaque in destaques:
                with st.container(border=True):
                    col_foto, col_info, col_editar, col_excluir = st.columns([1, 3, 1, 1])
                    with col_foto:
                        st.image(destaque["foto_url"], use_container_width=True)
                    with col_info:
                        status_destaque = "" if destaque["ativo"] else " (desativado)"
                        st.write(f"**{destaque['titulo']}**{status_destaque}")
                        if destaque.get("descricao"):
                            st.caption(destaque["descricao"])
                        st.caption(f"Ordem: {destaque['ordem']}")
                    with col_editar:
                        if st.button("✏️ Editar", key=f"editar_destaque_btn_{destaque['id']}", use_container_width=True):
                            st.session_state["destaque_em_edicao"] = destaque["id"]
                            st.rerun()
                    with col_excluir:
                        if st.button("🗑️ Excluir", key=f"excluir_destaque_btn_{destaque['id']}", use_container_width=True):
                            st.session_state["destaque_para_excluir"] = destaque["id"]
                            st.rerun()

                    if st.session_state.get("destaque_para_excluir") == destaque["id"]:
                        st.warning(f"Tem certeza que quer excluir **{destaque['titulo']}** do carrossel?")
                        col_sim, col_nao = st.columns(2)
                        with col_sim:
                            if st.button("Sim, excluir", key=f"confirma_excluir_destaque_{destaque['id']}", type="primary", use_container_width=True):
                                excluir_destaque(destaque["id"], destaque["caminho_storage"])
                                st.session_state.pop("destaque_para_excluir", None)
                                st.success("Destaque excluído.")
                                st.rerun()
                        with col_nao:
                            if st.button("Cancelar", key=f"cancela_excluir_destaque_{destaque['id']}", use_container_width=True):
                                st.session_state.pop("destaque_para_excluir", None)
                                st.rerun()

                    if st.session_state.get("destaque_em_edicao") == destaque["id"]:
                        with st.form(f"form_editar_destaque_{destaque['id']}"):
                            novo_titulo_destaque = st.text_input("Título *", value=destaque["titulo"])
                            nova_descricao_destaque = st.text_area("Descrição", value=destaque.get("descricao") or "")
                            nova_ordem_destaque = st.number_input("Ordem", min_value=1, value=destaque["ordem"])
                            novo_ativo_destaque = st.checkbox("Ativo (aparece no carrossel)", value=destaque["ativo"])
                            nova_foto_destaque = st.file_uploader(
                                "Trocar foto (opcional)", type=["png", "jpg", "jpeg"],
                                help="Deixe em branco para manter a foto atual.",
                            )
                            col_salvar, col_cancelar = st.columns(2)
                            with col_salvar:
                                salvar_edicao_destaque = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                            with col_cancelar:
                                cancelar_edicao_destaque = st.form_submit_button("Cancelar", use_container_width=True)

                        if salvar_edicao_destaque:
                            if not novo_titulo_destaque:
                                st.warning("Informe o título.")
                            else:
                                editar_destaque(
                                    destaque["id"], novo_titulo_destaque, nova_descricao_destaque,
                                    int(nova_ordem_destaque), novo_ativo_destaque,
                                    destaque["caminho_storage"],
                                    nova_foto_destaque.getvalue() if nova_foto_destaque else None,
                                )
                                st.session_state.pop("destaque_em_edicao", None)
                                st.success("Destaque atualizado.")
                                st.rerun()
                        if cancelar_edicao_destaque:
                            st.session_state.pop("destaque_em_edicao", None)
                            st.rerun()
        else:
            st.caption("Nenhum destaque cadastrado ainda.")

        st.divider()
        st.subheader("Adicionar destaque")
        with st.form("form_novo_destaque", clear_on_submit=True):
            titulo_destaque = st.text_input("Título *", placeholder="Ex: João Silva — Técnico de Fibra Óptica")
            descricao_destaque = st.text_area(
                "Descrição (opcional)",
                placeholder="Ex: Na empresa há 6 anos, começou como auxiliar e hoje é supervisor regional.",
            )
            ordem_destaque = st.number_input("Ordem de exibição", min_value=1, value=len(destaques) + 1)
            foto_destaque = st.file_uploader("Foto *", type=["png", "jpg", "jpeg"])
            salvar_destaque = st.form_submit_button("Adicionar ao carrossel", type="primary")

        if salvar_destaque:
            if not titulo_destaque or foto_destaque is None:
                st.warning("Preencha o título e escolha uma foto.")
            else:
                criar_destaque(titulo_destaque, descricao_destaque, foto_destaque.getvalue(), int(ordem_destaque))
                st.success(f"Destaque '{titulo_destaque}' adicionado ao carrossel!")
                st.rerun()
