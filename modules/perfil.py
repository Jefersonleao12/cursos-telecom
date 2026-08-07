"""
Módulo 'Meu Perfil'.

Permite que o próprio aluno:
- Troque sua senha
- Atualize empresa / cargo / filial
- Veja seu próprio histórico (cursos, notas nas provas, tempo gasto)
"""
import streamlit as st

from database.repositorio import (
    atualizar_perfil_aluno,
    trocar_senha_aluno,
    atualizar_foto_perfil,
    listar_cursos,
    calcular_progresso_curso,
    obter_tempos_curso,
    buscar_prova_do_curso,
    melhor_resultado,
)
from modules.auth import gerar_hash_senha, verificar_senha
from utils.helpers import FILIAIS


def _formatar_duracao(segundos) -> str:
    """Converte segundos em um texto curto tipo '2d 3h', '4h 12min' ou '18min'."""
    if not segundos:
        return "-"
    segundos = int(segundos)
    dias, resto = divmod(segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, _ = divmod(resto, 60)
    if dias > 0:
        return f"{dias}d {horas}h"
    if horas > 0:
        return f"{horas}h {minutos}min"
    return f"{minutos}min"


def tela_perfil():
    st.title("👤 Meu Perfil")

    aluno_id = st.session_state["aluno_id"]

    aba_dados, aba_senha, aba_historico = st.tabs(["Meus Dados", "Trocar Senha", "Meu Histórico"])

    # ---------------- MEUS DADOS ----------------
    with aba_dados:
        col_foto, col_dados = st.columns([1, 3])
        with col_foto:
            foto_atual = st.session_state.get("aluno_foto_url")
            if foto_atual:
                st.image(foto_atual, width=120)
            else:
                st.markdown(
                    "<div style='width:120px; height:120px; border-radius:50%; "
                    "background:#EAF1FB; display:flex; align-items:center; justify-content:center; "
                    "font-size:2.5rem;'>👤</div>",
                    unsafe_allow_html=True,
                )
        with col_dados:
            st.caption(f"Nome: **{st.session_state['aluno_nome']}**")
            st.caption(f"E-mail: **{st.session_state['aluno_email']}**")
            st.caption("Para trocar nome ou e-mail, entre em contato com o administrador.")

        nova_foto = st.file_uploader(
            "Trocar foto de perfil", type=["jpg", "jpeg", "png"], key="upload_foto_perfil"
        )
        if nova_foto is not None:
            if st.button("📷 Salvar foto de perfil"):
                nova_url = atualizar_foto_perfil(aluno_id, nova_foto.getvalue())
                st.session_state["aluno_foto_url"] = nova_url
                st.success("Foto atualizada com sucesso!")
                st.rerun()

        st.divider()

        with st.form("form_editar_perfil"):
            empresa = st.text_input("Empresa", value=st.session_state.get("aluno_empresa", ""))
            cargo = st.text_input("Cargo / Função", value=st.session_state.get("aluno_cargo", ""))
            filial_atual = st.session_state.get("aluno_filial", "")
            indice_filial = FILIAIS.index(filial_atual) + 1 if filial_atual in FILIAIS else 0
            filial = st.selectbox(
                "Filial (cidade)",
                options=[""] + FILIAIS,
                index=indice_filial,
                format_func=lambda v: "Selecione..." if v == "" else v,
            )
            salvar = st.form_submit_button("Salvar alterações", type="primary")

        if salvar:
            atualizar_perfil_aluno(aluno_id, empresa, cargo, filial)
            st.session_state["aluno_empresa"] = empresa
            st.session_state["aluno_cargo"] = cargo
            st.session_state["aluno_filial"] = filial
            st.success("Dados atualizados com sucesso!")
            st.rerun()

    # ---------------- TROCAR SENHA ----------------
    with aba_senha:
        st.caption("Por segurança, informe sua senha atual antes de definir uma nova.")
        with st.form("form_trocar_senha_perfil", clear_on_submit=True):
            senha_atual = st.text_input("Senha atual *", type="password")
            nova_senha = st.text_input("Nova senha *", type="password", help="Mínimo de 6 caracteres.")
            confirmar = st.text_input("Confirmar nova senha *", type="password")
            trocar = st.form_submit_button("Trocar senha", type="primary")

        if trocar:
            from database.repositorio import buscar_aluno_por_id
            aluno_atual = buscar_aluno_por_id(aluno_id)
            if not senha_atual or not nova_senha:
                st.warning("Preencha todos os campos.")
            elif not verificar_senha(senha_atual, aluno_atual["senha_hash"]):
                st.error("Senha atual incorreta.")
            elif len(nova_senha) < 6:
                st.warning("A nova senha deve ter pelo menos 6 caracteres.")
            elif nova_senha != confirmar:
                st.warning("As senhas não coincidem.")
            else:
                trocar_senha_aluno(aluno_id, gerar_hash_senha(nova_senha))
                st.success("Senha alterada com sucesso!")

    # ---------------- MEU HISTÓRICO ----------------
    with aba_historico:
        cursos = listar_cursos()
        algum_curso_iniciado = False

        for curso in cursos:
            progresso = calcular_progresso_curso(aluno_id, curso["id"])
            tempos = obter_tempos_curso(aluno_id, curso["id"])
            if progresso <= 0 and not tempos:
                continue

            algum_curso_iniciado = True
            with st.container(border=True):
                st.markdown(f"### {curso['titulo']}")
                st.progress(progresso, text=f"{int(progresso * 100)}% das aulas concluídas")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if tempos and tempos.get("finalizado_em"):
                        from datetime import datetime
                        inicio = datetime.fromisoformat(tempos["iniciado_em"])
                        fim = datetime.fromisoformat(tempos["finalizado_em"])
                        st.metric("Tempo até concluir", _formatar_duracao((fim - inicio).total_seconds()))
                    else:
                        st.metric("Status do curso", "Em andamento")

                prova = buscar_prova_do_curso(curso["id"])
                if prova:
                    resultado = melhor_resultado(aluno_id, prova["id"])
                    with col2:
                        if resultado:
                            st.metric("Nota na avaliação", f"{resultado['nota']:.1f}/10")
                        else:
                            st.metric("Nota na avaliação", "-")
                    with col3:
                        if resultado and resultado.get("tempo_gasto_segundos"):
                            st.metric("Tempo na prova", _formatar_duracao(resultado["tempo_gasto_segundos"]))
                        else:
                            st.metric("Tempo na prova", "-")

        if not algum_curso_iniciado:
            st.info("Você ainda não começou nenhum curso. Vá até 'Meus Cursos' para começar!")
