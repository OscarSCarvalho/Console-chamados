"""
Configura um banco SQLite temporário antes de qualquer import do app,
garantindo que os testes nunca toquem no console.db de produção.
"""
import os
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

# ── Banco temporário ── deve ser definido ANTES de importar app ────────────
_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_db.close()
os.environ["DB_PATH"] = _db.name
os.environ.setdefault("SECRET_KEY", "test-secret-key-ci")

# Aplica o schema base para que migrate_db() encontre as tabelas esperadas
_schema_path = os.path.join(os.path.dirname(__file__), "..", "schema.sql")
with sqlite3.connect(_db.name) as _conn:
    with open(_schema_path) as _f:
        _conn.executescript(_f.read())

import app as _flask_app  # noqa: E402


@pytest.fixture(scope="session")
def flask_app():
    _flask_app.app.config.update(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "RATELIMIT_ENABLED": False,
        }
    )

    # Usuário admin para testes de autenticação
    with sqlite3.connect(_db.name) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO usuarios (nome, email, senha_hash, papel, ativo) "
            "VALUES (?, ?, ?, ?, ?)",
            ("Admin CI", "admin@ci.test", generate_password_hash("senha123"), "admin", 1),
        )
        conn.commit()

    yield _flask_app.app

    try:
        os.unlink(_db.name)
    except PermissionError:
        pass  # Windows mantém o arquivo bloqueado; o SO limpa ao reiniciar


@pytest.fixture
def client(flask_app):
    """Cliente HTTP isolado — sessão zerada a cada teste."""
    with flask_app.test_client() as c:
        yield c
