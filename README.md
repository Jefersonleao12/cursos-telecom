# 📡 Plataforma de Treinamentos em Telecomunicações

Sistema web gratuito (custo zero) para treinamentos corporativos, com:

- Cadastro/Login de alunos
- Aulas em vídeo (YouTube não listado) com barra de progresso
- Provas de múltipla escolha com nota calculada automaticamente
- Emissão automática de certificado em PDF para aprovados

## Stack

- **Python + Streamlit** — front-end e back-end no mesmo código
- **Supabase (PostgreSQL)** — banco de dados gratuito
- **YouTube (não listado)** — hospedagem dos vídeos
- **Hospedagem do site**: Streamlit Community Cloud ou Render (ver seção abaixo) — o código não depende de nenhum dos dois em particular

## Como rodar localmente

```bash
pip install -r requirements.txt
# preencha .streamlit/secrets.toml com as suas chaves do Supabase
streamlit run app.py
```

## Estrutura

```
app.py                  → ponto de entrada e roteamento
database/schema.sql      → script para criar as tabelas no Supabase
database/repositorio.py  → todas as consultas ao banco
modules/auth.py           → cadastro e login
modules/cursos.py         → lista de cursos, aulas e progresso
modules/provas.py         → avaliações e cálculo de notas
modules/certificado.py    → geração do PDF do certificado
modules/admin.py          → painel para cadastrar cursos/aulas/provas
```

## Hospedagem: Streamlit Community Cloud vs Render

O projeto roda em qualquer um dos dois sem mudar código — as credenciais
(Supabase, WhatsApp) são lidas tanto de `st.secrets` (Streamlit Cloud) quanto
de variáveis de ambiente (Render, ou qualquer outro host), ver
`utils/helpers.obter_segredo`.

**Diferença prática importante:** no plano gratuito do Render, o serviço
"dorme" depois de ~15 min sem acesso e demora uns 30-50s pra acordar no
próximo acesso (o Streamlit Cloud gratuito também dorme, de um jeito
parecido). Pra ficar sempre no ar sem essa espera, é preciso um plano pago do
Render (a partir de uns US$ 7/mês).

### Como migrar para o Render

1. Crie uma conta em https://render.com (dá pra entrar direto com a conta do GitHub).
2. No painel, clique em **New +** → **Blueprint** e conecte este repositório
   (`Jefersonleao12/cursos-telecom`) — o Render já lê o arquivo `render.yaml`
   da raiz do projeto e propõe o serviço sozinho.
   - Alternativa sem Blueprint: **New +** → **Web Service**, escolha o repo, e
     preencha manualmente:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
3. Antes de confirmar a criação, preencha as variáveis de ambiente pedidas
   (mesmos valores que já estão configurados hoje no Streamlit Cloud):
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `WHATSAPP_PHONE` (opcional)
   - `WHATSAPP_APIKEY` (opcional)
4. Clique em **Apply**/**Create Web Service** — o primeiro deploy leva
   alguns minutos. Quando terminar, o Render te dá uma URL do tipo
   `https://cursos-telecom.onrender.com` (ou parecido).
5. **Teste tudo nessa URL antes de desligar o Streamlit Cloud**: login,
   cursos/vídeos, provas, certificado em PDF, materiais, avisos/destaques,
   e o botão de instalar no iPhone (PWA).
6. Avise para atualizar o APK e o EXE com a URL nova — eles têm o endereço
   do Streamlit Cloud fixo no código
   (`mobile-app/.../res/values/strings.xml` e `desktop-app/main.js`) e
   precisam ser recompilados apontando pro Render antes de continuar
   funcionando.
7. Só depois de confirmar que tudo funciona na nova URL (site + apps
   recompilados), desative/exclua o app no Streamlit Community Cloud.

## App para Android (APK) e Windows (EXE)

Além do site, o projeto tem duas "cascas" nativas que abrem
`https://cursos-telecom.streamlit.app/` como se fosse um app instalado —
mantendo o aluno logado entre uma abertura e outra e permitindo baixar o
certificado de capacitação em PDF direto pelo app:

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
Apple. O próprio app detecta quando o aluno está acessando de um iPhone pelo
Safari (e ainda não instalou) e mostra um aviso na tela Início explicando
como instalar (`modules/inicio.py`, `_aviso_instalar_iphone`). O passo a
passo para o aluno é:

1. Abrir `https://cursos-telecom.streamlit.app/` no **Safari** (não funciona
   pelo Chrome/Instagram no iPhone — só o Safari tem essa opção).
2. Tocar no ícone de **Compartilhar** (quadrado com uma seta para cima).
3. Tocar em **"Adicionar à Tela de Início"**.

Os arquivos de suporte ao PWA (ícone, manifest, service worker) já existem
em `static/` e são injetados automaticamente em toda página pelo próprio
`app.py`.

Se no futuro for necessário um app nativo de verdade (App Store), é preciso
antes providenciar uma conta paga da Apple Developer Program — sem isso não
tem como compilar/assinar nada que rode em iPhone de aluno.
