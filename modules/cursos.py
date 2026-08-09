"""
Módulo de Cursos, Módulos e Aulas.

Mostra a lista de cursos disponíveis e a tela de um curso, agora organizada
em MÓDULOS (assuntos) sequenciais: o aluno assiste os vídeos de um módulo,
faz a prova daquele módulo (se houver) e só então o módulo seguinte é
desbloqueado — até concluir o curso inteiro.
"""
import time

import streamlit as st

from database.repositorio import (
    listar_cursos,
    buscar_curso,
    listar_modulos_do_curso,
    listar_aulas_do_modulo,
    aulas_concluidas_do_aluno,
    aulas_concluidas_do_modulo,
    calcular_progresso_curso,
    marcar_aula_concluida,
    registrar_inicio_curso,
    finalizar_progresso_curso,
    buscar_prova_do_modulo,
    modulo_esta_completo,
)
from modules.provas import renderizar_prova_modulo


def _selo_status(progresso: float) -> str:
    """Retorna um selo HTML colorido de acordo com o progresso do curso."""
    if progresso >= 1.0:
        cor_fundo, cor_texto, texto = "#E3F5E9", "#1E7A46", "✅ Concluído"
    elif progresso > 0:
        cor_fundo, cor_texto, texto = "#FFF4D9", "#8A6100", "⏳ Em andamento"
    else:
        cor_fundo, cor_texto, texto = "#EDEFF5", "#4A4F5E", "🆕 Não iniciado"
    return (
        f"<span style='background:{cor_fundo}; color:{cor_texto}; padding:3px 10px; "
        f"border-radius:999px; font-size:0.78rem; font-weight:600;'>{texto}</span>"
    )


def tela_lista_cursos():
    st.title("📚 Meus Cursos")

    cursos = listar_cursos()
    if not cursos:
        st.info("Nenhum curso disponível no momento. Volte em breve!")
        return

    aluno_id = st.session_state["aluno_id"]

    termo_busca = st.text_input(
        "🔎 Buscar curso",
        placeholder="Digite o nome do curso...",
        label_visibility="collapsed",
    )
    if termo_busca:
        termo = termo_busca.lower().strip()
        cursos = [c for c in cursos if termo in c["titulo"].lower()]
        if not cursos:
            st.warning("Nenhum curso encontrado com esse nome.")
            return

    st.write("")

    for curso in cursos:
        progresso = calcular_progresso_curso(aluno_id, curso["id"])
        with st.container(border=True):
            col_info, col_botao = st.columns([4, 1])
            with col_info:
                st.markdown(f"### {curso['titulo']}")
                st.markdown(_selo_status(progresso), unsafe_allow_html=True)
                st.caption(f"Instrutor: {curso['instrutor']} · Carga horária: {curso.get('carga_horaria', '-')}h")
                if curso.get("descricao"):
                    st.write(curso["descricao"])
                st.progress(progresso, text=f"{int(progresso * 100)}% concluído")
            with col_botao:
                st.write("")
                st.write("")
                if st.button("Acessar curso", key=f"acessar_{curso['id']}", use_container_width=True):
                    st.session_state["curso_atual_id"] = curso["id"]
                    st.session_state["pagina_atual"] = "detalhe_curso"
                    st.rerun()


