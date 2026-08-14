document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // Lógica Condicional do Formulário (Pergunta 5 -> Pergunta 6)
    // -------------------------------------------------------------
    const comunhaoRadios = document.querySelectorAll('input[name="em_comunhao"]');
    const groupTempoComunhao = document.getElementById('group-tempo-comunhao');
    const inputTempoComunhao = document.getElementById('tempo_comunhao');

    if (comunhaoRadios.length > 0 && groupTempoComunhao && inputTempoComunhao) {
        comunhaoRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                if (e.target.value === 'Sim') {
                    // Mostrar campo 6 com animação via class
                    groupTempoComunhao.classList.remove('hidden');
                    // Torna o campo obrigatório
                    inputTempoComunhao.setAttribute('required', 'true');
                } else {
                    // Ocultar campo 6
                    groupTempoComunhao.classList.add('hidden');
                    // Remove obrigatoriedade
                    inputTempoComunhao.removeAttribute('required');
                    // Limpa o valor para não enviar dados residuais caso o usuário mude de ideia
                    inputTempoComunhao.value = '';
                    
                    // Limpa também a classe de erro caso existisse
                    inputTempoComunhao.classList.remove('is-invalid');
                    groupTempoComunhao.classList.remove('has-error');
                }
            });
        });
    }

    // A validação final e envio (T10-T12) será implementada depois
});
