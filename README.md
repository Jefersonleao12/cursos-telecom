# 📡 Plataforma de Treinamentos em Telecomunicações — Norte Tel

Sistema web para treinamentos corporativos, com:

- Login de alunos por CPF (sem autocadastro)
- Aulas em vídeo (YouTube ou Google Drive) com desbloqueio sequencial e barra de progresso
- Provas de múltipla escolha com nota calculada automaticamente
- Emissão automática de certificado em PDF para quem conclui o curso
- Painel de administração completo (cursos, módulos, aulas, provas, alunos, filiais, materiais, avisos, destaques e dúvidas)

## Stack

- **Python + FastAPI** — back-end (ASGI, servido por Uvicorn)
- **Jinja2 + Alpine.js + Tailwind CSS** — front-end renderizado no servidor. O CSS e o Alpine são
  servidos pelo próprio site (`static/css/app.css` e `static/js/alpine.min.js`), não por CDN — o
  servidor **não** precisa de Node.js pra rodar, só quem for regerar o CSS (ver abaixo)
- **Supabase (PostgreSQL)** — banco de dados
- **YouTube / Google Drive** — hospedagem dos vídeos das aulas
- **Hospedagem do site**: VPS próprio (Ubuntu + Caddy, ver seção abaixo), domínio `nortetel-cursos.com.br`

## Como rodar localmente

```bash
pip install -r requirements.txt

export SUPABASE_URL="..."
export SUPABASE_SERVICE_KEY="..."
export SESSION_SECRET="..."          # string aleatória qualquer, só pra assinar o cookie de sessão
export WHATSAPP_PHONE="..."          # opcional
export WHATSAPP_APIKEY="..."         # opcional
export EMAIL_REMETENTE="..."         # opcional, Gmail usado pro lembrete de curso parado
export EMAIL_SENHA_APP="..."         # opcional, senha de app do Gmail (não a senha normal)

uvicorn webapp.main:app --reload
```

O app abre em `http://127.0.0.1:8000`.

## Regerar o CSS (só quando mexer em template)

O visual usa Tailwind. O arquivo final já vem pronto e commitado em
`static/css/app.css`, então **o servidor não precisa de Node.js**. Mas o Tailwind
só inclui no CSS as classes que ele encontra nos templates — então, se você usar
uma classe nova em algum `.html`, precisa gerar o CSS de novo:

```bash
npm install          # só na primeira vez
npm run build:css    # regera static/css/app.css
```

Depois é só commitar o `static/css/app.css` junto com a mudança no template.
Se esquecer, a classe nova simplesmente não terá efeito na tela.

Para atualizar o Alpine.js: `npm install alpinejs@<versão> && npm run copy:alpine`.

## Estrutura

```
webapp/
  main.py                  → instância FastAPI, monta routers e arquivos estáticos, /healthz
  config.py                → leitura de configuração (variáveis de ambiente)
  deps.py                  → dependências de rota (exigir login, exigir admin)
  middleware.py            → redireciona pra trocar-senha-obrigatória / definir-foto-obrigatória

  auth/                    → login por CPF, cookie de sessão (HMAC + bcrypt)
  routers/                 → uma tela do aluno por arquivo (início, cursos, provas,
                              certificados, ranking, materiais, perfil)
  routers/admin/           → uma aba do painel de admin por arquivo
  services/                → geração do certificado em PDF, identificação de vídeo (YouTube/Drive)
  integrations/            → notificação via WhatsApp (CallMeBot)
  templates/                → HTML (Jinja2), com fragmentos pra HTMX em templates/partials/

database/
  repositorio.py            → todas as consultas ao banco
  supabase_client.py         → cliente Supabase
  cache.py                   → cache com TTL das consultas mais repetidas
  schema.sql                 → schema das tabelas e funções SQL do Postgres

utils/helpers.py            → funções utilitárias (validação de CPF, leitura de segredos etc.)
scripts/setup-vps.sh        → script de setup/atualização do servidor de produção
static/                     → CSS, ícones, manifest.json e service worker (PWA)
```

## Hospedagem: VPS próprio

