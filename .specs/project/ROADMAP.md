# Roadmap

**Current Milestone:** V1 — MVP Funcional
**Status:** Planning

---

## V1 — MVP Funcional

**Goal:** Sistema completo de inscrição com página pública, formulário, armazenamento no Supabase e painel administrativo simples. Publicado no GitHub Pages.
**Target:** Todos os critérios de aceitação do PRD atendidos

### Features

**Página Pública de Inscrição** — PLANNED

- Cabeçalho com nome do projeto e chamada
- Seção de apresentação do projeto (o que é, objetivo, quem pode participar, como funciona)
- Seção de ressalvas visualmente destacada
- Formulário com 7 perguntas (com campo condicional)
- Checkbox de confirmação obrigatória
- Validação de campos no JavaScript
- Envio para Supabase com feedback (sucesso/erro)
- Layout responsivo mobile-first

**Banco de Dados Supabase** — PLANNED

- Tabela `inscricoes` com 9 campos (id, created_at, cristao, tempo_cristao, batizado_aguas, batizado_espirito, em_comunhao, tempo_comunhao, motivo)
- Configuração de RLS (Row Level Security) para proteger dados

**Painel Administrativo** — PLANNED

- Login mockado (admin/123456)
- Total de inscritos
- Listagem de inscritos com data e respostas principais
- Ordenação por data
- Visualização completa de uma inscrição individual
- Logout

---

## V2 — Melhorias e Segurança (Futuro)

**Goal:** Adicionar autenticação real e campos adicionais

### Features

**Autenticação Real** — PLANNED

- Substituir login mockado por Supabase Auth
- Sessões seguras

**Campos Adicionais no Formulário** — PLANNED

- Nome, e-mail, telefone, cidade, idade

**Funcionalidades Administrativas Avançadas** — PLANNED

- Edição/exclusão de inscrições
- Exportação para Excel
- Filtros avançados

---

## Future Considerations

- Envio de e-mails/mensagens aos inscritos
- Múltiplos administradores com sistema de permissões
- Dashboard com gráficos e estatísticas
- Integração com ferramentas externas
