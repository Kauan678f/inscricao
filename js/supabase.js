// Arquivo de configuração do cliente Supabase

// TODO: Substitua pelos valores do seu projeto Supabase (encontrados em Project Settings -> API)
const SUPABASE_URL = 'https://mzyvdcuuqjrxgjbhwczf.supabase.co'; // Lembre-se de colocar sua URL!
const SUPABASE_ANON_KEY = 'sb_publishable_WJLyKpWN9g7N5-UT2NDjww__E3GI1QC';

// A service_role key só deve ser usada no painel administrativo.
// ATENÇÃO: Em projetos reais com backend, esta chave JAMAIS deve ir para o front-end público,
// pois dá acesso total ao banco bypassando as regras RLS.
// Como este é um projeto V1 100% front-end e o admin é estático, 
// a chave fica aqui exclusivamente para uso em admin.js.
const SUPABASE_SERVICE_ROLE_KEY = 'sb_secret_HsaaZQxVp8NkArl4pDQM7w__pVyRe7L';

/**
 * Retorna a instância do cliente Supabase para uso público (formulário de inscrição).
 * Utiliza a anon key. Sujeito às regras RLS (só permite INSERT).
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
 * Utiliza a service_role key (bypassa RLS e permite SELECT nas inscrições).
 */
function getSupabaseAdmin() {
    if (typeof supabase === 'undefined') {
        console.error('Biblioteca do Supabase não carregada. Verifique a tag <script> no HTML.');
        return null;
    }
    return supabase.createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
}
