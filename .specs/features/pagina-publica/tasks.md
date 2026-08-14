# Página Pública — Tasks

**Spec**: `.specs/features/pagina-publica/spec.md`
**Status**: Draft

---

## Execution Plan

### Phase 1: Foundation (Sequential)

Estrutura base de arquivos, CSS e configuração Supabase.

```
T1 → T2 → T3
```

### Phase 2: Seções da Página (Parallel OK)

Cabeçalho, apresentação e ressalvas podem ser construídos em paralelo.

```
     ┌→ T4 ─┐
T3 ──┼→ T5 ─┼──→ T7
     └→ T6 ─┘
```

### Phase 3: Formulário (Sequential)

Construção incremental do formulário.

```
T7 → T8 → T9 → T10
```

### Phase 4: Envio e Feedback (Sequential)

Integração com Supabase e mensagens.

```
T10 → T11 → T12
```

---

## Task Breakdown

### T1: Criar estrutura de arquivos do projeto

**What**: Criar a árvore de diretórios e arquivos vazios conforme PRD (index.html, admin.html, css/, js/, assets/)
**Where**: Raiz do projeto
**Depends on**: None
**Requirement**: PUB-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Arquivo `index.html` criado com boilerplate HTML5 (meta viewport, charset, links para CSS/JS)
- [x] Arquivo `admin.html` criado com boilerplate HTML5
- [x] Diretórios `css/`, `js/`, `assets/` criados
- [x] Arquivos `css/style.css`, `js/supabase.js`, `js/inscricao.js`, `js/admin.js` criados (vazios ou com comentário)

**Verify**: Abrir index.html no navegador — deve renderizar página em branco sem erros no console.

**Commit**: `chore: scaffold project file structure`

---

### T2: Criar design system CSS base

**What**: Definir variáveis CSS (cores, tipografia, espaçamentos), reset, utilitários e estilos globais com abordagem mobile-first
**Where**: `css/style.css`
**Depends on**: T1
**Requirement**: PUB-05

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] CSS custom properties definidas (--color-primary, --color-bg, --color-text, --font-family, --spacing-*, --radius-*)
- [x] Reset CSS aplicado (box-sizing, margin/padding zero, font smoothing)
- [x] Tipografia base configurada (Google Fonts importada, tamanhos responsivos)
- [x] Classes utilitárias para container, seções e espaçamentos
- [x] Media queries base definidas (480px, 768px, 1024px)

**Verify**: Abrir index.html com o CSS linkado — tipografia e cores base visíveis, sem erros no console.

**Commit**: `style: create CSS design system with mobile-first approach`

---

### T3: Configurar cliente Supabase

**What**: Criar módulo JavaScript que inicializa o cliente Supabase com URL e anon key, exportando funções reutilizáveis
**Where**: `js/supabase.js`
**Depends on**: T1
**Requirement**: DB-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Supabase JS Client importado via CDN (script tag no HTML ou import)
- [x] Constantes SUPABASE_URL e SUPABASE_ANON_KEY definidas (placeholder para preencher)
- [x] Cliente inicializado com `supabase.createClient()`
- [x] Funções exportadas: `getSupabaseClient()`, `getSupabaseAdmin()` (para service_role key)
- [x] Comentários indicando onde substituir as keys

**Verify**: Abrir console do navegador — cliente Supabase inicializado sem erros (mesmo com keys placeholder).

**Commit**: `feat: configure Supabase client module`

---

### T4: Construir seção de cabeçalho [P]

**What**: Criar o header da página pública com nome do projeto, espaço para logo e chamada
**Where**: `index.html` + `css/style.css`
**Depends on**: T2
**Requirement**: PUB-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Tag `<header>` com classe específica
- [x] Nome do projeto em `<h1>`
- [x] Elemento `<img>` para logo com fallback (hidden se não houver logo)
- [x] Parágrafo de chamada explicando o objetivo da inscrição
- [x] Estilizado com gradiente ou cor de destaque, responsivo

**Verify**: Abrir index.html — cabeçalho visível com texto legível em mobile (320px) e desktop (1440px).

**Commit**: `feat: build public page header section`

---

### T5: Construir seção de apresentação do projeto [P]

