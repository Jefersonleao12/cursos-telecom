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
- **Streamlit Community Cloud** — hospedagem do site, de graça

## Como rodar localmente

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.exemplo .streamlit/secrets.toml
# edite o secrets.toml com as suas chaves do Supabase
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
