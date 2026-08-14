# Guia de Configuração do Supabase

Este documento contém o passo a passo para configurar o banco de dados do Supabase para o Sistema de Inscrição.

## 1. Criar Projeto no Supabase
1. Acesse [supabase.com](https://supabase.com) e faça login.
2. No painel inicial, clique em **"New Project"**.
3. Selecione sua organização (ou crie uma nova).
4. Defina um **Name** (ex: `sistema-inscricao`).
5. Crie uma **Database Password** forte e guarde-a em um lugar seguro.
6. Escolha a **Region** mais próxima do seu público.
7. Clique em **"Create new project"** e aguarde alguns minutos enquanto o banco de dados é provisionado.

## 2. Configurar o Banco de Dados (Tabela e RLS)
1. No menu lateral esquerdo do Supabase, vá em **"SQL Editor"**.
2. Clique em **"New query"**.
3. Abra o arquivo [`schema.sql`](./schema.sql) deste projeto, copie todo o conteúdo e cole no SQL Editor.
4. Clique em **"Run"** (ou pressione Cmd/Ctrl + Enter). Isso criará a tabela `inscricoes`.
5. Apague o texto do editor, abra o arquivo [`rls.sql`](./rls.sql), copie e cole no SQL Editor.
6. Clique em **"Run"**. Isso configurará as políticas de segurança (permitindo envio pelo formulário e bloqueando leitura pública).

## 3. Obter as Chaves de API
1. No menu lateral esquerdo, vá em **"Project Settings"** (ícone de engrenagem no final).
2. Selecione **"API"**.
3. Na seção **Project URL**, copie a URL gerada.
4. Na seção **Project API keys**, copie as duas chaves:
   - **`anon`** `public`: Será usada no formulário de inscrição público.
   - **`service_role`** `secret`: Será usada no painel administrativo para visualizar as inscrições. 
   *(Nota: Nunca exponha a service_role key no lado público do cliente!)*

## 4. Configurar no Código do Projeto
Quando formos implementar o front-end, você precisará colar essas chaves nos arquivos JavaScript:

- Em `js/supabase.js` (ou onde as variáveis de ambiente forem configuradas), você definirá a **Project URL** e a **`anon` key**.
- Em `js/admin.js`, você também usará a **`service_role` key** para buscar a listagem de inscrições no painel administrativo de forma segura, contornando as restrições do RLS.
