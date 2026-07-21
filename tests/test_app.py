"""Testes básicos das rotas principais do console de chamados."""


# ── Páginas públicas ───────────────────────────────────────────────────────

def test_login_renderiza(client):
    r = client.get("/login")
    assert r.status_code == 200
    assert b"login" in r.data.lower() or b"entrar" in r.data.lower()


def test_cadastro_renderiza(client):
    r = client.get("/cadastro")
    assert r.status_code == 200


# ── Proteção de rotas ──────────────────────────────────────────────────────

def test_board_exige_login(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_relatorios_exige_login(client):
    r = client.get("/relatorios", follow_redirects=False)
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_usuarios_exige_login(client):
    r = client.get("/usuarios", follow_redirects=False)
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


# ── Autenticação ───────────────────────────────────────────────────────────

def test_login_credenciais_invalidas(client):
    r = client.post("/login", data={"email": "nao@existe.com", "senha": "errada"})
    assert r.status_code == 200
    assert "inv" in r.data.decode(errors="replace").lower()  # "inválidos"


def test_login_pendente_aguardando_aprovacao(client):
    """Solicitante inativo deve receber mensagem de aprovação pendente."""
    import sqlite3, os
    from werkzeug.security import generate_password_hash

    with sqlite3.connect(os.environ["DB_PATH"]) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO usuarios (nome, email, senha_hash, papel, ativo) "
            "VALUES (?, ?, ?, ?, ?)",
            ("Novo", "pendente@ci.test", generate_password_hash("senha123"), "solicitante", 0),
        )
        conn.commit()

    r = client.post("/login", data={"email": "pendente@ci.test", "senha": "senha123"})
    assert r.status_code == 200
    assert "aprovação" in r.data.decode(errors="replace").lower() or "aguardando" in r.data.decode(errors="replace").lower()


def test_login_admin_redireciona_para_board(client):
    r = client.post(
        "/login",
        data={"email": "admin@ci.test", "senha": "senha123"},
        follow_redirects=False,
    )
    assert r.status_code == 302
    assert "/login" not in r.headers.get("Location", "")


def test_logout_redireciona_para_login(client):
    # Faz login primeiro
    client.post("/login", data={"email": "admin@ci.test", "senha": "senha123"})
    r = client.get("/logout", follow_redirects=False)
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


# ── Board autenticado ──────────────────────────────────────────────────────

def test_board_acessivel_apos_login(client):
    client.post("/login", data={"email": "admin@ci.test", "senha": "senha123"})
    r = client.get("/")
    assert r.status_code == 200
