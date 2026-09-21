# 📋 Instruções — Página de Inscrição

## O que foi feito (21/09/2026)

As inscrições para o **1º Acampe Missionário** foram encerradas. A página de inscrição (`index.html`) foi modificada para:

1. **Esconder o formulário** — O formulário inteiro foi envolvido em uma `<div>` com `display:none`, então ele não aparece mais para o visitante.
2. **Mostrar mensagem de encerramento** — No lugar do formulário, aparece uma mensagem bonita dizendo que as inscrições foram encerradas.
3. **Painel admin intacto** — O `admin.html` não foi alterado. Continua funcionando normalmente no mesmo link de sempre.

> ⚠️ **Nada foi apagado!** O formulário original está todo lá, só está oculto.

---

## 🔄 Como reabrir as inscrições (passo a passo)

Se precisar reabrir as inscrições, siga estes passos no arquivo `index.html`:

### Passo 1 — Esconder a mensagem de encerramento

Procure esta seção (está logo depois de `<main>`):

```html
<!-- ====== INSCRIÇÕES ENCERRADAS (mensagem visível) ====== -->
<section id="inscricoes-encerradas" class="section container">
```

Adicione `style="display:none"` nela para ficar assim:

```html
<section id="inscricoes-encerradas" class="section container" style="display:none">
```

### Passo 2 — Mostrar o formulário novamente

Procure esta linha:

```html
<div id="formulario-wrapper" style="display:none">
```

**Remova** o `style="display:none"` para ficar assim:

```html
<div id="formulario-wrapper">
```

### Passo 3 — Salvar e fazer deploy

1. Salve o arquivo `index.html`
2. No terminal, rode:

```bash
git add index.html
git commit -m "Reabrir inscrições"
git push
```

3. Aguarde uns minutinhos e acesse `https://kauan678f.github.io/inscricao/` para confirmar.

---

## 🔒 Como fechar as inscrições de novo

É o processo inverso:

1. No `index.html`, **remova** o `style="display:none"` da seção `inscricoes-encerradas`
2. **Adicione** `style="display:none"` no `<div id="formulario-wrapper">`
3. Salve, commit e push

---

## 📁 Arquivos importantes

| Arquivo | O que é |
|---|---|
| `index.html` | Página de inscrição (agora mostrando "encerradas") |
| `admin.html` | Painel administrativo (não foi alterado) |
| `js/inscricao.js` | Script do formulário |
| `js/supabase.js` | Configuração do banco de dados |
| `css/style.css` | Estilos da página |
