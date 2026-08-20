#!/usr/bin/env bash
# Setup/atualização da Plataforma de Treinamentos em Telecomunicações
# (webapp/, FastAPI) num VPS Ubuntu/Debian. Roda como root.
#
# Seguro rodar de novo a qualquer momento (ex: depois de um git push) —
# reinstala dependências que já estão OK sem problema, e reaproveita o
# domínio já configurado (não volta pro sslip.io sozinho).
#
# O que faz:
#   1) Instala Python 3 + venv + git + Caddy (servidor HTTP com HTTPS
#      automático via Let's Encrypt).
#   2) Clona/atualiza o repositório em /opt/cursos-telecom.
#   3) Cria um venv e instala requirements.txt.
#   4) Na primeira vez, cria /etc/cursos-telecom.env com espaço pra colar
#      os 5 segredos (Supabase, WhatsApp) — o script PARA aqui e pede pra
#      você editar esse arquivo antes de continuar.
#   5) Cria/atualiza um serviço systemd (reinicia sozinho se cair).
#   6) Configura o Caddy como proxy com HTTPS automático.
#
# Como usar: salve este arquivo no servidor (ex: setup-vps.sh), depois:
#   chmod +x setup-vps.sh
#   ./setup-vps.sh

set -euo pipefail

REPO_URL="https://github.com/Jefersonleao12/cursos-telecom.git"
APP_DIR="/opt/cursos-telecom"
ENV_FILE="/etc/cursos-telecom.env"
DOMINIO_FILE="/etc/cursos-telecom-dominio"
SERVICE_NAME="cursos-telecom"
APP_PORT="8000"

if [ -f "$DOMINIO_FILE" ]; then
  DOMINIO="$(cat "$DOMINIO_FILE")"
  echo "==> Domínio já configurado antes, mantendo: $DOMINIO"
  echo "    (pra trocar, edite $DOMINIO_FILE e rode este script de novo)"
else
  echo "==> Detectando IP público..."
  # "-4" força IPv4 de propósito: um domínio sslip.io não aceita ":" (o
  # separador de um endereço IPv6), então pegar o IPv6 aqui geraria um
  # domínio inválido pro Caddy emitir certificado.
  IP_PUBLICO="$(curl -4 -s https://ifconfig.me || curl -4 -s https://api.ipify.org)"
  if [ -z "$IP_PUBLICO" ]; then
    echo "Não consegui detectar o IP público automaticamente."
    read -rp "Digite o IP público deste servidor: " IP_PUBLICO
  fi
  DOMINIO="${IP_PUBLICO}.sslip.io"
  echo "$DOMINIO" > "$DOMINIO_FILE"
  echo "==> Domínio que vai ser usado (grátis, já aponta pra este servidor): $DOMINIO"
  echo "    Se já tem domínio próprio apontando pro IP deste servidor, edite"
  echo "    $DOMINIO_FILE com ele e rode este script de novo antes de continuar."
fi

echo "==> Instalando pacotes básicos (Python, git, curl, Caddy)..."
apt-get update -y
apt-get install -y python3 python3-venv python3-pip git curl debian-keyring debian-archive-keyring apt-transport-https gnupg

if ! command -v caddy >/dev/null 2>&1; then
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
  apt-get update -y
  apt-get install -y caddy
fi

echo "==> Clonando/atualizando o repositório em $APP_DIR..."
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" fetch origin main
  git -C "$APP_DIR" checkout main
  git -C "$APP_DIR" pull origin main
else
  git clone --branch main "$REPO_URL" "$APP_DIR"
fi

echo "==> Criando ambiente virtual e instalando dependências..."
cd "$APP_DIR"
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<'ENVEOF'
# Preencha com as credenciais do Supabase (painel do projeto -> Settings
# -> API) e, se for usar notificação por WhatsApp, do CallMeBot. Sem as
# 3 primeiras a app recusa subir de propósito (ver webapp/config.py:validar()).
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
SESSION_SECRET=
WHATSAPP_PHONE=
WHATSAPP_APIKEY=
ENVEOF
  chmod 600 "$ENV_FILE"
  echo ""
  echo "############################################################"
  echo "  PARE AQUI: edite $ENV_FILE e preencha os 5 valores"
  echo "  (nano $ENV_FILE), depois rode este script de novo pra"
  echo "  continuar a partir do serviço systemd."
  echo "############################################################"
  exit 0
fi

if ! grep -qE '^SUPABASE_URL=.+' "$ENV_FILE"; then
  echo "AVISO: $ENV_FILE existe mas o SUPABASE_URL ainda está vazio. Edite-o (nano $ENV_FILE) e rode o script de novo."
  exit 1
fi

echo "==> Criando serviço systemd..."
cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<SERVICEEOF
[Unit]
Description=Plataforma de Treinamentos em Telecomunicações (webapp/, FastAPI)
After=network.target

[Service]
Type=simple
WorkingDirectory=${APP_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${APP_DIR}/venv/bin/python -m uvicorn webapp.main:app --host 127.0.0.1 --port ${APP_PORT}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

echo "==> Configurando Caddy (proxy + HTTPS automático em $DOMINIO)..."
cat > /etc/caddy/Caddyfile <<CADDYEOF
${DOMINIO} {
    reverse_proxy 127.0.0.1:${APP_PORT}
}
CADDYEOF

systemctl enable caddy
systemctl restart caddy

if command -v ufw >/dev/null 2>&1; then
  echo "==> Abrindo portas 80/443/22 no firewall (ufw)..."
  ufw allow 22/tcp || true
  ufw allow 80/tcp || true
  ufw allow 443/tcp || true
fi

echo ""
echo "############################################################"
echo "  Pronto! Em alguns segundos (emissão do certificado HTTPS):"
echo "  https://${DOMINIO}"
echo ""
echo "  Ver logs da app:    journalctl -u ${SERVICE_NAME} -f"
echo "  Ver logs do Caddy:  journalctl -u caddy -f"
echo "  Status da app:      systemctl status ${SERVICE_NAME}"
echo "############################################################"
