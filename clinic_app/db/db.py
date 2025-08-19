import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parents[1] / "clinic.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT, rg TEXT, sexo TEXT,
        nascimento TEXT, telefone TEXT, email TEXT, endereco TEXT,
        alergias TEXT, anamnese TEXT, obs TEXT,
        criado_em TEXT, atualizado_em TEXT
    );
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT DEFAULT 'html',
        conteudo_html TEXT NOT NULL,
        meta TEXT, versao INTEGER DEFAULT 1,
        criado_em TEXT, atualizado_em TEXT
    );
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        modelo_id INTEGER NOT NULL,
        titulo TEXT, dados_json TEXT, caminho_pdf TEXT, hash TEXT, criado_em TEXT,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
        FOREIGN KEY (modelo_id) REFERENCES modelos(id)
    );
    """)
    conn.commit()
    conn.close()
