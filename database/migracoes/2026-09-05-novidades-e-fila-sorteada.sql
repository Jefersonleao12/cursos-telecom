-- ============================================================================
-- RODE ESTE ARQUIVO NO SUPABASE **ANTES** DE PUBLICAR ESTA VERSÃO.
--
-- Onde: painel do Supabase -> SQL Editor -> cole tudo -> Run.
--
-- Por que antes: a aplicação nova grava a fila sorteada de casos nas colunas
-- criadas aqui. Se o código subir sem as colunas, os simuladores quebram na
-- primeira jogada. Rodar este arquivo com a versão ANTIGA no ar não causa
-- problema nenhum — colunas e tabelas novas simplesmente ficam sem uso até
-- a nova versão subir.
--
-- É seguro rodar de novo: tudo aqui usa "if not exists".
-- ============================================================================

-- 1) Ordem SORTEADA dos casos, uma por aluno ---------------------------------
-- Antes os simuladores entregavam os casos sempre na mesma sequência, igual
-- pra todo mundo — o que virava gabarito passado de colega pra colega. Agora
-- cada aluno tem a sua ordem, gravada aqui pra não mudar no meio da partida.
-- (O Simulador de Campo já tinha uma coluna dessas: jogo_campo_progresso.fila_missoes.)

alter table public.jogo_suporte_progresso
    add column if not exists fila_atendimentos jsonb;

alter table public.jogo_suporte_ia_progresso
    add column if not exists fila_atendimentos jsonb;


-- 2) Novidades: o mural técnico da equipe ------------------------------------
-- Configuração nova, solução rápida que alguém descobriu, procedimento que
-- mudou. Aceita texto, vídeo (YouTube/Drive/link direto) ou os dois.

create table if not exists public.novidades (
    id          bigint generated always as identity primary key,
    titulo      text not null,
    conteudo    text,
    video_url   text,
    categoria   text not null default 'Geral',
    autor       text,
    fixada      boolean not null default false,
    ativa       boolean not null default true,
    criado_em   timestamptz not null default now()
);

create index if not exists idx_novidades_recentes
    on public.novidades (ativa, fixada desc, criado_em desc);
