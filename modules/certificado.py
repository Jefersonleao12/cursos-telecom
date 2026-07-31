"""
Módulo de Certificados.

Gera automaticamente o PDF do certificado para alunos aprovados na
avaliação (com nome do aluno, empresa, curso, instrutor/assinatura e
código de verificação) e mantém o histórico de certificados emitidos.
"""
from fpdf import FPDF
import streamlit as st

from database.repositorio import (
    buscar_certificado,
    emitir_certificado,
    melhor_resultado,
    buscar_prova_do_curso,
    listar_cursos,
)
from utils.helpers import gerar_codigo_verificacao, formatar_data_br


AZUL = (20, 60, 110)
CINZA_ESCURO = (30, 30, 30)
CINZA = (110, 110, 110)


class CertificadoPDF(FPDF):
    """Layout do certificado em formato paisagem (A4)."""

    def __init__(self):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.set_auto_page_break(False)

    def moldura(self):
        """Desenha uma borda decorativa dupla ao redor da página."""
        self.set_draw_color(*AZUL)
        self.set_line_width(1.2)
        self.rect(8, 8, self.w - 16, self.h - 16)
        self.set_line_width(0.4)
        self.rect(11, 11, self.w - 22, self.h - 22)


def _linha_centralizada(pdf, texto, tamanho, negrito=False, cor=CINZA_ESCURO, espaco=8, y=None):
    """Escreve uma linha de texto centralizada na página e avança o cursor verticalmente."""
    if y is not None:
        pdf.set_y(y)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B" if negrito else "", tamanho)
    pdf.set_text_color(*cor)
    largura_util = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.cell(largura_util, espaco + 2, texto, align="C")
    pdf.ln(espaco + 2)


def gerar_pdf_certificado(
    nome_aluno: str,
    empresa: str,
    curso_titulo: str,
    instrutor: str,
    carga_horaria,
    nota: float,
    data_emissao: str,
    codigo_verificacao: str,
) -> bytes:
    """Monta o PDF do certificado e retorna os bytes prontos para download."""
    pdf = CertificadoPDF()
    pdf.add_page()
    pdf.moldura()

    _linha_centralizada(pdf, "CERTIFICADO DE CONCLUSÃO", 26, negrito=True, cor=AZUL, espaco=12, y=30)
    _linha_centralizada(pdf, "Plataforma de Treinamentos em Telecomunicações", 13, cor=CINZA, espaco=16)

    _linha_centralizada(pdf, "Certificamos que", 14, espaco=10)
    _linha_centralizada(pdf, nome_aluno.upper(), 22, negrito=True, cor=AZUL, espaco=10)

    texto_empresa = f"da empresa {empresa}, " if empresa else ""
    _linha_centralizada(pdf, f"{texto_empresa}concluiu com aproveitamento o curso", 13, espaco=8)
    _linha_centralizada(pdf, f'"{curso_titulo}"', 17, negrito=True, espaco=8)

    carga_texto = f"com carga horária de {carga_horaria} horas, " if carga_horaria else ""
    _linha_centralizada(pdf, f"{carga_texto}obtendo nota final {nota:.1f} de 10,0.", 13, espaco=16)

    _linha_centralizada(pdf, f"Emitido em {data_emissao}", 12, espaco=6)

    # Linha de assinatura do instrutor
    y_assinatura = pdf.h - 45
    centro = pdf.w / 2
    pdf.set_draw_color(*CINZA_ESCURO)
    pdf.set_line_width(0.3)
    pdf.line(centro - 40, y_assinatura, centro + 40, y_assinatura)

    _linha_centralizada(pdf, instrutor, 12, negrito=True, espaco=6, y=y_assinatura + 2)
    _linha_centralizada(pdf, "Instrutor Responsável", 10, cor=CINZA, espaco=5)

    # Código de verificação (rodapé)
    _linha_centralizada(
        pdf, f"Código de verificação: {codigo_verificacao}", 9, cor=CINZA, espaco=5, y=pdf.h - 16
    )

    saida = pdf.output()
    return bytes(saida)


def _preparar_e_baixar_certificado(aluno_id, curso, resultado):
    """Garante que exista um registro de certificado (cria se necessário) e devolve o PDF em bytes."""
    certificado = buscar_certificado(aluno_id, curso["id"])
    if certificado is None:
        codigo = gerar_codigo_verificacao()
        certificado = emitir_certificado(aluno_id, curso["id"], codigo)

    data_formatada = formatar_data_br(certificado["emitido_em"])

    pdf_bytes = gerar_pdf_certificado(
        nome_aluno=st.session_state["aluno_nome"],
        empresa=st.session_state.get("aluno_empresa", ""),
        curso_titulo=curso["titulo"],
        instrutor=curso["instrutor"],
        carga_horaria=curso.get("carga_horaria"),
        nota=resultado["nota"],
        data_emissao=data_formatada,
        codigo_verificacao=certificado["codigo_verificacao"],
    )
    return pdf_bytes


def tela_certificados():
    st.title("🏆 Meus Certificados")

    aluno_id = st.session_state["aluno_id"]
    cursos = listar_cursos()

    algum_certificado = False

    for curso in cursos:
        prova = buscar_prova_do_curso(curso["id"])
        if prova is None:
            continue

        resultado = melhor_resultado(aluno_id, prova["id"])
        if resultado is None or not resultado["aprovado"]:
            continue

        algum_certificado = True
        with st.container(border=True):
            col_info, col_botao = st.columns([3, 1])
            with col_info:
                st.markdown(f"### {curso['titulo']}")
                st.caption(f"Aprovado com nota {resultado['nota']:.1f} · Instrutor: {curso['instrutor']}")
            with col_botao:
                pdf_bytes = _preparar_e_baixar_certificado(aluno_id, curso, resultado)
                st.download_button(
                    label="⬇️ Baixar PDF",
                    data=pdf_bytes,
                    file_name=f"certificado_{curso['titulo'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"download_{curso['id']}",
                )

    if not algum_certificado:
        st.info(
            "Você ainda não possui certificados. Conclua um curso e seja "
            "aprovado na avaliação para gerar o seu."
        )
