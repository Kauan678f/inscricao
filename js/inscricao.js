document.addEventListener('DOMContentLoaded', () => {
    // Função de validação
    function validarFormulario() {
        let isValid = true;
        let primeiroCampoComErro = null;

        // Limpa os erros anteriores
        document.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));

        const marcarErro = (groupId) => {
            isValid = false;
            const group = document.getElementById(groupId);
            if (group) group.classList.add('has-error');
            if (!primeiroCampoComErro) primeiroCampoComErro = group;
        };

        const validarTexto = (id, groupId) => {
            const input = document.getElementById(id);
            if (!input || input.value.trim() === '') {
                marcarErro(groupId);
                return null;
            }
            return input.value.trim();
        };

        const validarRadio = (name, groupId) => {
            const radios = document.querySelectorAll(`input[name="${name}"]`);
            const checked = Array.from(radios).find(r => r.checked);
            if (!checked) {
                marcarErro(groupId);
                return null;
            }
            return checked.value;
        };

        // Validação dos campos
        validarTexto('nome', 'group-nome');
        validarRadio('e_cristao', 'group-cristao');
        // validarTexto('data_batismo_aguas', 'group-data-batismo'); // Removido do required porque não-cristãos não têm.
        validarRadio('batismo_espirito', 'group-batizado-espirito');
        validarRadio('cre_dons', 'group-cre-dons');
        validarRadio('cre_volta_cristo', 'group-cre-volta');
        validarRadio('ja_participou_missoes', 'group-ja-missoes');
        validarRadio('ja_acampou', 'group-ja-acampou');
        validarRadio('disponivel_missoes', 'group-disponivel-missoes');
        validarRadio('ciente_rede_social', 'group-ciente-rede');
        validarRadio('resolvido_orientacoes', 'group-resolvido-orientacoes');
        validarRadio('disponivel_orar_jejuar', 'group-disponivel-orar');
        validarTexto('motivo', 'group-motivo');

        if (!isValid && primeiroCampoComErro) {
            primeiroCampoComErro.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        return isValid;
    }

    // Função de Envio
    async function enviarInscricao() {
        const btnSubmit = document.getElementById('btn-submit');
        const originalBtnText = btnSubmit.innerText;
        const feedbackSuccess = document.getElementById('feedback-success');
        const feedbackError = document.getElementById('feedback-error');
        const errorText = document.getElementById('error-message-text');

        feedbackSuccess.classList.add('hidden');
        feedbackError.classList.add('hidden');

        btnSubmit.disabled = true;
        btnSubmit.innerText = 'Enviando aguarde...';

        try {
            const dtBatismoRaw = document.getElementById('data_batismo_aguas').value;
            // Se você quiser integrar com o Supabase depois, o payload é este
            const payload = {
                nome: document.getElementById('nome').value.trim(),
                e_cristao: document.querySelector('input[name="e_cristao"]:checked').value,
                data_batismo_aguas: dtBatismoRaw ? dtBatismoRaw : null,
                batismo_espirito: document.querySelector('input[name="batismo_espirito"]:checked').value,
                cre_dons: document.querySelector('input[name="cre_dons"]:checked').value,
                cre_volta_cristo: document.querySelector('input[name="cre_volta_cristo"]:checked').value,
                ja_participou_missoes: document.querySelector('input[name="ja_participou_missoes"]:checked').value,
                ja_acampou: document.querySelector('input[name="ja_acampou"]:checked').value,
                disponivel_missoes: document.querySelector('input[name="disponivel_missoes"]:checked').value,
                ciente_rede_social: document.querySelector('input[name="ciente_rede_social"]:checked').value,
                resolvido_orientacoes: document.querySelector('input[name="resolvido_orientacoes"]:checked').value,
                disponivel_orar_jejuar: document.querySelector('input[name="disponivel_orar_jejuar"]:checked').value,
                motivo: document.getElementById('motivo').value.trim()
            };

            // Simulação de envio por mockado (o usuário pediu pra deixar mockado dboa por agora ou Supabase)
            // Descomente abaixo se o Supabase estiver configurado
            
            const supabaseClient = window.getSupabaseClient ? window.getSupabaseClient() : null;
            if (supabaseClient) {
                const { error } = await supabaseClient.from('inscricoes').insert([payload]);
                if (error) throw new Error("Erro de comunicação com o banco de dados.");
            } else {
                // Mock delay
                await new Promise(resolve => setTimeout(resolve, 1500));
                console.log("Mock Payload:", payload);
            }
            

            form.style.display = 'none';
            feedbackSuccess.classList.remove('hidden');
            feedbackSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });

        } catch (err) {
            console.error("Erro na submissão:", err);
            errorText.innerText = err.message || "Não foi possível enviar sua inscrição no momento. Por favor, tente novamente.";
            feedbackError.classList.remove('hidden');
            
            btnSubmit.disabled = false;
            btnSubmit.innerText = originalBtnText;
        }
    }

    const form = document.getElementById('form-inscricao');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (validarFormulario()) {
                enviarInscricao();
            }
        });
    }
});
