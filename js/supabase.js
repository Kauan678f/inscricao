// Arquivo de configuração do cliente Supabase

const SUPABASE_URL = 'https://mzyvdcuuqjrxgjbhwczf.supabase.co'; // Lembre-se de colocar sua URL!
const SUPABASE_ANON_KEY = 'sb_publishable_WJLyKpWN9g7N5-UT2NDjww__E3GI1QC';

/**
 * Retorna a instância do cliente Supabase para uso público (formulário de inscrição).
 */
function getSupabaseClient() {
    if (typeof supabase === 'undefined') {
        console.error('Biblioteca do Supabase não carregada. Verifique a tag <script> no HTML.');
        return null;
    }
    return supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
}

/**
 * Retorna a instância do cliente Supabase para uso administrativo.
 * ATENÇÃO: Devido a atualizações de segurança recentes do Supabase, chaves secretas (service_role) 
 * são bloqueadas automaticamente se tentarmos usá-las diretamente pelo navegador (arquivos HTML).
 * 
 * Por isso, para o nosso painel estático funcionar, vamos reutilizar a chave pública.
 */
function getSupabaseAdmin() {
    if (typeof supabase === 'undefined') {
        console.error('Biblioteca do Supabase não carregada.');
        return null;
    }
    // Reutilizando a chave pública por conta do bloqueio de chaves secretas no front-end
    return supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
}
