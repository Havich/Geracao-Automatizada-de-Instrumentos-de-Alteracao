import sqlite3

def inicializar_banco():
    # Criar ou conectar banco de dados
    conn = sqlite3.connect('gaia.db')
    cursor = conn.cursor()

    # Cria a tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Cria um usuário de teste
    try:
        cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", ("admin", "1234"))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Usuário já existe

    conn.close()
    print("Banco de dados GAIA pronto para uso!")

if __name__ == "__main__":
    inicializar_banco()