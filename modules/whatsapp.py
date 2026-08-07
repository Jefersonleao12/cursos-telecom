"""
Módulo de Notificação via WhatsApp.

Usa o CallMeBot (https://www.callmebot.com/blog/free-api-whatsapp-messages/),
um serviço gratuito que envia mensagens de WhatsApp para um número pessoal
através de uma chamada HTTP simples — sem precisar de conta comercial paga
(Meta Business API) ou de serviços como Twilio.

IMPORTANTE: é um serviço de terceiros, gratuito e não-oficial. Ele funciona
bem para notificações pontuais como esta, mas pode ter instabilidades e um
pequeno limite de mensagens por minuto. Por isso, a dúvida do aluno é SEMPRE
salva no banco de dados primeiro (ver database/repositorio.py) — o WhatsApp
é um "bônus" de agilidade, não a única forma de a pergunta chegar até você.
"""
import streamlit as st
import requests


def _enviar_mensagem(texto: str) -> bool:
    """
    Função interna que faz a chamada HTTP ao CallMeBot. Retorna True se
    enviou, False se não foi possível (credenciais ausentes ou erro de rede).
    Nunca interrompe o fluxo do app: qualquer erro é silenciado aqui.
    """
    try:
        telefone = st.secrets["WHATSAPP_PHONE"]
        apikey = st.secrets["WHATSAPP_APIKEY"]
    except (KeyError, FileNotFoundError):
        return False

    try:
        resposta = requests.get(
            "https://api.callmebot.com/whatsapp.php",
            params={"phone": telefone, "text": texto, "apikey": apikey},
            timeout=10,
        )
        return resposta.status_code == 200
    except requests.RequestException:
        return False


def notificar_nova_duvida(aluno_nome: str, mensagem: str) -> bool:
    """Tenta enviar uma notificação no WhatsApp sobre uma nova dúvida."""
    texto = (
        f"📡 Nova dúvida na Plataforma Norte Tel\n\n"
        f"Aluno: {aluno_nome}\n"
        f"Mensagem: {mensagem}"
    )
    return _enviar_mensagem(texto)


def notificar_pedido_redefinicao_senha(aluno_nome: str, aluno_email: str) -> bool:
    """Tenta enviar uma notificação no WhatsApp sobre um pedido de 'esqueci minha senha'."""
    texto = (
        f"🔑 Pedido de redefinição de senha\n\n"
        f"Aluno: {aluno_nome}\n"
        f"E-mail: {aluno_email}\n\n"
        f"Acesse o Painel de Administração > Alunos para gerar uma nova senha."
    )
    return _enviar_mensagem(texto)
