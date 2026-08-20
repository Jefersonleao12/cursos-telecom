"""
Envio de e-mail via Gmail (SMTP com senha de app).

Usa uma conta do Gmail com uma "senha de app" (gerada em
https://myaccount.google.com/apppasswords, exige verificação em duas etapas
ativada na conta) — não a senha normal da conta. Assim como o WhatsApp
(ver webapp/integrations/whatsapp.py), isso nunca deve travar o fluxo
principal do app: qualquer falha de envio é só logada no console.
"""
import smtplib
from email.message import EmailMessage

from utils.helpers import obter_segredo


def _enviar(destinatario: str, assunto: str, corpo_texto: str) -> bool:
    remetente = obter_segredo("EMAIL_REMETENTE")
    senha_app = obter_segredo("EMAIL_SENHA_APP")

    if not remetente or not senha_app:
        print("[email] não enviado: EMAIL_REMETENTE ou EMAIL_SENHA_APP está vazio nos Secrets do app.")
        return False

    mensagem = EmailMessage()
    mensagem["Subject"] = assunto
    mensagem["From"] = f"Plataforma Norte Tel <{remetente}>"
    mensagem["To"] = destinatario
    mensagem.set_content(corpo_texto)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(remetente, senha_app)
            smtp.send_message(mensagem)
        return True
    except (smtplib.SMTPException, OSError) as erro:
        print(f"[email] falha ao enviar para {destinatario}: {erro}")
        return False


def notificar_curso_parado(aluno: dict, curso: dict, dias_parado: int) -> bool:
    """Manda um lembrete pro aluno que começou um curso e não voltou há alguns dias."""
    assunto = f"Não esqueça: seu curso \"{curso['titulo']}\" está te esperando"
    corpo = (
        f"Olá, {aluno['nome_completo'].split()[0]}!\n\n"
        f"Notamos que você começou o curso \"{curso['titulo']}\" na Plataforma "
        f"Norte Tel, mas já faz {dias_parado} dias que não continua de onde parou.\n\n"
        f"Que tal retomar? Leva só alguns minutos por dia para concluir.\n\n"
        f"Acesse: https://nortetel-cursos.com.br/\n\n"
        f"— Plataforma de Treinamentos Norte Tel"
    )
    return _enviar(aluno["email"], assunto, corpo)


def enviar_email_admin(aluno: dict, assunto: str, mensagem: str) -> bool:
    """Manda uma mensagem livre, escrita pelo admin, pro e-mail de um aluno específico (painel Alunos)."""
    corpo = (
        f"Olá, {aluno['nome_completo'].split()[0]}!\n\n"
        f"{mensagem}\n\n"
        f"— Plataforma de Treinamentos Norte Tel"
    )
    return _enviar(aluno["email"], assunto, corpo)
