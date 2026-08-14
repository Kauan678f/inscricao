# Página Pública de Inscrição — Specification

## Problem Statement

Pessoas interessadas em participar de um projeto cristão não possuem um canal claro e transparente para se inscrever. É necessário que conheçam a proposta, leiam as condições e ressalvas, e preencham um formulário estruturado — tudo em uma única página acessível e responsiva.

## Goals

- [ ] Apresentar claramente o projeto antes do formulário, evitando inscrições equivocadas
- [ ] Exibir ressalvas de forma destacada e incontornável
- [ ] Coletar 7 respostas estruturadas via formulário
- [ ] Enviar dados ao Supabase com feedback visual claro ao usuário
- [ ] Funcionar perfeitamente em celular, tablet e desktop (mobile-first)

## Out of Scope

| Feature                            | Reason                                          |
| ---------------------------------- | ----------------------------------------------- |
| Campos de nome, e-mail, telefone   | Planejados para V2                              |
| Upload de arquivos                 | Fora do escopo do projeto                       |
| Multi-idioma                       | Apenas português na V1                          |
| Edição de inscrição após envio     | V2                                              |
| Envio de e-mail de confirmação     | Requer backend/integração adicional             |

---

## User Stories

### P1: Apresentação do Projeto ⭐ MVP

**User Story**: Como visitante, quero ler sobre o projeto antes de me inscrever, para entender claramente a proposta e decidir se quero participar.

**Why P1**: Sem a apresentação, o usuário pode se inscrever sem compreender o projeto.

**Acceptance Criteria**:

1. WHEN o usuário acessar index.html THEN o sistema SHALL exibir um cabeçalho com o nome do projeto e uma breve chamada
2. WHEN o usuário rolar a página THEN o sistema SHALL exibir uma seção de apresentação com: o que é o projeto, objetivo, quem pode participar e como funciona
3. WHEN o usuário visualizar a página em dispositivo móvel THEN o layout SHALL se adaptar corretamente sem perda de conteúdo

**Independent Test**: Abrir index.html no navegador e verificar que todas as seções informativas estão visíveis antes do formulário.

---

### P1: Ressalvas Obrigatórias ⭐ MVP

**User Story**: Como visitante, quero ler as condições e ressalvas do projeto antes de preencher o formulário, para não me inscrever com expectativas erradas.

**Why P1**: Evitar inscrições de pessoas que não compreenderam a proposta.

**Acceptance Criteria**:

1. WHEN o usuário rolar até a seção de ressalvas THEN o sistema SHALL exibir uma seção visualmente destacada com título "⚠️ Antes de se inscrever, leia atentamente"
2. WHEN o usuário visualizar as ressalvas THEN o sistema SHALL apresentar todas as condições listadas (inscrição ≠ aprovação automática, compreensão da proposta, critérios da organização, natureza do projeto)
3. WHEN o usuário tentar acessar o formulário THEN as ressalvas SHALL estar posicionadas de forma que sejam inevitavelmente visíveis antes do formulário

**Independent Test**: Verificar que é impossível chegar ao formulário sem passar pelas ressalvas na rolagem natural da página.

---

### P1: Formulário de Inscrição ⭐ MVP

**User Story**: Como visitante que leu e compreendeu a proposta, quero preencher um formulário com minhas informações espirituais e motivação, para demonstrar meu interesse em participar.

**Why P1**: É a funcionalidade central do sistema.

**Acceptance Criteria**:

1. WHEN o formulário for renderizado THEN o sistema SHALL exibir 7 perguntas na ordem definida (cristão, tempo cristão, batizado águas, batizado espírito, comunhão, tempo comunhão, motivo)
2. WHEN o usuário responder "Sim" na pergunta "Está em comunhão com uma igreja?" THEN o sistema SHALL exibir o campo "Há quanto tempo está em comunhão?"
3. WHEN o usuário responder "Não" na pergunta de comunhão THEN o sistema SHALL ocultar o campo de tempo de comunhão
4. WHEN o usuário não marcar a checkbox de confirmação THEN o botão "Enviar inscrição" SHALL permanecer desabilitado
5. WHEN o usuário marcar a checkbox de confirmação THEN o botão "Enviar inscrição" SHALL ser habilitado
6. WHEN o usuário clicar em "Enviar inscrição" com campos obrigatórios vazios THEN o sistema SHALL exibir validação indicando os campos faltantes
7. WHEN o formulário for visualizado em mobile THEN todos os campos SHALL ser exibidos em layout adequado para toque

