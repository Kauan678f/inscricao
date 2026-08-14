# Banco de Dados Supabase — Specification

## Problem Statement

As inscrições enviadas pelo formulário público precisam ser armazenadas de forma persistente e segura em um banco de dados. O Supabase será utilizado como backend-as-a-service, com a tabela `inscricoes` no PostgreSQL e regras de acesso configuradas para proteger os dados.

## Goals

- [ ] Criar tabela `inscricoes` com a estrutura definida no PRD
- [ ] Configurar RLS (Row Level Security) para proteger dados contra acesso público
- [ ] Permitir INSERT público (anônimo) para inscrições
- [ ] Permitir SELECT apenas para sessões autenticadas (preparar para V2)
- [ ] Integrar o JavaScript client do Supabase via CDN

## Out of Scope

| Feature                         | Reason                                         |
| ------------------------------- | ---------------------------------------------- |
| Supabase Auth integrado ao app  | V1 usa login mockado; Auth real na V2          |
| Triggers/Functions no Supabase  | Não necessário na V1                           |
| Storage do Supabase             | Sem upload de arquivos na V1                   |
| Edge Functions                  | Sem servidor/serverless                        |

---

## User Stories

### P1: Armazenamento de Inscrições ⭐ MVP

**User Story**: Como sistema, quero gravar cada inscrição enviada no banco de dados, para que os dados sejam persistidos de forma confiável.

**Why P1**: Sem armazenamento, o sistema não tem propósito.

**Acceptance Criteria**:

1. WHEN uma inscrição for enviada via formulário THEN o Supabase SHALL inserir uma nova row na tabela `inscricoes` com todos os campos preenchidos
2. WHEN a inscrição for gravada THEN o campo `id` SHALL ser gerado automaticamente como UUID
3. WHEN a inscrição for gravada THEN o campo `created_at` SHALL ser preenchido automaticamente com o timestamp do momento da inserção
4. WHEN o campo `batizado_espirito` receber "Prefiro não responder" THEN o sistema SHALL armazenar o valor como texto

**Independent Test**: Enviar inscrição pelo formulário e consultar diretamente no painel do Supabase se a row foi criada.

---

### P1: Consulta de Inscrições ⭐ MVP

**User Story**: Como administrador (via painel), quero consultar todas as inscrições armazenadas, para visualizar os dados dos interessados.

**Why P1**: O painel admin depende desta funcionalidade.

**Acceptance Criteria**:

1. WHEN o painel admin solicitar as inscrições THEN o Supabase SHALL retornar todas as rows da tabela `inscricoes`
2. WHEN a consulta for realizada THEN os resultados SHALL ser ordenáveis por `created_at`
3. WHEN uma inscrição específica for solicitada pelo `id` THEN o Supabase SHALL retornar todos os campos daquela row

**Independent Test**: Consultar via Supabase dashboard ou REST API e verificar que os dados retornados estão corretos.

---

### P1: Segurança Básica (RLS) ⭐ MVP

**User Story**: Como administrador, quero que os dados das inscrições não sejam acessíveis publicamente, para proteger a privacidade dos inscritos.

**Why P1**: Sem RLS, qualquer pessoa pode consultar todas as inscrições via API pública do Supabase.

**Acceptance Criteria**:

1. WHEN RLS estiver habilitado na tabela THEN visitantes anônimos SHALL conseguir apenas INSERT (enviar inscrição)
2. WHEN um visitante anônimo tentar SELECT na tabela THEN o Supabase SHALL negar a operação
3. WHEN o sistema precisar consultar inscrições THEN SHALL usar a service_role key (apenas no admin, nunca exposta publicamente)

**Independent Test**: Tentar consultar a tabela via API pública com a anon key e verificar que retorna vazio/erro.

---

## Edge Cases

- WHEN o Supabase estiver fora do ar THEN o sistema SHALL exibir mensagem de erro sem crashar
- WHEN campos opcionais (tempo_comunhao) forem enviados vazios THEN o Supabase SHALL aceitar null
- WHEN dois envios idênticos ocorrerem simultaneamente THEN o Supabase SHALL criar duas rows distintas (UUIDs diferentes)

---

## Requirement Traceability

| Requirement ID | Story                    | Phase  | Status  |
| -------------- | ------------------------ | ------ | ------- |
| DB-01          | P1: Armazenamento        | Specify | Pending |
| DB-02          | P1: Consulta             | Specify | Pending |
| DB-03          | P1: Segurança RLS        | Specify | Pending |

**Coverage:** 3 total, 0 mapped to tasks, 3 unmapped ⚠️

---

## Success Criteria

- [ ] Toda inscrição enviada pelo formulário é persistida corretamente no banco
- [ ] Visitantes anônimos não conseguem consultar dados via API pública
- [ ] O admin consegue listar e visualizar todas as inscrições
