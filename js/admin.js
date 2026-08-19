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
            if (username === 'admin' && password === '123456') {
                sessionStorage.setItem('admin_logged_in', 'true');
                return true;
            }
            return false;
        },
        
        logout() {
            sessionStorage.removeItem('admin_logged_in');
            renderizarTela();
        }
    };

    // --- Controle de UI ---
    function renderizarTela() {
        if (Auth.isAuthenticated()) {
            loginSection.classList.add('hidden');
            dashboardSection.classList.remove('hidden');
            carregarInscritos();
        } else {
            dashboardSection.classList.add('hidden');
            loginSection.classList.remove('hidden');
            if (formLogin) formLogin.reset();
        }
    }

    // --- Event Listeners ---
    if (formLogin) {
        formLogin.addEventListener('submit', (e) => {
            e.preventDefault();
            const usernameInput = document.getElementById('username').value.trim();
            const passwordInput = document.getElementById('password').value.trim();
            
            loginError.classList.add('hidden');
            
            if (Auth.login(usernameInput, passwordInput)) {
                renderizarTela();
            } else {
                loginError.classList.remove('hidden');
            }
        });
    }

    // -------------------------------------------------------------
    // Lógica de Carregamento de Inscritos
    // -------------------------------------------------------------
    window.carregarInscritos = async function() {
        const container = document.getElementById('lista-inscritos');
        const spanTotal = document.getElementById('total-inscritos');
        const spanMissoes = document.getElementById('total-missoes');
        
        if (!container || !spanTotal) return;

        container.innerHTML = `<div class="text-center" style="padding: 3rem; color: var(--color-text-muted);">🔄 Carregando dados do Supabase...</div>`;

        try {
            const adminClient = getSupabaseAdmin();
            if (!adminClient) throw new Error("Cliente Supabase não configurado.");

            const { data, error } = await adminClient
                .from('inscricoes')
                .select('*')
                .order('created_at', { ascending: false });

            if (error) throw error;

            spanTotal.innerText = data.length;
            
            // Calcula total disponíveis para missões
            const disponiveis = data.filter(i => i.disponivel_missoes === 'Sim').length;
            if(spanMissoes) spanMissoes.innerText = disponiveis;

            if (data.length === 0) {
                container.innerHTML = `<div class="text-center" style="padding: 3rem; color: var(--color-text-muted);">Nenhuma inscrição encontrada até o momento.</div>`;
                return;
            }

            const formatDate = (isoString) => {
                return new Date(isoString).toLocaleDateString('pt-BR');
            };

            const getBadgeHtml = (text, type) => {
                const colorClass = type === 'success' ? 'badge-green' : 'badge-gray';
                return `<span class="badge ${colorClass}">${text}</span>`;
            };

            // Montar Tabela Modernizada
            let tableHTML = `
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Nome</th>
                            <th>Batismo (Águas)</th>
                            <th>Disp. Missões</th>
                            <th>Dons</th>
                            <th>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            data.forEach(item => {
                const itemJSON = encodeURIComponent(JSON.stringify(item));
                
                const missaoBadge = item.disponivel_missoes === 'Sim' ? getBadgeHtml('Sim', 'success') : getBadgeHtml('Não', 'neutral');
                
                // Tratar a data de batismo se existir
                let dtBatismoStr = '-';
                if(item.data_batismo_aguas) {
                    const partes = item.data_batismo_aguas.split('-');
                    if(partes.length === 3) {
                        dtBatismoStr = `${partes[2]}/${partes[1]}/${partes[0]}`; // YYYY-MM-DD to DD/MM/YYYY
                    } else {
                        dtBatismoStr = item.data_batismo_aguas;
                    }
                }

                tableHTML += `
                    <tr onclick="verDetalhes('${itemJSON}')">
                        <td style="color: var(--color-text-muted);">${formatDate(item.created_at)}</td>
                        <td style="font-weight: 600; color: var(--color-text);">${item.nome || '-'}</td>
                        <td>${dtBatismoStr}</td>
                        <td>${missaoBadge}</td>
                        <td>${item.cre_dons || '-'}</td>
                        <td><button class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;">Ver Ficha</button></td>
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
            container.innerHTML = `<div class="text-center" style="padding: 3rem; color: var(--color-error);">❌ Erro ao carregar os dados. Verifique a aba Console (F12).</div>`;
        }
    }

    // -------------------------------------------------------------
    // Modal de Detalhes
    // -------------------------------------------------------------
    window.verDetalhes = function(inscricaoJSON) {
        const inscricao = JSON.parse(decodeURIComponent(inscricaoJSON));
        const modal = document.getElementById('modal-detalhes');
        const modalBody = document.getElementById('modal-body-content');
        const modalNome = document.getElementById('modal-nome');
        
        if (!modal || !modalBody) return;
        
        modalNome.innerText = inscricao.nome || 'Ficha de Inscrição';
        
        const formatDateObj = (isoString) => new Date(isoString).toLocaleString('pt-BR');
        
        let dtBatismoStr = '-';
        if(inscricao.data_batismo_aguas) {
            const p = inscricao.data_batismo_aguas.split('-');
            if(p.length === 3) dtBatismoStr = `${p[2]}/${p[1]}/${p[0]}`;
            else dtBatismoStr = inscricao.data_batismo_aguas;
        }

        const html = `
            <div class="detail-grid">
                <div class="detail-block">
                    <span class="detail-label">Enviado em</span>
                    <span class="detail-value">${formatDateObj(inscricao.created_at)}</span>
                </div>
                
                <div class="detail-block">
                    <span class="detail-label">Batismo nas Águas</span>
                    <span class="detail-value">${dtBatismoStr}</span>
                </div>
                
                <div class="detail-block">
                    <span class="detail-label">Batismo no Espírito Santo</span>
                    <span class="detail-value">${inscricao.batismo_espirito || '-'}</span>
                </div>
                
                <div class="detail-block">
                    <span class="detail-label">Crê nos Dons Espirituais?</span>
                    <span class="detail-value">${inscricao.cre_dons || '-'}</span>
                </div>
                
                <div class="detail-block">
                    <span class="detail-label">Crê na volta de Cristo?</span>
                    <span class="detail-value">${inscricao.cre_volta_cristo || '-'}</span>
                </div>
                
                <div class="detail-block">
                    <span class="detail-label">Já participou de missões?</span>
                    <span class="detail-value">${inscricao.ja_participou_missoes || '-'}</span>
                </div>
                
                <div class="detail-block">
                    <span class="detail-label">Já acampou com esse objetivo?</span>
                    <span class="detail-value">${inscricao.ja_acampou || '-'}</span>
                </div>
                
                <div class="detail-block">
                    <span class="detail-label">Disponível para Missões?</span>
                    <span class="detail-value badge ${inscricao.disponivel_missoes === 'Sim' ? 'badge-green' : 'badge-gray'}">${inscricao.disponivel_missoes || '-'}</span>
                </div>
                
                <div class="detail-block detail-full">
                    <span class="detail-label">Motivo para participar</span>
                    <span class="detail-value" style="display: block; margin-top: 0.5rem; line-height: 1.5; font-style: italic;">"${inscricao.motivo || 'Não informado.'}"</span>
                </div>
                
                <div class="detail-block detail-full" style="background: rgba(37,99,235,0.05); border-color: rgba(37,99,235,0.2);">
                    <span class="detail-label" style="color: var(--color-primary);">Termos de Conduta Aceitos:</span>
                    <ul style="margin: 0.5rem 0 0 1.2rem; font-size: 0.85rem; color: var(--color-text-muted);">
                        <li>Ciente de ficar sem rede social: <strong>${inscricao.ciente_rede_social}</strong></li>
                        <li>Resolvido a seguir orientações: <strong>${inscricao.resolvido_orientacoes}</strong></li>
                        <li>Disponível para orar e jejuar: <strong>${inscricao.disponivel_orar_jejuar}</strong></li>
                    </ul>
                </div>
            </div>
        `;
        
        modalBody.innerHTML = html;
        modal.classList.remove('hidden');
    };

    window.fecharDetalhes = function() {
        const modal = document.getElementById('modal-detalhes');
        if (modal) {
            modal.classList.add('hidden');
        }
    };
    
    // Fechar modal clicando fora dele
    document.getElementById('modal-detalhes')?.addEventListener('click', function(e) {
        if(e.target === this) {
            window.fecharDetalhes();
        }
    });

    window.logout = Auth.logout;

    // Inicialização
    renderizarTela();
});
