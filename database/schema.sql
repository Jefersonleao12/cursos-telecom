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
    cpf            text unique,         -- login e senha inicial do aluno (cadastro é feito só pelo admin)
    senha_hash     text not null,       -- senha JAMAIS é salva em texto puro (usamos bcrypt)
    empresa        text,
    cargo          text,
    filial         text,                -- cidade/filial do aluno
    telefone       text,                -- WhatsApp de contato
    is_admin       boolean not null default false,
    ativo          boolean not null default true,   -- acesso pode ser bloqueado pelo admin sem excluir a conta
    deve_trocar_senha            boolean not null default false, -- true após o admin gerar uma senha temporária (ou cadastrar o aluno)
    deve_definir_foto            boolean not null default false, -- true até o aluno definir a foto de perfil pela 1ª vez
    solicitou_redefinicao_senha  boolean not null default false, -- "esqueci minha senha", aguardando o admin
    foto_url       text,                -- link público da foto de perfil (Supabase Storage)
    criado_em      timestamptz not null default now()
);
-- Garante as colunas também em bancos que já tinham a tabela "alunos" criada
-- antes desta versão (rodar este script de novo é seguro/idempotente).
alter table public.alunos add column if not exists telefone text;
alter table public.alunos add column if not exists cpf text unique;
alter table public.alunos add column if not exists deve_definir_foto boolean not null default false;

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
    -- Instante em que o aluno abriu a aula pela primeira vez. A app nova
    -- (webapp/) usa isso para checar no SERVIDOR se já passou tempo
    -- suficiente de reprodução antes de liberar a conclusão — os vídeos
    -- agora vêm do Google Drive, que (assim como o YouTube antes) não
    -- expõe o tempo real assistido para o servidor, então o cronômetro
    -- precisa ser contado a partir de quando a aula foi aberta.
    iniciada_em    timestamptz,
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

-- MATERIAIS: fotos, documentos e arquivos disponibilizados como link (ex:
-- pasta/arquivo do Google Drive) para os alunos consultarem. Cada material é
-- um card com ícone + título que abre o link em outra aba.
-- ----------------------------------------------------------------------------
create table if not exists public.materiais (
    id                bigint generated always as identity primary key,
    titulo            text not null,
    descricao         text,
    categoria         text not null,
    link_url          text not null,          -- link do Google Drive (ou outro serviço) com o material
    icone             text not null default '🔗',
    -- colunas antigas (versão com upload de arquivo p/ Supabase Storage),
    -- mantidas só para não quebrar bancos já existentes; não são mais usadas.
    nome_arquivo      text,
    caminho_storage   text,
    tipo_arquivo      text,
    tamanho_bytes     bigint,
    criado_em         timestamptz not null default now()
);
-- Migração de bancos criados antes desta versão (upload de arquivo -> link):
alter table public.materiais add column if not exists link_url text;
alter table public.materiais add column if not exists icone text not null default '🔗';
alter table public.materiais alter column nome_arquivo drop not null;
alter table public.materiais alter column caminho_storage drop not null;

-- ----------------------------------------------------------------------------
-- DÚVIDAS (perguntas do dia a dia enviadas pelos alunos na página inicial)
-- ----------------------------------------------------------------------------
create table if not exists public.duvidas (
    id            bigint generated always as identity primary key,
    aluno_id      uuid not null references public.alunos(id) on delete cascade,
    aluno_nome    text not null,
    telefone      text,                -- telefone de contato do aluno no momento do envio (facilita o retorno)
    mensagem      text not null,
    respondida    boolean not null default false,
    criado_em     timestamptz not null default now()
);
alter table public.duvidas add column if not exists telefone text;

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
-- LEMBRETES DE CURSO PARADO (histórico de e-mails já enviados, pra não
-- lembrar o aluno todo santo dia enquanto ele continuar parado no mesmo
-- curso — ver database/repositorio.py: cursos_parados())
-- ----------------------------------------------------------------------------
create table if not exists public.lembretes_curso_enviados (
    id          bigint generated always as identity primary key,
    aluno_id    uuid not null references public.alunos(id) on delete cascade,
    curso_id    bigint not null references public.cursos(id) on delete cascade,
    enviado_em  timestamptz not null default now()
);
create index if not exists idx_lembretes_aluno_curso on public.lembretes_curso_enviados(aluno_id, curso_id);

