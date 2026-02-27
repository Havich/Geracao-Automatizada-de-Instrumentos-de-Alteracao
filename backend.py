import sqlite3

def autenticar(usuario, senha):
    """Verifica se o login e senha existem no banco."""
    conn = sqlite3.connect('gaia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE login = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def cadastrar(usuario, senha):
    """Tenta cadastrar e retorna True (sucesso) ou False (erro)."""
    try:
        conn = sqlite3.connect('gaia.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False