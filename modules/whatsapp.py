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


def notificar_nova_duvida(aluno_nome: str, mensagem: str) -> bool:
    """
    Tenta enviar uma notificação no WhatsApp sobre uma nova dúvida.
    Retorna True se a mensagem foi enviada, False se não foi possível
    (por exemplo, se as credenciais do CallMeBot não estiverem configuradas).
    Nunca interrompe o fluxo do app: qualquer erro é silenciado aqui.
    """
    try:
        telefone = st.secrets["WHATSAPP_PHONE"]
        apikey = st.secrets["WHATSAPP_APIKEY"]
    except (KeyError, FileNotFoundError):
        return False

    texto = (
        f"📡 Nova dúvida na Plataforma Norte Tel\n\n"
        f"Aluno: {aluno_nome}\n"
        f"Mensagem: {mensagem}"
    )

    try:
        resposta = requests.get(
            "https://api.callmebot.com/whatsapp.php",
            params={"phone": telefone, "text": texto, "apikey": apikey},
            timeout=10,
        )
        return resposta.status_code == 200
    except requests.RequestException:
        return False
