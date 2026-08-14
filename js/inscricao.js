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

    // -------------------------------------------------------------
    // Lógica do Checkbox de Aceite e Botão de Envio (T10)
    // -------------------------------------------------------------
    const checkboxAceite = document.getElementById('aceite_termos');
    const btnSubmit = document.getElementById('btn-submit');

    if (checkboxAceite && btnSubmit) {
        checkboxAceite.addEventListener('change', (e) => {
            // Habilita o botão apenas se o checkbox estiver marcado
            btnSubmit.disabled = !e.target.checked;
        });
    }

    // -------------------------------------------------------------
    // Lógica de Validação do Formulário (T11)
    // -------------------------------------------------------------
    function validarFormulario() {
        let isValid = true;
        let primeiroCampoComErro = null;

        // 1. Limpa erros anteriores
        document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        document.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));

        // Função auxiliar para marcar erro num grupo
        const marcarErro = (group, inputElement = null) => {
            isValid = false;
            if (group) group.classList.add('has-error');
            if (inputElement) inputElement.classList.add('is-invalid');
            if (!primeiroCampoComErro) primeiroCampoComErro = group;
        };

        // Função auxiliar para validação de Radio buttons
        const validarRadio = (name, groupId) => {
            const radios = document.querySelectorAll(`input[name="${name}"]`);
            const checked = Array.from(radios).find(r => r.checked);
            if (!checked) {
                marcarErro(document.getElementById(groupId));
                return null;
            }
            return checked.value;
        };

        // Função auxiliar para validação de Textos e Textareas
        const validarTexto = (id, groupId) => {
            const input = document.getElementById(id);
            if (!input || input.value.trim() === '') {
                marcarErro(document.getElementById(groupId), input);
                return null;
            }
            return input.value.trim();
        };

        // 2. Verificações obrigatórias
        validarTexto('nome', 'group-nome');
        validarRadio('cristao', 'group-cristao');
        validarTexto('tempo_cristao', 'group-tempo-cristao');
        validarRadio('batizado_aguas', 'group-batizado-aguas');
        validarRadio('batizado_espirito', 'group-batizado-espirito');
        
        const comunhao = validarRadio('em_comunhao', 'group-comunhao');
        if (comunhao === 'Sim') {
            validarTexto('tempo_comunhao', 'group-tempo-comunhao');
        }

        validarTexto('motivo', 'group-motivo');

        // 3. Scroll para o primeiro erro se houver
        if (!isValid && primeiroCampoComErro) {
            primeiroCampoComErro.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        return isValid;
    }

    // -------------------------------------------------------------
    // Lógica de Envio para o Supabase (T12)
    // -------------------------------------------------------------
    async function enviarInscricao() {
        const btnSubmit = document.getElementById('btn-submit');
        const originalBtnText = btnSubmit.innerText;
        const feedbackSuccess = document.getElementById('feedback-success');
        const feedbackError = document.getElementById('feedback-error');
        const errorText = document.getElementById('error-message-text');

        // Função auxiliar para converter "Sim"/"Não" em booleano
        const toBool = (val) => val === 'Sim';

        // Reset feedbacks
        feedbackSuccess.classList.add('hidden');
        feedbackError.classList.add('hidden');

        // Loading state (desabilita botão e muda texto)
        btnSubmit.disabled = true;
        btnSubmit.innerText = 'Enviando aguarde...';

        try {
            // Inicializa cliente
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) throw new Error("Cliente Supabase não configurado. Verifique js/supabase.js.");

            // Coleta os valores do formulário
            const isComunhao = toBool(document.querySelector('input[name="em_comunhao"]:checked').value);
            const tempoComunhaoEl = document.getElementById('tempo_comunhao');

            const payload = {
                nome: document.getElementById('nome').value.trim(),
                cristao: toBool(document.querySelector('input[name="cristao"]:checked').value),
                tempo_cristao: document.getElementById('tempo_cristao').value.trim(),
                batizado_aguas: toBool(document.querySelector('input[name="batizado_aguas"]:checked').value),
                batizado_espirito: document.querySelector('input[name="batizado_espirito"]:checked').value,
                em_comunhao: isComunhao,
                tempo_comunhao: isComunhao && tempoComunhaoEl ? tempoComunhaoEl.value.trim() : null,
                motivo: document.getElementById('motivo').value.trim()
            };

            // Envia pro Supabase
            const { data, error } = await supabaseClient
                .from('inscricoes')
                .insert([payload]);

            if (error) {
                console.error("Erro Supabase:", error);
                throw new Error("Erro de comunicação com o banco de dados.");
            }

            // Sucesso: Oculta o formulário e mostra a mensagem de sucesso
            form.style.display = 'none';
            feedbackSuccess.classList.remove('hidden');
            
            // Rola a tela suavemente para a mensagem de sucesso
            feedbackSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });

        } catch (err) {
            console.error("Erro na submissão:", err);
            errorText.innerText = err.message || "Não foi possível enviar sua inscrição no momento. Por favor, tente novamente.";
            feedbackError.classList.remove('hidden');
            
            // Restaura o botão para tentar novamente
            btnSubmit.disabled = false;
            btnSubmit.innerText = originalBtnText;
        }
    }

    // Interceptar o submit do form
    const form = document.getElementById('form-inscricao');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Impede recarregamento da página
            
            if (validarFormulario()) {
                enviarInscricao();
            }
        });
    }
});
