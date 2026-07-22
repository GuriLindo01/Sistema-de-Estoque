import sqlite3
from database.conexao import conectar

def funcaocadastro(usuario, senha, cargo):
    conexao = conectar()
    cursor = conexao.cursor()

    try: 
        cursor.execute('''INSERT INTO usuarios (usuario, senha, cargo) VALUES (?, ?, ?)''', (usuario, senha, cargo))
        conexao.commit()
        return True, cargo
    except sqlite3.IntegrityError:
        return False, "Erro: Usuário já existe"
    finally:
        conexao.close()

def funcaologin(usuario, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''SELECT cargo FROM usuarios WHERE usuario = ? AND senha = ?''', (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()
    
    if resultado:
        cargo = resultado[0]
        return True, cargo
    else:
        return False, "Erro: Usuário ou senha incorretos"