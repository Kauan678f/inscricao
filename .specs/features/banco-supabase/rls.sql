-- Habilitar Row Level Security na tabela inscricoes
ALTER TABLE inscricoes ENABLE ROW LEVEL SECURITY;

-- Permitir INSERT para visitantes anônimos (qualquer um pode preencher o formulário)
CREATE POLICY "allow_anon_insert"
ON inscricoes
FOR INSERT
TO anon
WITH CHECK (true);

-- Negar SELECT público para visitantes anônimos
-- Isso garante que as inscrições não fiquem expostas publicamente.
-- Nota: O painel administrativo (que utilizará a service_role key do Supabase) 
-- irá ignorar o RLS e conseguirá buscar todas as inscrições para a listagem.
CREATE POLICY "deny_anon_select"
ON inscricoes
FOR SELECT
TO anon
USING (false);
