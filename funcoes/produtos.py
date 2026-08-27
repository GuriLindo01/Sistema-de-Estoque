import sqlite3
from database.conexao import conectar

def adicionar_produto(nome, categoria, descricao, quantidade, preco_compra, preco_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''INSERT INTO produtos (nome, categoria, descricao, quantidade, preco_compra, preco_venda) VALUES (?, ?, ?, ?, ?, ?)''', (nome, descricao, categoria, quantidade, preco_compra, preco_venda))
    conexao.commit()
    conexao.close()

def editar_produto(id, nome, categoria, descricao, quantidade, preco_compra, preco_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''UPDATE produtos SET nome = ?, categoria = ?, descricao = ?, quantidade = ?, preco_compra = ?, preco_venda = ? WHERE id = ?''', (nome, descricao, categoria, quantidade, preco_compra, preco_venda, id))
    conexao.commit()
    conexao.close()

def excluir_produto(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()

def ver_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM produtos')
    produto = cursor.fetchall()

    conexao.close()
    return [tuple(produtos) for produtos in produto]

def buscar_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
    produto = cursor.fetchone()

    conexao.close()
    return produto