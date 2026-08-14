-- Schema para a tabela de inscrições
CREATE TABLE inscricoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    cristao BOOLEAN NOT NULL,
    tempo_cristao TEXT NOT NULL,
    batizado_aguas BOOLEAN NOT NULL,
    batizado_espirito TEXT NOT NULL,
    em_comunhao BOOLEAN NOT NULL,
    tempo_comunhao TEXT,
    motivo TEXT NOT NULL
);
