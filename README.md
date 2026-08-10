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