-- ----------------------------------------------------------------------------
-- SIMULADOR DE CAMPO (jogo de treinamento com Ordens de Serviço simuladas,
-- acessado pela tela Início) — 1 linha por aluno, guarda em que ponto do
-- jogo ele está pra continuar de onde parou. O conteúdo das O.S. (cenário,
-- perguntas, alternativas) NÃO fica no banco — vive em
-- webapp/data/jogo_campo_missoes.py; aqui só o progresso.
-- ----------------------------------------------------------------------------
create table if not exists public.jogo_campo_progresso (
    aluno_id             uuid primary key references public.alunos(id) on delete cascade,
    tela                 text not null default 'welcome',  -- welcome | mission-intro | decision | feedback | mission-end | game-end
    missao_index         int not null default 0,
    decisao_index        int not null default 0,
    acertos_missao       int not null default 0,
    missoes_completadas  int not null default 0,
    acertos_totais       int not null default 0,
    xp                   int not null default 0,
    opcao_escolhida      int,          -- índice (na ordem embaralhada) da alternativa escolhida na última decisão
    atualizado_em        timestamptz not null default now()
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

-- ----------------------------------------------------------------------------
-- FUNÇÃO: progresso e conclusão de curso pra todos os alunos de uma vez
--
-- Usada pelo Ranking, pelo Dashboard do admin e pela lista de Alunos do
-- admin — telas que precisam ver o progresso de TODO MUNDO ao mesmo tempo.
-- Calcular isso trazendo os dados brutos pro servidor (uma consulta por
-- combinação aluno×curso) virava dezenas/centenas de idas e vindas ao
-- banco, cada uma pagando a latência de rede — visivelmente lento mesmo
-- com bastante CPU sobrando. Rodando dentro do próprio Postgres, vira
-- 1 única consulta, não importa quantos alunos/cursos existam.
--
-- Calcula pra TODOS os alunos (ativos ou não) de propósito: quem chama
-- decide quais alunos filtrar (ex: o Ranking só usa os ativos, mas o
-- Dashboard quer o progresso de todo mundo, incluindo quem foi desativado
-- depois de já ter avançado nos cursos) — filtrar aqui dentro mudaria
-- esse comportamento.
-- ----------------------------------------------------------------------------
create or replace function public.progresso_ranking_dados()
returns table (
    aluno_id uuid,
    curso_id bigint,
    progresso numeric,
    concluido boolean
)
language sql
stable
as $$
with todos_alunos as (
    select id from public.alunos
),
aulas_por_curso as (
    select curso_id, count(*) as total_aulas
    from public.aulas
    group by curso_id
),
aulas_concluidas as (
    select a.curso_id, pa.aluno_id, count(*) as concluidas
    from public.progresso_aulas pa
    join public.aulas a on a.id = pa.aula_id
    where pa.concluida = true
    group by a.curso_id, pa.aluno_id
),
melhor_resultado as (
    select distinct on (rp.aluno_id, rp.prova_id)
        rp.aluno_id, rp.prova_id, rp.aprovado
    from public.resultados_provas rp
    order by rp.aluno_id, rp.prova_id, rp.nota desc, rp.id asc
),
modulo_status as (
    select
        al.id as aluno_id,
        m.id as modulo_id,
        m.curso_id as curso_id,
        (
            exists (select 1 from public.aulas au where au.modulo_id = m.id)
            and not exists (
                select 1 from public.aulas au
                where au.modulo_id = m.id
                and not exists (
                    select 1 from public.progresso_aulas pa
                    where pa.aula_id = au.id and pa.aluno_id = al.id and pa.concluida = true
                )
            )
            and (
                not exists (select 1 from public.provas p where p.modulo_id = m.id)
                or exists (
                    select 1 from public.provas p
                    join melhor_resultado mr on mr.prova_id = p.id and mr.aluno_id = al.id
                    where p.modulo_id = m.id and mr.aprovado = true
                )
            )
        ) as completo
    from todos_alunos al
    cross join public.modulos m
),
curso_concluido as (
    select aluno_id, curso_id,
        bool_and(completo) as todos_completos,
        count(*) as total_modulos
    from modulo_status
    group by aluno_id, curso_id
)
select
    al.id as aluno_id,
    c.id as curso_id,
    coalesce(ac.concluidas::numeric / nullif(apc.total_aulas, 0), 0) as progresso,
    coalesce(cc.todos_completos, false) and coalesce(cc.total_modulos, 0) > 0 as concluido
from todos_alunos al
cross join public.cursos c
left join aulas_por_curso apc on apc.curso_id = c.id
left join aulas_concluidas ac on ac.curso_id = c.id and ac.aluno_id = al.id
left join curso_concluido cc on cc.curso_id = c.id and cc.aluno_id = al.id;
$$;

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
