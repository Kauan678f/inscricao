# Painel Administrativo — Specification

## Problem Statement

Os administradores do projeto precisam visualizar as inscrições recebidas sem acessar diretamente o banco de dados. É necessária uma interface web simples com login (mockado na V1) que permita listar inscritos, ver totais e abrir cada inscrição para visualizar todas as respostas.

## Goals

- [ ] Implementar login mockado funcional (admin/123456) como porta de entrada
- [ ] Exibir total de inscritos no painel
- [ ] Listar inscritos com data e respostas principais
- [ ] Permitir visualização completa de uma inscrição individual
- [ ] Ordenar inscrições por data
- [ ] Implementar logout
- [ ] Estruturar código para substituição futura do login mockado por autenticação real

## Out of Scope

| Feature                            | Reason                                          |
| ---------------------------------- | ----------------------------------------------- |
| Autenticação real (Supabase Auth)  | Planejada para V2                               |
| Edição de inscrições               | V2                                              |
| Exclusão de inscrições             | V2                                              |
| Exportação Excel/CSV               | V2                                              |
| Filtros avançados                  | V2                                              |
| Dashboard com gráficos             | V2                                              |
| Múltiplos administradores          | V2                                              |
| Sistema de permissões              | V2                                              |
| Envio de mensagens                 | V2                                              |

---

## User Stories

### P1: Login Mockado ⭐ MVP

**User Story**: Como administrador, quero fazer login com credenciais simples para acessar o painel, para que visitantes comuns não vejam as inscrições.

**Why P1**: Sem login, qualquer pessoa acessaria os dados.

**Acceptance Criteria**:

1. WHEN o admin acessar admin.html THEN o sistema SHALL exibir um formulário de login (usuário + senha)
2. WHEN o admin inserir "admin" e "123456" THEN o sistema SHALL autenticar e exibir o painel administrativo
3. WHEN o admin inserir credenciais incorretas THEN o sistema SHALL exibir mensagem de erro e manter na tela de login
4. WHEN o admin recarregar a página após login THEN o sistema SHALL manter a sessão ativa (via sessionStorage ou similar)
5. WHEN o login for implementado THEN a estrutura do código SHALL permitir substituição futura por autenticação real sem reescrita significativa

**Independent Test**: Acessar admin.html, tentar credenciais erradas (ver erro), inserir credenciais corretas (ver painel).

---

### P1: Listagem de Inscritos ⭐ MVP

**User Story**: Como administrador logado, quero ver uma lista de todos os inscritos com suas informações principais, para ter uma visão geral rápida.

**Why P1**: Funcionalidade central do painel.

**Acceptance Criteria**:

1. WHEN o admin acessar o painel THEN o sistema SHALL exibir o total de inscritos
2. WHEN o painel carregar THEN o sistema SHALL exibir uma tabela/lista com: data da inscrição, se é cristão, batizado nas águas, batizado no espírito santo, em comunhão
3. WHEN houver inscrições THEN a listagem SHALL ser ordenada por data (mais recente primeiro)
4. WHEN não houver inscrições THEN o sistema SHALL exibir mensagem indicando que não há inscritos
5. WHEN a consulta ao Supabase falhar THEN o sistema SHALL exibir mensagem de erro

**Independent Test**: Logar no admin e verificar que a listagem corresponde aos dados no Supabase.

---

### P1: Visualização de Inscrição Individual ⭐ MVP

**User Story**: Como administrador, quero clicar em um inscrito e ver todas as suas respostas, para analisar a inscrição completa.

**Why P1**: Sem isso, o admin vê apenas resumo e não consegue analisar a motivação do candidato.

**Acceptance Criteria**:

1. WHEN o admin clicar em uma inscrição na listagem THEN o sistema SHALL exibir todas as respostas daquela inscrição
2. WHEN a inscrição individual for exibida THEN SHALL mostrar: data, é cristão, há quanto tempo, batizado águas, batizado espírito, em comunhão, há quanto tempo, motivo (texto completo)
3. WHEN o admin estiver visualizando uma inscrição THEN SHALL haver um botão/link para voltar à listagem

**Independent Test**: Clicar em uma inscrição e verificar que todas as 7 respostas estão visíveis e corretas.

---

### P1: Logout ⭐ MVP

**User Story**: Como administrador, quero sair do painel de forma segura, para que outra pessoa não acesse o painel no meu dispositivo.

**Why P1**: Requisito básico de segurança, mesmo com login mockado.

**Acceptance Criteria**:

1. WHEN o admin clicar no botão "Sair" THEN o sistema SHALL limpar a sessão e redirecionar para a tela de login
2. WHEN o admin fizer logout THEN acessar admin.html SHALL exigir novo login

**Independent Test**: Fazer logout, tentar acessar admin.html novamente e verificar que pede login.

---

### P2: Responsividade do Painel

**User Story**: Como administrador, quero acessar o painel pelo celular quando necessário, para verificar inscrições de qualquer lugar.

**Why P2**: O uso principal será em desktop, mas acesso mobile é desejável.

**Acceptance Criteria**:

1. WHEN acessado em mobile THEN o painel SHALL adaptar tabela/listagem para tela pequena (scroll horizontal ou cards)
2. WHEN acessado em desktop THEN o painel SHALL utilizar layout amplo com tabela completa

**Independent Test**: Acessar admin.html em simulação mobile no DevTools.

---

## Edge Cases

- WHEN houver muitas inscrições (> 100) THEN o sistema SHALL manter performance aceitável na listagem
- WHEN o admin tentar acessar o painel sem login THEN o sistema SHALL redirecionar para a tela de login
- WHEN a sessão expirar (tab fechada) THEN o sistema SHALL exigir novo login
- WHEN a inscrição tiver campo `tempo_comunhao` nulo (respondeu "Não" em comunhão) THEN o sistema SHALL exibir "N/A" ou equivalente

---

## Requirement Traceability

| Requirement ID | Story                         | Phase  | Status  |
| -------------- | ----------------------------- | ------ | ------- |
| ADM-01         | P1: Login Mockado             | Specify | Pending |
| ADM-02         | P1: Listagem de Inscritos     | Specify | Pending |
| ADM-03         | P1: Visualização Individual   | Specify | Pending |
| ADM-04         | P1: Logout                    | Specify | Pending |
| ADM-05         | P2: Responsividade do Painel  | Specify | Pending |

**Coverage:** 5 total, 0 mapped to tasks, 5 unmapped ⚠️

---

## Success Criteria

- [ ] Admin consegue logar, ver lista, abrir inscrição e fazer logout em < 2 minutos
- [ ] Todas as respostas de uma inscrição são exibidas corretamente na visualização individual
- [ ] Credenciais incorretas não permitem acesso ao painel
- [ ] Código estruturado para fácil substituição do login mockado por autenticação real
