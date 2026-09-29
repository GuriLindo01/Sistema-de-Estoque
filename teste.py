from database.tabelas import criar_tabelas
from funcoes.produtos import adicionar_produto, editar_produto, ver_produtos, excluir_produto
from funcoes.vendas import registrar_venda, ver_vendas, ver_itens_venda

criar_tabelas()

while True:
    print("Escolha uma opção:")
    print("1 - Ver vendas")
    print("2 - Sair")

    opcao = input("Digite a opção: ")

    if opcao == "1":
        print("Lista de Vendas")
        vendas = ver_vendas()

        for venda in vendas:
            print(f"ID: {venda[0]} | Data: {venda[1]} | Pagamento: {venda[2]} | Desconto: {venda[3]} | Total: {venda[4]} | Lucro: {venda[5]}")
            itens = ver_itens_venda(venda[0])
            for item in itens:
                print(f"   Produto ID: {item[2]} | Qtd: {item[3]} | Preço unit: {item[4]} | Subtotal: {item[6]}")

    elif opcao == "2":
        break

    else:
        print("invalido")