document.addEventListener('DOMContentLoaded', () => {
    // Referências do DOM
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const formLogin = document.getElementById('form-login');
    const loginError = document.getElementById('login-error');
    
    // Estado Global para Filtros e Impressão
    window.todasInscricoes = [];
    window.inscricoesFiltradas = [];
    
    if (loginError) loginError.classList.add('hidden');
    
    const Auth = {
        isAuthenticated() { return sessionStorage.getItem('admin_logged_in') === 'true'; },
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

    if (formLogin) {
        formLogin.addEventListener('submit', (e) => {
            e.preventDefault();
            const u = document.getElementById('username').value.trim();
            const p = document.getElementById('password').value.trim();
            loginError.classList.add('hidden');
            if (Auth.login(u, p)) renderizarTela();
            else loginError.classList.remove('hidden');
        });
    }

    // -------------------------------------------------------------
    // Buscar Dados do Supabase
    // -------------------------------------------------------------
    window.carregarInscritos = async function() {
        const container = document.getElementById('lista-inscritos');
        const spanTotal = document.getElementById('total-inscritos');
        const spanMissoes = document.getElementById('total-missoes');
        const inputBusca = document.getElementById('input-busca');
        
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

            window.todasInscricoes = data || [];
            if(inputBusca) inputBusca.value = ''; // reseta a busca
            
            atualizarEstatisticas();
            renderizarTabela(window.todasInscricoes);

        } catch (err) {
            console.error("Erro ao buscar inscrições:", err);
            container.innerHTML = `<div class="text-center" style="padding: 3rem; color: var(--color-error);">❌ Erro ao carregar os dados. Verifique a aba Console (F12).</div>`;
        }
    }

    function atualizarEstatisticas() {
        const spanTotal = document.getElementById('total-inscritos');
        const spanMissoes = document.getElementById('total-missoes');
        if(spanTotal) spanTotal.innerText = window.todasInscricoes.length;
        if(spanMissoes) {
            spanMissoes.innerText = window.todasInscricoes.filter(i => i.disponivel_missoes === 'Sim').length;
        }
    }

    // -------------------------------------------------------------
    // Renderizar a Tabela Principal
    // -------------------------------------------------------------
    function renderizarTabela(lista) {
        const container = document.getElementById('lista-inscritos');
        window.inscricoesFiltradas = lista; // Atualiza a lista atual que estamos vendo
        
        if (lista.length === 0) {
            container.innerHTML = `<div class="text-center" style="padding: 3rem; color: var(--color-text-muted);">Nenhuma inscrição encontrada para essa busca.</div>`;
            return;
        }

        const formatDate = (isoString) => new Date(isoString).toLocaleDateString('pt-BR');
        const getBadgeHtml = (text, type) => `<span class="badge ${type === 'success' ? 'badge-green' : 'badge-gray'}">${text}</span>`;

        let tableHTML = `
            <table class="admin-table" id="tabela-dados">
                <thead>
                    <tr>
                        <th style="width: 40px; text-align: center;">
                            <input type="checkbox" id="check-all" onclick="toggleAll(this)">
                        </th>
                        <th>Data</th>
                        <th>Nome</th>
                        <th>É Cristão?</th>
                        <th>Batismo (Águas)</th>
                        <th>Disp. Missões</th>
                        <th>Dons</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>
        `;

        lista.forEach(item => {
            const itemJSON = encodeURIComponent(JSON.stringify(item));
            const missaoBadge = item.disponivel_missoes === 'Sim' ? getBadgeHtml('Sim', 'success') : getBadgeHtml('Não', 'neutral');
            const cristaoBadge = item.e_cristao === 'Sim' ? getBadgeHtml('Sim', 'success') : getBadgeHtml(item.e_cristao || '-', 'neutral');
            
            let dtBatismoStr = '-';
            if(item.data_batismo_aguas) {
                const partes = item.data_batismo_aguas.split('-');
                if(partes.length === 3) dtBatismoStr = `${partes[2]}/${partes[1]}/${partes[0]}`;
                else dtBatismoStr = item.data_batismo_aguas;
            }

            // O onclick na linha abriria o modal. Precisamos garantir que clicar no checkbox NÃO abra o modal.
            tableHTML += `
                <tr class="item-row" data-id="${item.id}">
                    <td style="text-align: center;" onclick="event.stopPropagation();">
                        <input type="checkbox" class="check-item" value="${item.id}">
                    </td>
                    <td style="color: var(--color-text-muted);" onclick="verDetalhes('${itemJSON}')">${formatDate(item.created_at)}</td>
                    <td style="font-weight: 600; color: var(--color-text);" onclick="verDetalhes('${itemJSON}')">${item.nome || '-'}</td>
                    <td onclick="verDetalhes('${itemJSON}')">${cristaoBadge}</td>
                    <td onclick="verDetalhes('${itemJSON}')">${dtBatismoStr}</td>
                    <td onclick="verDetalhes('${itemJSON}')">${missaoBadge}</td>
                    <td onclick="verDetalhes('${itemJSON}')">${item.cre_dons || '-'}</td>
                    <td onclick="verDetalhes('${itemJSON}')"><button class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;">Ver Ficha</button></td>
                </tr>
            `;
        });

        tableHTML += `</tbody></table>`;
        container.innerHTML = tableHTML;
    }

    // -------------------------------------------------------------
    // Funcionalidades da Toolbar
    // -------------------------------------------------------------
    
    // Busca e Filtros Avançados
    window.toggleFiltros = function() {
        const painel = document.getElementById('painel-filtros');
        if(painel) painel.classList.toggle('hidden');
    };

    window.limparFiltros = function() {
        if(document.getElementById('filtro-cristao')) document.getElementById('filtro-cristao').value = '';
        if(document.getElementById('filtro-missoes')) document.getElementById('filtro-missoes').value = '';
        if(document.getElementById('filtro-espirito')) document.getElementById('filtro-espirito').value = '';
        if(document.getElementById('filtro-termos')) document.getElementById('filtro-termos').value = '';
        filtrarTabela();
    };

    window.filtrarTabela = function() {
        const termo = document.getElementById('input-busca').value.toLowerCase();
        const filtroCristao = document.getElementById('filtro-cristao')?.value || '';
        const filtroMissoes = document.getElementById('filtro-missoes')?.value || '';
        const filtroEspirito = document.getElementById('filtro-espirito')?.value || '';
        const filtroTermos = document.getElementById('filtro-termos')?.value || '';
        
        let filtrado = window.todasInscricoes;

        if(termo) {
            filtrado = filtrado.filter(item => (item.nome && item.nome.toLowerCase().includes(termo)));
        }
        if(filtroCristao) {
            filtrado = filtrado.filter(item => item.e_cristao === filtroCristao);
        }
        if(filtroMissoes) {
            filtrado = filtrado.filter(item => item.disponivel_missoes === filtroMissoes);
        }
        if(filtroEspirito) {
            filtrado = filtrado.filter(item => item.batismo_espirito === filtroEspirito);
        }
        if(filtroTermos === 'Sim') {
            // Verifica se a pessoa respondeu Sim para todos os termos de conduta exigidos
            filtrado = filtrado.filter(item => 
                item.ciente_rede_social === 'Sim' && 
                item.resolvido_orientacoes === 'Sim' && 
                item.disponivel_orar_jejuar === 'Sim'
            );
        }
        
        renderizarTabela(filtrado);
    };

    // Seleção de Checkboxes
    window.toggleAll = function(source) {
        const checkboxes = document.querySelectorAll('.check-item');
        checkboxes.forEach(cb => cb.checked = source.checked);
    };

    function getIdsSelecionados() {
        const checkboxes = document.querySelectorAll('.check-item:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    }

    // Apagar Selecionados
    window.apagarSelecionados = async function() {
        const ids = getIdsSelecionados();
        if(ids.length === 0) {
            alert("Selecione pelo menos uma inscrição para apagar.");
            return;
        }

        if(!confirm(`Tem certeza absoluta que deseja apagar ${ids.length} inscrição(ões)? Essa ação não pode ser desfeita.`)) {
            return;
        }

        try {
            const adminClient = getSupabaseAdmin();
            if (!adminClient) throw new Error("Cliente Supabase não configurado.");

            // Supabase permite deletar múltiplos com o .in()
            const { error } = await adminClient
                .from('inscricoes')
                .delete()
                .in('id', ids);

            if(error) throw error;

            alert("Inscrições deletadas com sucesso!");
            carregarInscritos(); // Recarrega do banco
        } catch(err) {
            console.error(err);
            alert("Erro ao deletar inscrições. Verifique o console.");
        }
    };

    // -------------------------------------------------------------
    // Impressão da Lista de Presença
    // -------------------------------------------------------------
    window.imprimirLista = function(apenasSelecionados) {
        let listaImpressao = [];
        
        if (apenasSelecionados) {
            const ids = getIdsSelecionados();
            if(ids.length === 0) {
                alert("Nenhuma inscrição selecionada. Selecione na tabela ou clique em 'Imprimir Todos'.");
                return;
            }
            listaImpressao = window.todasInscricoes.filter(i => ids.includes(i.id));
        } else {
            // Imprime a lista atualmente visível (filtrada ou total)
            listaImpressao = window.inscricoesFiltradas;
        }

        if(listaImpressao.length === 0) {
            alert("Não há dados para imprimir.");
            return;
        }

        const tbody = document.getElementById('print-tbody');
        if(!tbody) return;

        // Ordenar alfabeticamente para a lista de presença
        const listaOrdenada = [...listaImpressao].sort((a, b) => (a.nome || '').localeCompare(b.nome || ''));

        let html = '';
        listaOrdenada.forEach((item, index) => {
            html += `
                <tr>
                    <td style="text-align: center;">${index + 1}</td>
                    <td>${item.nome.toUpperCase()}</td>
                    <td></td> <!-- Coluna vazia para assinatura -->
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
        // Dispara a impressão do navegador (CSS lida com a ocultação dos painéis)
        window.print();
    };


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
                    <span class="detail-label">É Cristão?</span>
                    <span class="detail-value badge ${inscricao.e_cristao === 'Sim' ? 'badge-green' : 'badge-gray'}">${inscricao.e_cristao || '-'}</span>
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
        if (modal) modal.classList.add('hidden');
    };
    
    document.getElementById('modal-detalhes')?.addEventListener('click', function(e) {
        if(e.target === this) window.fecharDetalhes();
    });

    window.logout = Auth.logout;
    renderizarTela();
});
