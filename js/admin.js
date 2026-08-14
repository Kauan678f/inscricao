document.addEventListener('DOMContentLoaded', () => {
    // Referências do DOM
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const formLogin = document.getElementById('form-login');
    const loginError = document.getElementById('login-error');
    
    // Ocultar erro por padrão
    if (loginError) {
        loginError.classList.add('hidden');
    }
    
    // --- Módulo de Autenticação (Mock) ---
    const Auth = {
        isAuthenticated() {
            return sessionStorage.getItem('admin_logged_in') === 'true';
        },
        
        login(username, password) {
            // Hardcoded credentials para mock auth
            if (username === 'admin' && password === '123456') {
                sessionStorage.setItem('admin_logged_in', 'true');
                return true;
            }
            return false;
        },
        
        logout() {
            sessionStorage.removeItem('admin_logged_in');
            renderizarTela(); // Atualiza UI
        }
    };

    // --- Controle de UI ---
    function renderizarTela() {
        if (Auth.isAuthenticated()) {
            loginSection.classList.add('hidden');
            dashboardSection.classList.remove('hidden');
            // Inicializa a tabela de inscritos
            console.log("Painel autenticado. Carregando dados...");
            carregarInscritos();
        } else {
            dashboardSection.classList.add('hidden');
            loginSection.classList.remove('hidden');
            
            // Limpa form se houver
            if (formLogin) formLogin.reset();
        }
    }

    // --- Event Listeners ---
    if (formLogin) {
        formLogin.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const usernameInput = document.getElementById('username').value.trim();
            const passwordInput = document.getElementById('password').value.trim();
            
            // Limpar erros anteriores
            loginError.classList.add('hidden');
            
            // Tenta logar
            if (Auth.login(usernameInput, passwordInput)) {
                // Sucesso
                renderizarTela();
            } else {
                // Erro: Credenciais inválidas
                loginError.classList.remove('hidden');
            }
        });
    }

    // -------------------------------------------------------------
    // Lógica de Carregamento de Inscritos (T4)
    // -------------------------------------------------------------
    async function carregarInscritos() {
        const container = document.getElementById('lista-inscritos');
        const spanTotal = document.getElementById('total-inscritos');
        
        if (!container || !spanTotal) return;

        container.innerHTML = `<div style="padding: var(--spacing-8); text-align: center; color: var(--color-text-muted);">Carregando dados...</div>`;

        try {
            const adminClient = getSupabaseAdmin();
            if (!adminClient) throw new Error("Cliente Admin Supabase não configurado.");

            const { data, error } = await adminClient
                .from('inscricoes')
                .select('*')
                .order('created_at', { ascending: false });

            if (error) throw error;

            spanTotal.innerText = data.length;

            if (data.length === 0) {
                container.innerHTML = `<div style="padding: var(--spacing-8); text-align: center; color: var(--color-text-muted);">Nenhuma inscrição encontrada até o momento.</div>`;
                return;
            }

            // Utilitários de formatação
            const formatDate = (isoString) => {
                const date = new Date(isoString);
                return date.toLocaleDateString('pt-BR');
            };
            const formatBool = (bool) => bool ? 'Sim' : 'Não';

            // Montar Tabela
            let tableHTML = `
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: var(--font-size-sm);">
                    <thead>
                        <tr style="border-bottom: 2px solid var(--color-border); background-color: var(--color-bg);">
                            <th style="padding: var(--spacing-3);">Data</th>
                            <th style="padding: var(--spacing-3);">Nome</th>
                            <th style="padding: var(--spacing-3);">Cristão?</th>
                            <th style="padding: var(--spacing-3);">Águas</th>
                            <th style="padding: var(--spacing-3);">Espírito Santo</th>
                            <th style="padding: var(--spacing-3);">Comunhão</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            data.forEach(item => {
                // Converte o objeto item para string JSON safely to pass to onclick
                const itemJSON = encodeURIComponent(JSON.stringify(item));
                
                tableHTML += `
                    <tr style="border-bottom: 1px solid var(--color-border); cursor: pointer;" class="table-row-hover" onclick="verDetalhes('${itemJSON}')">
                        <td style="padding: var(--spacing-3); color: var(--color-text-muted);">${formatDate(item.created_at)}</td>
                        <td style="padding: var(--spacing-3); font-weight: bold; color: var(--color-text);">${item.nome || '-'}</td>
                        <td style="padding: var(--spacing-3);">${formatBool(item.cristao)}</td>
                        <td style="padding: var(--spacing-3);">${formatBool(item.batizado_aguas)}</td>
                        <td style="padding: var(--spacing-3);">${item.batizado_espirito || '-'}</td>
                        <td style="padding: var(--spacing-3);">${formatBool(item.em_comunhao)}</td>
                    </tr>
                `;
            });

            tableHTML += `
                    </tbody>
                </table>
            `;

            container.innerHTML = tableHTML;

        } catch (err) {
            console.error("Erro ao buscar inscrições:", err);
            container.innerHTML = `<div style="padding: var(--spacing-8); text-align: center; color: var(--color-error);">❌ Erro ao carregar os dados. Verifique o console.</div>`;
        }
    }

    // Expõe logout globalmente para o botão (que será criado na T3/T4)
    window.logout = Auth.logout;

    // Inicialização da página
    renderizarTela();
});
