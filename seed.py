"""
Cria o banco (console.db) a partir do schema.sql e popula com dados de exemplo.
Rodar uma vez: python seed.py
"""
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "console.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn):
    with open("schema.sql", encoding="utf-8") as f:
        conn.executescript(f.read())


def seed(conn):
    cur = conn.cursor()

    # Usuários
    usuarios = [
        ("Oscar Carvalho", "oscar@athos.com.br", "oscar123", "admin"),
        ("Rafael Costa", "rafael@athos.com.br", "rafael123", "atendente"),
        ("Marina Souza", "marina@athos.com.br", "marina123", "atendente"),
    ]
    for nome, email, senha, papel in usuarios:
        cur.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, papel) VALUES (?, ?, ?, ?)",
            (nome, email, generate_password_hash(senha), papel),
        )

    # Setores
    setores = ["Infra", "Hardware", "Financeiro", "Logística", "Suporte"]
    for nome in setores:
        cur.execute("INSERT INTO setores (nome) VALUES (?)", (nome,))

    conn.commit()

    # Chamados de exemplo
    chamados = [
        ("Totem iMin S1 não emite Pix", "Loja Alphaville relata falha na geração do QR code após atualização.", "alta", "aberto", 4, 2, None),
        ("Gôndola smart offline — Setor B", "Sensor de peso não sincroniza com o painel central.", "media", "aberto", 24, 1, None),
        ("Solicitação de manual do coletor de dados", "Cliente pede manual atualizado do modelo CD-200.", "baixa", "aberto", 48, 5, None),
        ("Falha crítica no servidor de totens — filial SP", "3 totens fora do ar simultaneamente. Equipe de infra acionada.", "alta", "andamento", 8, 1, 2),
        ("Ajuste de leitura em data collector DC-150", "Divergência de leituras em ambiente com alta umidade.", "media", "andamento", 24, 2, 1),
        ("Peça de reposição — leitor de código de barras", "Aguardando confirmação do estoque com o setor de logística.", "media", "aguardando", 48, 4, 3),
        ("Aprovação orçamentária — upgrade de licença", "Aguardando retorno do setor financeiro sobre o orçamento.", "baixa", "aguardando", 72, 3, 1),
        ("Reset de configuração — totem MEVAM", "Configuração de rede restaurada. Cliente confirmou funcionamento.", "media", "resolvido", 24, 5, 2),
        ("Dúvida sobre relatório de vendas", "Explicado processo de exportação de relatório mensal.", "baixa", "resolvido", 48, 5, 3),
    ]
    for titulo, desc, prioridade, status, sla, setor_id, atribuido_a in chamados:
        cur.execute(
            """INSERT INTO chamados
               (titulo, descricao, prioridade, status, sla_horas, setor_id, atribuido_a, criado_por)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (titulo, desc, prioridade, status, sla, setor_id, atribuido_a, 1),
        )
        chamado_id = cur.lastrowid
        cur.execute(
            """INSERT INTO movimentacoes (chamado_id, status_anterior, status_novo, usuario_id)
               VALUES (?, NULL, ?, ?)""",
            (chamado_id, status, 1),
        )

    conn.commit()


if __name__ == "__main__":
    conn = get_conn()
    init_schema(conn)
    seed(conn)
    conn.close()
    print("Banco console.db criado e populado com sucesso.")
    print("Login de teste -> email: oscar@athos.com.br | senha: oscar123")