O site roda num VPS (Ubuntu 24.04) como serviço systemd (`cursos-telecom.service`),
atrás do [Caddy](https://caddyserver.com/) (HTTPS automático via Let's Encrypt) no
domínio `nortetel-cursos.com.br`.

### Primeira instalação

No servidor novo, como root:

```bash
curl -fsSL https://raw.githubusercontent.com/Jefersonleao12/cursos-telecom/main/scripts/setup-vps.sh -o setup-vps.sh
bash setup-vps.sh
```

O script instala Python/venv/git/Caddy, clona o repositório, cria o arquivo de
credenciais `/etc/cursos-telecom.env` (edite com `nano` e preencha
`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SESSION_SECRET` e, opcionalmente,
`WHATSAPP_PHONE`/`WHATSAPP_APIKEY`), cria o serviço systemd e configura o
Caddy para HTTPS automático.

### Atualizar produção (deploy de uma mudança)

```bash
cd /opt/cursos-telecom   # ou o caminho onde o script clonou o repo
git pull origin main
sudo systemctl restart cursos-telecom
```

### Comandos úteis

```bash
sudo systemctl status cursos-telecom      # status do serviço
sudo journalctl -u cursos-telecom -f      # logs em tempo real
sudo systemctl restart cursos-telecom     # reiniciar depois de um deploy
```

## Lembrete de curso parado (e-mail)

Todo dia às 8h (horário de Rondônia), `scripts/lembretes_diarios.py` roda
via cron e manda um e-mail para quem começou um curso e ficou 3 dias sem
voltar (não repete o lembrete todo dia — só de novo depois de outros 3 dias
parado). O `setup-vps.sh` já agenda isso sozinho na primeira instalação.

Pra funcionar, preencha em `/etc/cursos-telecom.env`:

- `EMAIL_REMETENTE` — um Gmail (ex: crie um `nortetel.treinamentos@gmail.com`)
- `EMAIL_SENHA_APP` — uma "senha de app" gerada em
  https://myaccount.google.com/apppasswords (exige verificação em duas
  etapas ativada na conta; **não** é a senha normal do Gmail)

Sem essas duas variáveis, o lembrete simplesmente não é enviado (fica só
logado em `/var/log/cursos-telecom-lembretes.log`) — o resto do site
continua funcionando normalmente.

```bash
tail -f /var/log/cursos-telecom-lembretes.log   # ver os envios de hoje
crontab -l                                       # conferir o agendamento
```

## App para Android (APK) e Windows (EXE)

Além do site, o projeto tem duas "cascas" nativas que abrem
`https://nortetel-cursos.com.br/` como se fosse um app instalado — mantendo
o aluno logado entre uma abertura e outra e permitindo baixar o certificado
de capacitação em PDF direto pelo app:

```
mobile-app/    → projeto Android (Kotlin + WebView)
desktop-app/   → projeto Electron (Windows/.exe)
```

Os dois são compilados automaticamente pelo GitHub Actions
(`.github/workflows/build-apps.yml`) a cada mudança nessas pastas, ou
manualmente pela aba **Actions → Build APK e EXE → Run workflow**. Depois de
rodar, baixe o `.apk` ou o `.exe` na seção **Artifacts** daquela execução.

## App para iPhone (iOS)

A Apple não permite instalar um app compilado em iPhone sem uma conta paga
de desenvolvedor (Apple Developer Program, US$ 99/ano) e assinatura digital
— não existe "sideload livre" como no Android. Por isso, para os alunos que
usam iPhone, a plataforma já funciona como um **PWA (Progressive Web App)**:
instalando pelo Safari, o aluno ganha um ícone próprio na tela de início e o
site abre em tela cheia, sem a barra do navegador, como se fosse um app.

Isso já está pronto e é gratuito — sem custo, sem espera de aprovação da
Apple. O passo a passo para o aluno é:

1. Abrir `https://nortetel-cursos.com.br/` no **Safari** (não funciona pelo
   Chrome/Instagram no iPhone — só o Safari tem essa opção).
2. Tocar no ícone de **Compartilhar** (quadrado com uma seta para cima).
3. Tocar em **"Adicionar à Tela de Início"**.

Os arquivos de suporte ao PWA (ícone, manifest, service worker) ficam em
`static/` e são referenciados diretamente pelas páginas em `webapp/templates/`.

Se no futuro for necessário um app nativo de verdade (App Store), é preciso
antes providenciar uma conta paga da Apple Developer Program — sem isso não
tem como compilar/assinar nada que rode em iPhone de aluno.