**Independent Test**: Preencher o formulário completo em celular e desktop, verificando campo condicional e validação.

---

### P1: Envio e Feedback ⭐ MVP

**User Story**: Como visitante, quero receber confirmação clara de que minha inscrição foi enviada (ou que houve um erro), para saber se preciso tentar novamente.

**Why P1**: Sem feedback, o usuário não sabe se a inscrição foi registrada.

**Acceptance Criteria**:

1. WHEN o usuário clicar em "Enviar inscrição" com todos os campos válidos THEN o sistema SHALL enviar os dados ao Supabase
2. WHEN o Supabase confirmar o recebimento THEN o sistema SHALL exibir a mensagem de sucesso: "Inscrição enviada com sucesso! Recebemos suas informações..."
3. WHEN ocorrer erro no envio THEN o sistema SHALL exibir a mensagem de erro: "Não foi possível enviar sua inscrição. Verifique sua conexão e tente novamente."
4. WHEN a inscrição for enviada com sucesso THEN o formulário SHALL ser ocultado ou desabilitado para evitar envio duplicado

**Independent Test**: Enviar formulário válido e verificar mensagem de sucesso; desconectar internet e verificar mensagem de erro.

---

### P2: Responsividade Completa

**User Story**: Como visitante usando celular, quero que o site funcione perfeitamente no meu dispositivo, para poder me inscrever de qualquer lugar.

**Why P2**: Alta prioridade mas a funcionalidade core funciona sem otimização perfeita de responsividade.

**Acceptance Criteria**:

1. WHEN acessado em tela < 480px THEN o layout SHALL ser single-column com tamanhos de toque adequados (≥ 44px)
2. WHEN acessado em tablet (481px-1024px) THEN o layout SHALL adaptar os espaçamentos mantendo legibilidade
3. WHEN acessado em desktop (> 1024px) THEN o layout SHALL utilizar largura máxima centralizada

**Independent Test**: Testar em Chrome DevTools com simulação de iPhone SE, iPad e desktop.

---

## Edge Cases

- WHEN o campo "tempo_cristao" receber texto muito longo (> 500 chars) THEN o sistema SHALL truncar ou limitar a entrada
- WHEN o campo "motivo" receber texto vazio THEN o sistema SHALL bloquear o envio e indicar o campo obrigatório
- WHEN o usuário tentar reenviar o formulário THEN o sistema SHALL prevenir envio duplicado
- WHEN a conexão com Supabase falhar THEN o sistema SHALL exibir mensagem de erro sem perder os dados preenchidos
- WHEN o JavaScript estiver desabilitado THEN o sistema SHALL exibir uma mensagem informando que JavaScript é necessário

---

## Requirement Traceability

| Requirement ID | Story                    | Phase  | Status  |
| -------------- | ------------------------ | ------ | ------- |
| PUB-01         | P1: Apresentação         | Specify | Pending |
| PUB-02         | P1: Ressalvas            | Specify | Pending |
| PUB-03         | P1: Formulário           | Specify | Pending |
| PUB-04         | P1: Envio e Feedback     | Specify | Pending |
| PUB-05         | P2: Responsividade       | Specify | Pending |

**Coverage:** 5 total, 0 mapped to tasks, 5 unmapped ⚠️

---

## Success Criteria

- [ ] Usuário completa fluxo inteiro (ler → preencher → enviar) em < 5 minutos
- [ ] Formulário funciona corretamente em Chrome, Firefox e Safari mobile
- [ ] Zero dados perdidos — toda inscrição enviada é gravada no Supabase
- [ ] Ressalvas são impossíveis de ignorar no fluxo natural da página