def _bloco_aula(aluno_id: str, aula: dict, aula_concluida: bool):
    """Desenha o vídeo de uma aula e o botão de concluir (com a trava de tempo mínimo)."""
    st.video(aula["url_video"])
    if aula_concluida:
        st.success("Você já concluiu esta aula.")
        return

    # Trava simples: exige que um tempo mínimo (baseado na duração cadastrada
    # da aula) tenha passado desde que o aluno abriu o vídeo, antes de
    # liberar o botão de concluir. Não é uma prova cabal de que ele assistiu
    # (não temos esse controle com um link do YouTube), mas evita o "clique
    # instantâneo" que marcava a aula como concluída sem sequer abrir o vídeo.
    chave_abertura = f"abertura_aula_{aula['id']}"
    if chave_abertura not in st.session_state:
        st.session_state[chave_abertura] = time.time()

    duracao_min = aula.get("duracao_minutos") or 0
    segundos_exigidos = int(duracao_min * 60 * 0.9)  # 90% da duração cadastrada
    segundos_passados = int(time.time() - st.session_state[chave_abertura])

    if segundos_exigidos > 0 and segundos_passados < segundos_exigidos:
        faltam = segundos_exigidos - segundos_passados
        minutos_faltam = faltam // 60 + 1
        st.button(
            f"Marcar aula como concluída (assista mais ~{minutos_faltam} min)",
            key=f"concluir_{aula['id']}",
            disabled=True,
            use_container_width=True,
        )
        if st.button("🔄 Já assisti, verificar novamente", key=f"verificar_{aula['id']}"):
            st.rerun()
    else:
        if st.button("Marcar aula como concluída", key=f"concluir_{aula['id']}", type="primary"):
            marcar_aula_concluida(aluno_id, aula["id"])
            st.toast("Aula concluída! 🎉", icon="✅")
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
    modulos = listar_modulos_do_curso(curso_id)

    if not modulos:
        st.info("Este curso ainda não possui módulos cadastrados.")
        return

    # Registra (uma única vez por sessão) o instante em que o aluno começou
    # este curso, usado depois para calcular quanto tempo ele levou para concluir.
    if not st.session_state.get(f"inicio_registrado_curso_{curso_id}"):
        registrar_inicio_curso(aluno_id, curso_id)
        st.session_state[f"inicio_registrado_curso_{curso_id}"] = True

    progresso_geral = calcular_progresso_curso(aluno_id, curso_id)
    st.progress(progresso_geral, text=f"Progresso geral do curso: {int(progresso_geral * 100)}%")
    st.caption(f"{len(modulos)} módulo(s) neste curso")

    st.divider()

    # Percorre os módulos em ordem. Cada um só é liberado depois que o
    # anterior estiver 100% completo (aulas + prova, se houver).
    modulo_anterior_completo = True
    curso_recem_concluido = False
    status_dos_modulos = []  # guarda o "completo" de cada módulo já calculado,
                              # para não recalcular tudo de novo no final (evita
                              # dobrar as consultas ao banco a cada clique).

    for indice, modulo in enumerate(modulos, start=1):
        desbloqueado = modulo_anterior_completo
        completo = modulo_esta_completo(aluno_id, modulo["id"]) if desbloqueado else False
        status_dos_modulos.append(completo)

        if not desbloqueado:
            st.markdown(f"##### 🔒 Módulo {indice}: {modulo['titulo']}")
            st.caption("Conclua o módulo anterior para desbloquear este.")
            st.write("")
            modulo_anterior_completo = False
            continue

        icone = "✅" if completo else "▶️"
        with st.expander(f"{icone} Módulo {indice}: {modulo['titulo']}", expanded=not completo):
            aulas = listar_aulas_do_modulo(modulo["id"])

            if not aulas:
                st.caption("Este módulo ainda não possui aulas cadastradas.")
            else:
                concluidas_modulo = set(aulas_concluidas_do_modulo(aluno_id, modulo["id"]))
                for aula in aulas:
                    aula_concluida = aula["id"] in concluidas_modulo
                    st.markdown(f"**Aula {aula['ordem']}: {aula['titulo']}**")
                    _bloco_aula(aluno_id, aula, aula_concluida)
                    st.write("")

                todas_aulas_concluidas = len(concluidas_modulo) == len(aulas)

                if todas_aulas_concluidas:
                    prova = buscar_prova_do_modulo(modulo["id"])
                    if prova:
                        st.divider()
                        st.markdown(f"#### 📝 Avaliação — {prova['titulo']}")
                        aprovado_agora = renderizar_prova_modulo(aluno_id, prova)
                        if aprovado_agora:
                            status_dos_modulos[-1] = True  # este módulo acabou de ficar completo
                            if all(status_dos_modulos) and len(status_dos_modulos) == len(modulos):
                                finalizar_progresso_curso(aluno_id, curso_id)
                                curso_recem_concluido = True
                            st.rerun()
                    elif not completo:
                        st.success("Módulo concluído! Siga para o próximo. 🎉")

        modulo_anterior_completo = completo

    st.divider()

    curso_completo_agora = len(status_dos_modulos) == len(modulos) and all(status_dos_modulos)

    if curso_completo_agora:
        st.success("🎉 Parabéns! Você concluiu TODOS os módulos deste curso.")
        if st.button("Ver meu certificado de capacitação", type="primary"):
            st.session_state["pagina_atual"] = "certificados"
            st.rerun()
    else:
        st.info("Conclua os vídeos e as avaliações de cada módulo, em ordem, para liberar o certificado de capacitação.")