**What**: Criar a seção que explica o projeto (o que é, objetivo, quem pode participar, como funciona)
**Where**: `index.html` + `css/style.css`
**Depends on**: T2
**Requirement**: PUB-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Tag `<section>` com id="sobre" e classe específica
- [x] Subtítulos para cada tópico (O que é, Objetivo, Quem pode participar, Como funciona)
- [x] Texto placeholder claro e direto (marcado como placeholder para substituição)
- [x] Layout em cards ou blocos visuais para cada tópico
- [x] Responsivo em todas as breakpoints

**Verify**: Scroll da página mostra seção de apresentação completa antes das ressalvas.

**Commit**: `feat: build project presentation section`

---

### T6: Construir seção de ressalvas [P]

**What**: Criar a seção visualmente destacada com as ressalvas obrigatórias antes do formulário
**Where**: `index.html` + `css/style.css`
**Depends on**: T2
**Requirement**: PUB-02

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Tag `<section>` com id="ressalvas" e classe de destaque visual
- [x] Título "⚠️ Antes de se inscrever, leia atentamente" em `<h2>`
- [x] Lista de ressalvas com ícones/bullets visuais
- [x] Background diferenciado (cor de alerta suave) com borda ou box-shadow
- [x] Posicionada entre a apresentação e o formulário
- [x] Impossível de ser ignorada no fluxo de scroll

**Verify**: Scroll natural da página — ressalvas aparecem destacadas antes do formulário, impossíveis de pular.

**Commit**: `feat: build mandatory disclaimers section`

---

### T7: Criar estrutura base do formulário

**What**: Criar o elemento `<form>` com container, título e estrutura para receber os campos
**Where**: `index.html` + `css/style.css`
**Depends on**: T4, T5, T6
**Requirement**: PUB-03

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Tag `<section>` com id="inscricao"
- [x] Tag `<form>` com id="form-inscricao" e atributo novalidate
- [x] Estilos para form groups, labels, inputs, radio buttons e textareas
- [x] Layout mobile-first para campos de formulário
- [x] Título da seção "Formulário de Inscrição"

**Verify**: Formulário vazio renderiza com estilos corretos em mobile e desktop.

**Commit**: `feat: create registration form base structure`

---

### T8: Implementar perguntas 1 a 4 do formulário

**What**: Adicionar os campos: É cristão (radio), Tempo cristão (text), Batizado águas (radio), Batizado espírito (radio com 3 opções)
**Where**: `index.html`
**Depends on**: T7
**Requirement**: PUB-03

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [x] Pergunta 1: Radio group "Sim/Não" com name="cristao"
- [x] Pergunta 2: Input text com name="tempo_cristao" e label
- [x] Pergunta 3: Radio group "Sim/Não" com name="batizado_aguas"
- [x] Pergunta 4: Radio group "Sim/Não/Prefiro não responder" com name="batizado_espirito"
- [x] Todos os campos com labels acessíveis (for/id)
- [x] Estilos de radio buttons customizados

**Verify**: Todos os 4 campos visíveis e interativos, radio buttons funcionam corretamente.

**Commit**: `feat: add form questions 1-4 (faith background)`

---

### T9: Implementar perguntas 5 a 7 com campo condicional

**What**: Adicionar os campos: Comunhão (radio), Tempo comunhão (text, condicional), Motivo (textarea). Implementar lógica de exibição condicional do campo 6.
**Where**: `index.html` + `js/inscricao.js`
**Depends on**: T8
**Requirement**: PUB-03

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [ ] Pergunta 5: Radio group "Sim/Não" com name="em_comunhao"
- [ ] Pergunta 6: Input text com name="tempo_comunhao", inicialmente oculto (display:none)
- [ ] Pergunta 7: Textarea com name="motivo", rows suficientes para texto longo
- [ ] JavaScript: event listener no radio de comunhão que mostra/oculta campo 6
- [ ] Quando "Sim" selecionado → campo 6 aparece com animação suave
- [ ] Quando "Não" selecionado → campo 6 desaparece e valor é limpo

**Verify**: Clicar "Sim" em comunhão → campo de tempo aparece. Clicar "Não" → campo desaparece.

**Commit**: `feat: add form questions 5-7 with conditional field logic`

---

### T10: Implementar checkbox de confirmação e botão de envio

