# Sistema de Inscrição — Projeto Cristão

**Vision:** Permitir que pessoas interessadas conheçam a proposta de um projeto cristão, leiam as ressalvas e se inscrevam através de um formulário online, com dados armazenados no Supabase e visualizados por um painel administrativo simples.

**For:** Pessoas interessadas em participar de um projeto cristão + administradores que precisam visualizar as inscrições.

**Solves:** Centralizar o processo de inscrição de forma clara, transparente e acessível, evitando que pessoas se inscrevam sem compreender a proposta real do projeto.

## Goals

- Entregar uma página pública funcional onde o usuário lê a proposta, as ressalvas e preenche o formulário de inscrição
- Armazenar as inscrições de forma segura no Supabase (PostgreSQL)
- Fornecer um painel administrativo simples para visualização dos inscritos e suas respostas
- Garantir que o site funcione corretamente em dispositivos móveis e desktop (mobile-first)

## Tech Stack

**Core:**

- Linguagem: HTML5 + CSS3 + JavaScript (vanilla)
- Banco de dados: Supabase (PostgreSQL)
- Hospedagem: GitHub Pages

**Key dependencies:**

- Supabase JS Client (CDN)

**Não utilizar:** Node.js, PHP, Vercel, Netlify, frameworks, servidor próprio

## Scope

**v1 includes:**

- Página pública com apresentação do projeto, ressalvas e formulário de inscrição
- 7 perguntas do formulário (cristão, tempo, batismo águas, batismo espírito, comunhão, tempo comunhão, motivo)
- Confirmação obrigatória antes do envio
- Envio dos dados para o Supabase com feedback de sucesso/erro
- Página administrativa com login mockado (admin/123456)
- Painel com total de inscritos, listagem com ordenação por data
- Visualização completa de cada inscrição
- Logout
- Layout responsivo mobile-first

**Explicitly out of scope:**

- Autenticação real (substituirá o mock em versão futura)
- Edição/exclusão de inscrições
- Exportação para Excel
- Envio de mensagens aos inscritos
- Múltiplos administradores / sistema de permissões
- Dashboard complexo / filtros avançados
- Campos adicionais (nome, e-mail, telefone, cidade, idade) — planejados para v2

## Constraints

- **Hospedagem:** Apenas GitHub Pages — sem servidor próprio, sem serverless
- **Tecnologia:** Apenas HTML/CSS/JS vanilla — sem frameworks
- **Segurança V1:** Login mockado não é segurança real; estruturar código para substituição futura
- **Supabase RLS:** Configurar regras de acesso para evitar consulta livre às inscrições
