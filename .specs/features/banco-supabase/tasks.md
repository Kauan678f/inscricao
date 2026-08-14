# Banco de Dados Supabase — Tasks

**Spec**: `.specs/features/banco-supabase/spec.md`
**Status**: Draft

---

## Execution Plan

### Phase 1: Setup (Sequential)

Criação da tabela e configuração de segurança.

```
T1 → T2 → T3
```

> **Nota**: Estas tasks geram scripts SQL e documentação. A execução dos scripts no Supabase Dashboard será feita manualmente pelo usuário ou via API.

---

## Task Breakdown

### T1: Criar script SQL da tabela inscricoes

**What**: Escrever o SQL de criação da tabela `inscricoes` com todos os campos definidos no PRD
**Where**: `.specs/features/banco-supabase/schema.sql` (referência)
**Depends on**: None
**Requirement**: DB-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Script SQL com CREATE TABLE `inscricoes`
- [x] Campo `id` como UUID com default `gen_random_uuid()`
- [x] Campo `created_at` como timestamptz com default `now()`
- [x] Campo `cristao` como boolean NOT NULL
- [x] Campo `tempo_cristao` como text NOT NULL
- [x] Campo `batizado_aguas` como boolean NOT NULL
- [x] Campo `batizado_espirito` como text NOT NULL
- [x] Campo `em_comunhao` como boolean NOT NULL
- [x] Campo `tempo_comunhao` como text (NULLABLE — vazio quando não em comunhão)
- [x] Campo `motivo` como text NOT NULL
- [x] Primary key em `id`

**Verify**: Copiar SQL no Supabase SQL Editor → executar → tabela aparece no Table Editor.

**Commit**: `feat(db): create inscricoes table schema`

---

### T2: Criar script SQL de RLS (Row Level Security)

**What**: Escrever as políticas de RLS para permitir INSERT anônimo e bloquear SELECT público
**Where**: `.specs/features/banco-supabase/rls.sql` (referência)
**Depends on**: T1
**Requirement**: DB-03

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [ ] `ALTER TABLE inscricoes ENABLE ROW LEVEL SECURITY`
- [ ] Policy "allow_anon_insert": permite INSERT para role `anon`
- [ ] Policy "deny_anon_select": nega SELECT para role `anon`
- [ ] Comentários explicando que SELECT será permitido apenas via service_role key
- [ ] Script pode ser executado no Supabase SQL Editor

**Verify**: Após executar, tentar SELECT via API com anon key → retorna vazio. Tentar INSERT via formulário → funciona.

**Commit**: `feat(db): configure RLS policies for inscricoes`

---

### T3: Documentar configuração do Supabase

**What**: Criar documento com instruções passo a passo para configurar o Supabase (criar projeto, executar SQLs, obter keys)
**Where**: `.specs/features/banco-supabase/setup-guide.md`
**Depends on**: T1, T2
**Requirement**: DB-01, DB-02, DB-03

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [ ] Instruções para criar projeto no Supabase (se não existir)
- [ ] Instruções para executar schema.sql no SQL Editor
- [ ] Instruções para executar rls.sql no SQL Editor
- [ ] Instruções para obter URL, anon key e service_role key
- [ ] Instruções para colar as keys nos arquivos JS do projeto

**Verify**: Seguir o guia do zero resulta em Supabase configurado corretamente.

**Commit**: `docs: add Supabase setup guide`

---

## Parallel Execution Map

```
Phase 1 (Sequential):
  T1 ──→ T2 ──→ T3
```

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Schema SQL | 1 script SQL | ✅ Granular |
| T2: RLS SQL | 1 script SQL | ✅ Granular |
| T3: Setup guide | 1 documento | ✅ Granular |
