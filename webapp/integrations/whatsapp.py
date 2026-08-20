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
import requests

from utils.helpers import obter_segredo


def _chamar_callmebot(texto: str) -> tuple[bool, str]:
    """
    Faz a chamada HTTP ao CallMeBot e devolve (sucesso, detalhe). O
    CallMeBot às vezes responde HTTP 200 mesmo quando recusa o envio (ex:
    API Key inválida/expirada) — o motivo real vem no corpo da resposta,
    por isso não basta olhar o status_code.
    """
    telefone = obter_segredo("WHATSAPP_PHONE")
    apikey = obter_segredo("WHATSAPP_APIKEY")

    if not telefone or not apikey:
        return False, "WHATSAPP_PHONE ou WHATSAPP_APIKEY está vazio nos Secrets do app."

    try:
        resposta = requests.get(
            "https://api.callmebot.com/whatsapp.php",
            params={"phone": telefone, "text": texto, "apikey": apikey},
            timeout=10,
        )
    except requests.RequestException as erro:
        return False, f"Falha de conexão com o CallMeBot: {erro}"

    corpo = (resposta.text or "").strip()
    if resposta.status_code == 200 and "error" not in corpo.lower():
        return True, corpo[:200]
    return False, f"CallMeBot recusou o envio (HTTP {resposta.status_code}): {corpo[:300] or '(resposta vazia)'}"


def _enviar_mensagem(texto: str) -> bool:
    """
    Função interna que faz a chamada HTTP ao CallMeBot. Retorna True se
    enviou, False se não foi possível (credenciais ausentes, erro de rede
    ou recusa do CallMeBot). Nunca interrompe o fluxo do app: qualquer
    problema é apenas logado no console (visível com
    `journalctl -u cursos-telecom -f` no servidor) em vez de gerar um
    erro na tela do aluno — quem precisa investigar uma falha usa o
    botão "Testar notificação" no painel de administração (aba Dúvidas),
    que chama diagnosticar_configuracao().
    """
    sucesso, detalhe = _chamar_callmebot(texto)
    if not sucesso:
        print(f"[whatsapp] notificação não enviada: {detalhe}")
    return sucesso


def diagnosticar_configuracao() -> tuple[bool, str]:
    """
    Envia uma mensagem de teste real e devolve (sucesso, mensagem em
    português explicando o resultado) — usado pelo botão "Testar
    notificação" no painel de administração, já que _enviar_mensagem
    engole erros de propósito (ver docstring acima).
    """
    sucesso, detalhe = _chamar_callmebot("🔔 Mensagem de teste - Plataforma Norte Tel")
    if sucesso:
        return True, "Mensagem de teste enviada! Confira o WhatsApp do número configurado em WHATSAPP_PHONE."
    return False, detalhe


def notificar_nova_duvida(aluno_nome: str, mensagem: str, telefone: str = None) -> bool:
    """Tenta enviar uma notificação no WhatsApp sobre uma nova dúvida."""
    texto = (
        f"📡 Nova dúvida na Plataforma Norte Tel\n\n"
        f"Aluno: {aluno_nome}\n"
        + (f"Telefone: {telefone}\n" if telefone else "")
        + f"Mensagem: {mensagem}"
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
