import sqlite3
from database.conexao import conectar

def adicionar_produto(nome, descricao, categoria, quantidade, preco_compra, preco_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    try: 
        cursor.execute('''INSERT INTO produtos (nome, descricao, categoria, quantidade, preco_compra, preco_venda) VALUES (?, ?, ?, ?, ?, ?)''', (nome, descricao, categoria, quantidade, preco_compra, preco_venda))
        conexao.commit()
        return True, "Produto criado"
    except sqlite3.IntegrityError:
        return False, "Erro: O produto já existe"
    finally:
        conexao.close()

def editar_produto(id, nome, descricao, categoria, quantidade, preco_compra, preco_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute('''UPDATE produtos SET nome = ?, descricao = ?, categoria = ?, quantidade = ?, preco_compra = ?, preco_venda = ? WHERE id = ?''', (nome, descricao, categoria, quantidade, preco_compra, preco_venda, id))
        conexao.commit()
        return True, "Produto atualizado"
    except sqlite3.Error as e:
        return False, f"Erro ao atualizar: {e}"
    finally:
        conexao.close()

def excluir_produto(id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute('DELETE FROM produtos WHERE id = ?', (id))
        conexao.commit()
        return True, "Produto excluido"
    except sqlite3.Error as e:
        return False, "Erro ao excluir o produto"
    finally:
        conexao.close()

def ver_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM produtos')
    produto = cursor.fetchall()
    print(produto)

    conexao.close()