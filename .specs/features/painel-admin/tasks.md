# Painel Administrativo — Tasks

**Spec**: `.specs/features/painel-admin/spec.md`
**Status**: Draft

---

## Execution Plan

### Phase 1: Login (Sequential)

Tela de login e lógica de autenticação mockada.

```
T1 → T2
```

### Phase 2: Painel Core (Sequential)

Estrutura do painel, listagem e detalhes.

```
T2 → T3 → T4 → T5
```

### Phase 3: Finalização (Sequential)

Logout e responsividade.

```
T5 → T6 → T7
```

---

## Task Breakdown

### T1: Construir tela de login

**What**: Criar a interface HTML/CSS do formulário de login (usuário + senha) na página admin.html
**Where**: `admin.html` + `css/style.css`
**Depends on**: Página Pública T2 (design system CSS)
**Requirement**: ADM-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Formulário de login centralizado na tela com campos "Usuário" e "Senha"
- [x] Input de senha com type="password"
- [x] Botão "Entrar"
- [x] Espaço para mensagem de erro (hidden por padrão)
- [x] Estilizado com o design system do projeto (mesmas cores, fontes)
- [x] Layout responsivo (funciona em mobile e desktop)

**Verify**: Abrir admin.html → tela de login renderiza centralizada, campos funcionais.

**Commit**: `feat(admin): build login screen UI`

---

### T2: Implementar lógica de login mockado

**What**: Criar a validação de credenciais (admin/123456), gerenciamento de sessão via sessionStorage, e redirecionamento
**Where**: `js/admin.js`
**Depends on**: T1
**Requirement**: ADM-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Função `handleLogin()` que compara usuário/senha com credenciais mockadas
- [x] Credenciais corretas: salvar flag em sessionStorage e mostrar painel (ocultar login)
- [x] Credenciais incorretas: exibir mensagem "Usuário ou senha incorretos"
- [x] Ao carregar página: verificar sessionStorage — se logado, mostrar painel direto
- [x] Estrutura modular que permita substituição futura por Supabase Auth (função `isAuthenticated()`, `login()`, `logout()` separadas)

**Verify**: Inserir "admin"/"123456" → painel aparece. Inserir "wrong"/"wrong" → erro aparece. Recarregar → sessão mantida.

**Commit**: `feat(admin): implement mock authentication logic`

---

### T3: Construir layout do painel administrativo

**What**: Criar a estrutura HTML/CSS do painel (header com logout, contador de inscritos, área de listagem, área de detalhes)
**Where**: `admin.html` + `css/style.css`
**Depends on**: T2
**Requirement**: ADM-02

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Header do painel com título "Painel Administrativo" e botão "Sair"
- [x] Card/badge mostrando "Total de inscritos: X"
- [x] Container para tabela de listagem (id="lista-inscritos")
- [x] Container para detalhes de inscrição (id="detalhe-inscricao", hidden por padrão)
- [x] Layout com design system do projeto
- [x] Seção de login e seção de painel são mutuamente exclusivas (uma oculta a outra)

**Verify**: Após login, painel aparece com todas as áreas estruturadas (vazias, sem dados ainda).

**Commit**: `feat(admin): build admin panel layout`

---

### T4: Implementar listagem de inscritos

**What**: Criar função que consulta o Supabase e renderiza a tabela de inscritos com data, cristão, batizado águas, espírito santo, comunhão
**Where**: `js/admin.js`
**Depends on**: T3, Supabase T3 (cliente configurado)
**Requirement**: ADM-02, DB-02

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Função `carregarInscritos()` que faz SELECT na tabela inscricoes via service_role key
- [x] Renderização de tabela HTML com colunas: Data, Nome, Cristão, Batizado Águas, Espírito Santo, Comunhão
- [x] Valores boolean exibidos como "Sim"/"Não"
- [x] Data formatada no padrão DD/MM/AAAA
- [x] Ordenação por created_at DESC (mais recente primeiro)
- [x] Total de inscritos atualizado no badge/card
- [x] Estado vazio: mensagem "Nenhuma inscrição encontrada"
- [x] Erro na consulta: mensagem de erro exibida
- [x] Cada row clicável (cursor pointer, evento de clique)

