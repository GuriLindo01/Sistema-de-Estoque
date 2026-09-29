from database.conexao import conectar
from funcoes.produtos import buscar_produto


def registrar_venda(itens, forma_pagamento, desconto, tipo_desconto):
    valor_total = 0
    lucro_total = 0

    for item in itens:
        produto = buscar_produto(item["produto_id"])

        if produto is None:
            return False, f"Produto {item['produto_id']} não encontrado"

        preco_compra = produto[5]
        preco_venda = produto[6]
        quantidade = item["quantidade"]

        subtotal = preco_venda * quantidade
        lucro_item = (preco_venda - preco_compra) * quantidade

        valor_total = valor_total + subtotal
        lucro_total = lucro_total + lucro_item

    if tipo_desconto == "R$":
        valor_total = valor_total - desconto
        lucro_total = lucro_total - desconto
    else:
        valor_total = valor_total - (valor_total * (desconto / 100))
        lucro_total = lucro_total - (lucro_total * (desconto / 100))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO vendas (forma_pagamento, desconto, valor_total, lucro_total)
        VALUES (?, ?, ?, ?)
    ''', (forma_pagamento, f"{tipo_desconto}{desconto}", valor_total, lucro_total))

    venda_id = cursor.lastrowid

    for item in itens:
        produto = buscar_produto(item["produto_id"])
        preco_compra = produto[5]
        preco_venda = produto[6]
        quantidade = item["quantidade"]
        subtotal = preco_venda * quantidade
        lucro_item = (preco_venda - preco_compra) * quantidade

        cursor.execute('''
            INSERT INTO itens_venda 
            (venda_id, produto_id, quantidade, preco_unitario, preco_compra_unitario, subtotal, lucro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (venda_id, item["produto_id"], quantidade, preco_venda, preco_compra, subtotal, lucro_item))

        cursor.execute('''
            UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?
        ''', (quantidade, item["produto_id"]))

    conexao.commit()
    conexao.close()

    return True, venda_id

def ver_vendas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    conexao.close()
    return vendas

def ver_itens_venda(venda_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM itens_venda WHERE venda_id = ?', (venda_id,))
    itens = cursor.fetchall()
    conexao.close()
    return itens