**What**: Adicionar checkbox obrigatória e botão "Enviar inscrição" que só habilita quando checkbox está marcada
**Where**: `index.html` + `js/inscricao.js`
**Depends on**: T9
**Requirement**: PUB-03

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [ ] Checkbox com texto "Li e compreendi as informações apresentadas sobre o projeto..."
- [ ] Botão "Enviar inscrição" com atributo disabled por padrão
- [ ] JavaScript: event listener na checkbox que habilita/desabilita o botão
- [ ] Estilo visual claro diferenciando botão habilitado vs desabilitado
- [ ] Botão com estilo de destaque (cor primária, tamanho adequado para toque)

**Verify**: Checkbox desmarcada → botão cinza/desabilitado. Checkbox marcada → botão ativo e clicável.

**Commit**: `feat: add confirmation checkbox and submit button`

---

### T11: Implementar validação de campos obrigatórios

**What**: Criar função JavaScript que valida todos os campos obrigatórios antes do envio
**Where**: `js/inscricao.js`
**Depends on**: T10
**Requirement**: PUB-04

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [ ] Função `validarFormulario()` que verifica cada campo obrigatório
- [ ] Campos obrigatórios: cristao, tempo_cristao, batizado_aguas, batizado_espirito, em_comunhao, motivo
- [ ] Se em_comunhao === "Sim", tempo_comunhao também é obrigatório
- [ ] Campos inválidos recebem classe CSS de erro (borda vermelha) + mensagem
- [ ] Scroll automático para o primeiro campo com erro
- [ ] Retorna true/false

**Verify**: Submeter formulário vazio → todos os campos obrigatórios destacados em vermelho com mensagens.

**Commit**: `feat: add form validation for required fields`

---

### T12: Implementar envio para Supabase e feedback

**What**: Criar função que envia os dados validados ao Supabase e exibe mensagem de sucesso ou erro
**Where**: `js/inscricao.js` + `js/supabase.js`
**Depends on**: T11, T3
**Requirement**: PUB-04, DB-01

**Tools**:
- MCP: NONE
- Skill: NONE

**Done when**:
- [ ] Função `enviarInscricao()` que coleta dados do form e chama Supabase insert
- [ ] Mapeamento correto: cristao→boolean, batizado_aguas→boolean, em_comunhao→boolean, batizado_espirito→text, textos→text
- [ ] Loading state no botão durante envio (spinner ou texto "Enviando...")
- [ ] Sucesso: exibe mensagem "Inscrição enviada com sucesso!" e oculta/desabilita formulário
- [ ] Erro: exibe mensagem "Não foi possível enviar sua inscrição..." sem perder dados preenchidos
- [ ] Prevenção de envio duplicado (desabilitar botão após clique)

**Verify**: Preencher formulário completo → enviar → mensagem de sucesso aparece. Desconectar internet → enviar → mensagem de erro aparece.

**Commit**: `feat: implement Supabase submission with success/error feedback`

---

## Parallel Execution Map

```
Phase 1 (Sequential):
  T1 ──→ T2 ──→ T3

Phase 2 (Parallel):
  T2 complete, then:
    ├── T4 [P] (header)
    ├── T5 [P] (apresentação)
    └── T6 [P] (ressalvas)

Phase 3 (Sequential):
  T4,T5,T6 complete, then:
    T7 ──→ T8 ──→ T9 ──→ T10

Phase 4 (Sequential):
  T10 + T3 complete, then:
    T11 ──→ T12
```

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Scaffold arquivos | Criação de arquivos | ✅ Granular |
| T2: Design system CSS | 1 arquivo CSS | ✅ Granular |
| T3: Cliente Supabase | 1 módulo JS | ✅ Granular |
| T4: Header | 1 seção HTML + CSS | ✅ Granular |
| T5: Apresentação | 1 seção HTML + CSS | ✅ Granular |
| T6: Ressalvas | 1 seção HTML + CSS | ✅ Granular |
| T7: Form base | 1 estrutura form | ✅ Granular |
| T8: Perguntas 1-4 | 4 campos relacionados | ⚠️ OK (coesivos) |
| T9: Perguntas 5-7 + condicional | 3 campos + 1 lógica | ⚠️ OK (coesivos) |
| T10: Checkbox + botão | 2 elementos vinculados | ✅ Granular |
| T11: Validação | 1 função JS | ✅ Granular |
| T12: Envio + feedback | 1 função JS + UI | ✅ Granular |