**Verify**: Com inscrições no banco → tabela renderiza corretamente. Banco vazio → mensagem de vazio. Supabase off → mensagem de erro.

**Commit**: `feat(admin): implement subscriber listing with Supabase query`

---

### T5: Implementar visualização de inscrição individual

**What**: Criar função que exibe todas as respostas de uma inscrição selecionada na listagem
**Where**: `js/admin.js` + `admin.html`
**Depends on**: T4
**Requirement**: ADM-03

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Função `verDetalhes(inscricao)` vinculada ao clique da linha da tabela
- [x] Renderizar no container `detalhe-inscricao` todas as respostas
- [x] Botão "Fechar" ou "Voltar" para ocultar os detalhes
- [x] Animação ou scroll suave para a área de detalhes
- [x] Campo tempo_comunhao nulo exibe "N/A" ou "Não se aplica"
- [x] Botão "Voltar à listagem" que oculta detalhes e mostra tabela
- [x] Ao clicar em uma row na listagem → oculta tabela, mostra detalhes
- [x] Transição suave entre listagem e detalhe

**Verify**: Clicar em inscrição na tabela → todas as respostas visíveis. Clicar "Voltar" → volta à tabela.

**Commit**: `feat(admin): implement individual registration detail view`

---

### T6: Implementar logout

**What**: Criar função de logout que limpa sessão e retorna à tela de login
**Where**: `js/admin.js`
**Depends on**: T5
**Requirement**: ADM-04

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Função `handleLogout()` que limpa sessionStorage
- [x] Após logout, seção do painel é ocultada e tela de login é exibida
- [x] Botão "Sair" no header do painel conectado ao handleLogout
- [x] Após logout, recarregar página exige novo login

**Verify**: Clicar "Sair" → tela de login aparece. Recarregar → pede login novamente.

**Commit**: `feat(admin): implement logout functionality`

---

### T7: Responsividade do painel admin

**What**: Ajustar o layout do painel para funcionar em dispositivos móveis (tabela responsiva, cards, etc.)
**Where**: `css/style.css`
**Depends on**: T6
**Requirement**: ADM-05

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Em telas < 768px: tabela de listagem com scroll horizontal ou transformada em cards
- [x] Login centralizado e usável em telas pequenas
- [x] Detalhe da inscrição com layout single-column em mobile
- [x] Botão "Sair" acessível em mobile
- [x] Tamanhos de toque adequados (≥ 44px) em todos os botões

**Verify**: Simular iPhone SE e iPad no DevTools → todas as telas do admin (login, listagem, detalhe) funcionam.

**Commit**: `style(admin): add responsive layout for mobile devices`

---

## Parallel Execution Map

```
Phase 1 (Sequential):
  T1 ──→ T2

Phase 2 (Sequential):
  T2 ──→ T3 ──→ T4 ──→ T5

Phase 3 (Sequential):
  T5 ──→ T6 ──→ T7
```

> **Nota**: As tasks do admin são majoritariamente sequenciais porque cada uma depende da anterior (login → painel → listagem → detalhe → logout → responsividade).

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Tela de login UI | 1 formulário HTML/CSS | ✅ Granular |
| T2: Lógica de login | 1 módulo JS (auth) | ✅ Granular |
| T3: Layout do painel | 1 estrutura HTML/CSS | ✅ Granular |
| T4: Listagem inscritos | 1 função JS + render | ✅ Granular |
| T5: Detalhe inscrição | 1 função JS + render | ✅ Granular |
| T6: Logout | 1 função JS | ✅ Granular |
| T7: Responsividade | CSS media queries | ✅ Granular |
