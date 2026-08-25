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


def _enviar(destinatario: str, assunto: str, corpo_texto: str) -> tuple[bool, str]:
    """
    Devolve (sucesso, detalhe). O detalhe distingue "não configurado" de
    "configurado mas o Gmail recusou o login" de "erro de conexão" — sem
    isso, qualquer falha de envio (ex: senha de app errada, ou revogada
    pelo Google) aparecia pro admin como se as variáveis estivessem vazias,
    o que manda quem for investigar atrás da causa errada (mesmo problema
    que _chamar_callmebot resolve pro WhatsApp, ver webapp/integrations/whatsapp.py).
    """
    remetente = obter_segredo("EMAIL_REMETENTE")
    senha_app = obter_segredo("EMAIL_SENHA_APP")

    if not remetente or not senha_app:
        detalhe = "EMAIL_REMETENTE ou EMAIL_SENHA_APP está vazio nos Secrets do app."
        print(f"[email] não enviado: {detalhe}")
        return False, detalhe

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
        return True, ""
    except smtplib.SMTPAuthenticationError as erro:
        detalhe = f"Gmail recusou o login (usuário ou senha de app incorretos): {erro}"
        print(f"[email] falha ao enviar para {destinatario}: {detalhe}")
        return False, detalhe
    except (smtplib.SMTPException, OSError) as erro:
        detalhe = f"Erro ao enviar: {erro}"
        print(f"[email] falha ao enviar para {destinatario}: {detalhe}")
        return False, detalhe


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
    sucesso, _detalhe = _enviar(aluno["email"], assunto, corpo)
    return sucesso


def enviar_email_admin(aluno: dict, assunto: str, mensagem: str) -> tuple[bool, str]:
    """Manda uma mensagem livre, escrita pelo admin, pro e-mail de um aluno específico (painel Alunos)."""
    corpo = (
        f"Olá, {aluno['nome_completo'].split()[0]}!\n\n"
        f"{mensagem}\n\n"
        f"— Plataforma de Treinamentos Norte Tel"
    )
    return _enviar(aluno["email"], assunto, corpo)
