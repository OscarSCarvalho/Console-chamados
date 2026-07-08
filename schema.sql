-- Console de Chamados — Athos Tecnologia
-- Schema SQLite (sem ORM, sqlite3 puro)

DROP TABLE IF EXISTS movimentacoes;
DROP TABLE IF EXISTS chamados;
DROP TABLE IF EXISTS setores;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    senha_hash  TEXT NOT NULL,
    papel       TEXT NOT NULL CHECK (papel IN ('atendente', 'admin')) DEFAULT 'atendente',
    ativo       INTEGER NOT NULL DEFAULT 1,
    criado_em   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE setores (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL UNIQUE
);

CREATE TABLE chamados (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo        TEXT NOT NULL,
    descricao     TEXT,
    prioridade    TEXT NOT NULL CHECK (prioridade IN ('alta', 'media', 'baixa')) DEFAULT 'media',
    status        TEXT NOT NULL CHECK (status IN ('aberto', 'andamento', 'aguardando', 'resolvido')) DEFAULT 'aberto',
    sla_horas     INTEGER NOT NULL DEFAULT 24,
    setor_id      INTEGER REFERENCES setores(id),
    atribuido_a   INTEGER REFERENCES usuarios(id),
    criado_por    INTEGER REFERENCES usuarios(id),
    criado_em     TEXT NOT NULL DEFAULT (datetime('now')),
    atualizado_em TEXT NOT NULL DEFAULT (datetime('now')),
    resolvido_em  TEXT
);

CREATE TABLE movimentacoes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado_id      INTEGER NOT NULL REFERENCES chamados(id),
    status_anterior TEXT,
    status_novo     TEXT NOT NULL,
    usuario_id      INTEGER REFERENCES usuarios(id),
    criado_em       TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE comentarios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado_id  INTEGER NOT NULL REFERENCES chamados(id),
    usuario_id  INTEGER NOT NULL REFERENCES usuarios(id),
    texto       TEXT NOT NULL,
    criado_em   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_chamados_status ON chamados(status);
CREATE INDEX idx_movimentacoes_chamado ON movimentacoes(chamado_id);
CREATE INDEX idx_comentarios_chamado ON comentarios(chamado_id);
