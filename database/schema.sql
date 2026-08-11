-- ============================================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS
-- Plataforma de Treinamentos em Telecomunicações
--
-- COMO USAR:
-- 1) Acesse o painel do seu projeto em https://supabase.com
-- 2) Vá em "SQL Editor" -> "New query"
-- 3) Cole TODO o conteúdo deste arquivo e clique em "Run"
-- ============================================================================

-- Extensão necessária para gerar IDs únicos (UUID) automaticamente
create extension if not exists pgcrypto;

-- ----------------------------------------------------------------------------
-- ALUNOS (usuários da plataforma)
-- ----------------------------------------------------------------------------
create table if not exists public.alunos (
    id             uuid primary key default gen_random_uuid(),
    nome_completo  text not null,
    email          text unique not null,
    senha_hash     text not null,       -- senha JAMAIS é salva em texto puro (usamos bcrypt)
    empresa        text,
    cargo          text,
    filial         text,                -- cidade/filial escolhida pelo aluno no cadastro
    is_admin       boolean not null default false,
    ativo          boolean not null default true,   -- acesso pode ser bloqueado pelo admin sem excluir a conta
    deve_trocar_senha            boolean not null default false, -- true após o admin gerar uma senha temporária
    solicitou_redefinicao_senha  boolean not null default false, -- "esqueci minha senha", aguardando o admin
    foto_url       text,                -- link público da foto de perfil (Supabase Storage)
    criado_em      timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- CURSOS
-- ----------------------------------------------------------------------------
create table if not exists public.cursos (
    id             bigint generated always as identity primary key,
    titulo         text not null,
    descricao      text,
    instrutor      text not null,
    carga_horaria  int,                 -- em horas, usado no certificado
    criado_em      timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- MÓDULOS (assuntos dentro de um curso — ex: "Módulo 1: Fundamentos de Fibra")
-- Cada módulo tem seus próprios vídeos e sua própria prova. O aluno só
-- desbloqueia o módulo seguinte depois de concluir o atual (vídeos + prova,
-- se houver). Isso permite cursos mais longos e completos, com carga
-- horária que realmente justifica o certificado.
-- ----------------------------------------------------------------------------
create table if not exists public.modulos (
    id         bigint generated always as identity primary key,
    curso_id   bigint not null references public.cursos(id) on delete cascade,
    titulo     text not null,
    ordem      int not null default 1
);
create index if not exists idx_modulos_curso on public.modulos(curso_id);

-- ----------------------------------------------------------------------------
-- AULAS (vídeos de cada módulo)
-- ----------------------------------------------------------------------------
create table if not exists public.aulas (
    id               bigint generated always as identity primary key,
    modulo_id        bigint not null references public.modulos(id) on delete cascade,
    curso_id         bigint not null references public.cursos(id) on delete cascade,  -- denormalizado, facilita consultas de progresso geral
    titulo           text not null,
    url_video        text not null,     -- link do YouTube (não listado) ou outro host de vídeo
    ordem            int not null default 1,
    duracao_minutos  int default 0
);
create index if not exists idx_aulas_modulo on public.aulas(modulo_id);
create index if not exists idx_aulas_curso on public.aulas(curso_id);

-- ----------------------------------------------------------------------------
-- PROGRESSO DO ALUNO EM CADA AULA
-- ----------------------------------------------------------------------------
create table if not exists public.progresso_aulas (
    id             bigint generated always as identity primary key,
    aluno_id       uuid not null references public.alunos(id) on delete cascade,
    aula_id        bigint not null references public.aulas(id) on delete cascade,
    concluida      boolean not null default false,
    concluida_em   timestamptz,
    unique (aluno_id, aula_id)
);
create index if not exists idx_progresso_aluno on public.progresso_aulas(aluno_id);

-- ----------------------------------------------------------------------------
-- PROVAS (uma avaliação final por curso)
-- ----------------------------------------------------------------------------
create table if not exists public.provas (
    id             bigint generated always as identity primary key,
    modulo_id      bigint not null references public.modulos(id) on delete cascade,
    curso_id       bigint not null references public.cursos(id) on delete cascade,  -- denormalizado, facilita consultas
    titulo         text not null,
    nota_minima    numeric not null default 7.0   -- escala de 0 a 10
);
create unique index if not exists idx_provas_modulo_unico on public.provas(modulo_id);
create index if not exists idx_provas_curso on public.provas(curso_id);

-- ----------------------------------------------------------------------------
-- PERGUNTAS (múltipla escolha, 4 alternativas)
-- ----------------------------------------------------------------------------
create table if not exists public.perguntas (
    id                bigint generated always as identity primary key,
    prova_id          bigint not null references public.provas(id) on delete cascade,
    enunciado         text not null,
    opcao_a           text not null,
    opcao_b           text not null,
    opcao_c           text not null,
    opcao_d           text not null,
    resposta_correta  char(1) not null check (resposta_correta in ('A','B','C','D')),
    ordem             int default 1
);
create index if not exists idx_perguntas_prova on public.perguntas(prova_id);

-- ----------------------------------------------------------------------------
-- RESULTADOS DAS PROVAS REALIZADAS
-- ----------------------------------------------------------------------------
create table if not exists public.resultados_provas (
    id             bigint generated always as identity primary key,
    aluno_id       uuid not null references public.alunos(id) on delete cascade,
    prova_id       bigint not null references public.provas(id) on delete cascade,
    nota           numeric not null,
    aprovado       boolean not null,
    realizada_em   timestamptz not null default now()
);
create index if not exists idx_resultados_aluno on public.resultados_provas(aluno_id);

-- ----------------------------------------------------------------------------
-- CERTIFICADOS EMITIDOS
-- ----------------------------------------------------------------------------
create table if not exists public.certificados (
    id                  bigint generated always as identity primary key,
    aluno_id            uuid not null references public.alunos(id) on delete cascade,
    curso_id            bigint not null references public.cursos(id) on delete cascade,
    codigo_verificacao  text unique not null,
    emitido_em          timestamptz not null default now(),
    unique (aluno_id, curso_id)
);

-- MATERIAIS: fotos, documentos e arquivos disponibilizados para download.
-- O arquivo em si fica no Supabase Storage (bucket "materiais"); aqui só
-- guardamos os metadados (título, categoria, caminho do arquivo etc.).
-- ----------------------------------------------------------------------------
create table if not exists public.materiais (
    id                bigint generated always as identity primary key,
    titulo            text not null,
    descricao         text,
    categoria         text not null,
    nome_arquivo      text not null,
    caminho_storage   text not null,
    tipo_arquivo      text,
    tamanho_bytes     bigint,
    criado_em         timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- DÚVIDAS (perguntas do dia a dia enviadas pelos alunos na página inicial)
-- ----------------------------------------------------------------------------
create table if not exists public.duvidas (
    id            bigint generated always as identity primary key,
    aluno_id      uuid not null references public.alunos(id) on delete cascade,
    aluno_nome    text not null,
    mensagem      text not null,
    respondida    boolean not null default false,
    criado_em     timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- PROGRESSO DO CURSO (quando o aluno começou e quando terminou/foi aprovado)
-- ----------------------------------------------------------------------------
create table if not exists public.progresso_cursos (
    id            bigint generated always as identity primary key,
    aluno_id      uuid not null references public.alunos(id) on delete cascade,
    curso_id      bigint not null references public.cursos(id) on delete cascade,
    iniciado_em   timestamptz not null default now(),
    finalizado_em timestamptz,
    unique (aluno_id, curso_id)
);

-- ----------------------------------------------------------------------------
-- AVISOS (comunicados gerais do admin para todos os alunos, na tela de Início)
-- ----------------------------------------------------------------------------
create table if not exists public.avisos (
    id          bigint generated always as identity primary key,
    titulo      text not null,
    mensagem    text not null,
    ativo       boolean not null default true,
    criado_em   timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- DESTAQUES (carrossel de fotos na tela de Início — ex: técnicos da equipe,
-- trajetória de carreira dentro da empresa). A foto em si fica no Supabase
-- Storage (bucket "destaques"); aqui só guardamos os metadados.
-- ----------------------------------------------------------------------------
create table if not exists public.destaques (
    id                bigint generated always as identity primary key,
    titulo            text not null,           -- ex: nome e cargo do técnico
    descricao         text,                    -- ex: trajetória/tempo de empresa
    foto_url          text not null,
    caminho_storage   text not null,           -- caminho do arquivo no bucket "destaques" (para excluir/trocar a foto)
    ordem             int not null default 1,
    ativo             boolean not null default true,
    criado_em         timestamptz not null default now()
);

-- ============================================================================
-- IMPORTANTE SOBRE SEGURANÇA (leia antes de ir para produção):
--
-- Este projeto acessa o banco usando a chave "service_role" do Supabase,
-- SEMPRE a partir do servidor (Streamlit Cloud), nunca do navegador do aluno.
-- Por isso, o Row Level Security (RLS) das tabelas acima pode ficar desativado
-- (padrão do Postgres) sem risco, desde que você NUNCA:
--   a) coloque a chave "service_role" em código-fonte público, ou
--   b) troque-a pela chave "anon" dentro do app.
--
-- Guarde a chave "service_role" apenas em "Secrets" (Streamlit Cloud) ou no
-- arquivo local .streamlit/secrets.toml (que nunca é enviado ao GitHub).
-- ============================================================================

-- ============================================================================
-- DICA: depois de criar sua própria conta pelo cadastro da plataforma,
-- promova-se a administrador rodando (troque pelo seu e-mail):
--
-- update public.alunos set is_admin = true where email = 'seuemail@empresa.com';
-- ============================================================================
