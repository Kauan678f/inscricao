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
            // T3: A inicialização e carregamento dos dados do painel será feita nas próximas tasks
            console.log("Painel autenticado. Pronto para carregar dados (T3).");
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

    // Expõe logout globalmente para o botão (que será criado na T3/T4)
    window.logout = Auth.logout;

    // Inicialização da página
    renderizarTela();
});
