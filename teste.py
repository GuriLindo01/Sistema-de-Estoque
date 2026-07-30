from database.tabelas import criar_tabelas
from funcoes.produtos import adicionar_produto, editar_produto, ver_produtos, excluir_produto

criar_tabelas()

while True:
    print("Escolha uma opção:")
    print("1 - Adicionar produto")
    print("2 - Editar produtos")
    print("3 - Ver produtos adicionados")
    print("4 - Excluir produto")
    print("5 - Sair")

    opcao = input("Digite a opção: ")

    if opcao == "1":
        nome = input("Digite o nome do produto: ")
        descricao = input("Descrição do produto: ")
        categoria = input("Categoria do produto: ")
        quantidade = input("Quantidade do produto: ")
        preco_compra = input("Valor de compra por unidade do produto: ")
        preco_venda = input("Valor de venda por unidade do produto: ")

        sucesso, resultado = adicionar_produto(nome, descricao, categoria, quantidade, preco_compra, preco_venda)
        if sucesso:
            print("Produto adicionado com sucesso!")
        else:
            print("O produto já existe.")

    elif opcao == "2":

        id = input("Digite o ID do produto que deseja editar: ")
        nome = input("Digite o nome do produto: ")
        descricao = input("Descrição do produto: ")
        categoria = input("Categoria do produto: ")
        quantidade = input("Quantidade do produto: ")
        preco_compra = input("Valor de compra por unidade do produto: ")
        preco_venda = input("Valor de venda por unidade do produto: ")

        sucesso, resultado = editar_produto(id, nome, descricao, categoria, quantidade, preco_compra, preco_venda)
        if sucesso:
            print("Produto editado com sucesso!")
        else:
            print("Erro ao editar.")

    elif opcao == "3":
        print("Lista de Produtos")
        ver_produtos()

    elif opcao == "4":
        id = input("Digite o ID do produto que deseja excluir: ")
        sucesso, resultado = excluir_produto(id)

        if sucesso:
            print("Produto excluído com sucesso")
        else:
            print("Erro ao excluir o produto")

    elif opcao == "5":
        print("Saindo do programa...")
        break

    else:
        print("Opção inválida")
