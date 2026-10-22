import customtkinter as ctk
from PIL import Image
from funcoes.vendas import registrar_venda
from funcoes.produtos import ver_produtos, buscar_produto


class TelaVendas(ctk.CTkFrame):
    def __init__(self, master, controller, usuario="Usuário", cargo="Vendedor"):
        super().__init__(master)
        self.controller = controller

        self.usuario = usuario
        self.cargo = cargo

        self.cor_fundo = "#F1F5F9"
        self.cor_cards = "#FFFFFF"
        self.cor_primaria = "#00569D"
        self.cor_secundaria = "#000020"
        self.cor_texto_principal = "#0C162E"
        self.cor_texto_secundario = "#475569"
        self.cor_bordas = "#E2E8F0"

        self.configure(fg_color=self.cor_fundo)

        self.configurar_imagens()

        self.menu = MenuPrincipal(self, controller, usuario, cargo)
        self.menu.pack(side="top", fill="x")

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.carrinho = []
        self.checkboxes_produtos = {}

        self.tela_venda()

    def configurar_imagens(self):
        try:
            self.imagem_lixeira = ctk.CTkImage(Image.open("imagens/lixeira.png"), size=(15, 15))
            self.imagem_carrinho = ctk.CTkImage(Image.open("imagens/carrinho.png"), size=(15, 15))
            self.imagem_x = ctk.CTkImage(Image.open("imagens/x.png"), size=(19, 19))
            self.circulo_verde = ctk.CTkImage(Image.open("imagens/circulo_verde.png"), size=(14, 14))
            self.circulo_amarelo = ctk.CTkImage(Image.open("imagens/circulo_amarelo.png"), size=(14, 14))
            self.circulo_vermelho = ctk.CTkImage(Image.open("imagens/circulo_vermelho.png"), size=(14, 14))
            self.imagem_configuracoes = ctk.CTkImage(Image.open("imagens/engrenagem.png"), size=(17, 17))

        except Exception:
            self.imagem_lixeira = None
            self.imagem_carrinho = None
            self.imagem_x = None
            self.circulo_verde = None
            self.circulo_amarelo = None
            self.circulo_vermelho = None
            self.imagem_configuracoes = None

    def tela_venda(self):
        self.frame_topo = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        self.frame_topo.pack(fill="x", pady=35)

        self.titulo_vendas = ctk.CTkLabel(self.frame_topo, text="Venda de Produtos", font=("Arial", 20, "bold"), text_color=self.cor_texto_principal)
        self.titulo_vendas.pack(side="left")

        self.frame_esquerda = ctk.CTkFrame(self.frame_conteudo, width=400, fg_color=self.cor_cards)
        self.frame_esquerda.pack(side="left", fill="y", pady=(0, 10), padx=(0, 10))
        self.frame_esquerda.pack_propagate(False)

        self.label_itens_estoque = ctk.CTkLabel(self.frame_esquerda, text="Produtos em Estoque", font=("Arial", 16, "bold"))
        self.label_itens_estoque.pack(pady=(5, 0))

        self.frame_direita = ctk.CTkFrame(self.frame_conteudo, fg_color=self.cor_cards)
        self.frame_direita.pack(expand=True, side="right", fill="both", pady=(0, 10))

        self.label_itens_carrinho = ctk.CTkLabel(self.frame_direita, text="Produtos no Carrinho", font=("Arial", 16, "bold"))
        self.label_itens_carrinho.pack(pady=(5, 0))

        self.frame_produtos = ctk.CTkScrollableFrame(self.frame_esquerda, fg_color=self.cor_fundo)
        self.frame_produtos.pack(side="top", pady= 10, padx=10, expand=True, fill="both")

        self.carregar_lista_produtos()

        self.botao_adicionar_carrinho = ctk.CTkButton(self.frame_esquerda, text="Adicionar produtos ao carrinho", command=self.adicionar_ao_carrinho)
        self.botao_adicionar_carrinho.pack(side="bottom", pady=(0, 10), padx=10, fill="x")

        self.frame_carrinho = ctk.CTkScrollableFrame(self.frame_direita, height=50, fg_color=self.cor_fundo)
        self.frame_carrinho.pack(pady=10, padx=10, fill="x")

        self.container_venda = ctk.CTkFrame(self.frame_direita, fg_color="transparent")
        self.container_venda.pack(padx=10, pady=10, fill="x")

        self.container_venda_inputs = ctk.CTkFrame(self.container_venda, fg_color=self.cor_fundo)
        self.container_venda_inputs.pack(side="left")

        self.container_pagamento = ctk.CTkFrame(self.container_venda_inputs, fg_color="transparent")
        self.container_pagamento.pack(anchor="w", pady=5)

        self.venda_label_pagamento = ctk.CTkLabel(self.container_pagamento, text="Forma de Pagamento:", font=("Arial", 16, "bold"))
        self.venda_label_pagamento.pack(side="left", padx=10)

        self.venda_forma_pagamento = ctk.CTkOptionMenu(self.container_pagamento, values=["Dinheiro", "Cartão", "PIX", "Outro"])
        self.venda_forma_pagamento.pack(side="right", pady=5)

        self.container_desconto = ctk.CTkFrame(self.container_venda_inputs, fg_color="transparent")
        self.container_desconto.pack(anchor="w", pady=5)

        self.venda_label_desconto = ctk.CTkLabel(self.container_desconto, text="Desconto:", font=("Arial", 16, "bold"))
        self.venda_label_desconto.pack(side="left", padx=10)

        self.venda_desconto = ctk.CTkEntry(self.container_desconto, placeholder_text="0")
        self.venda_desconto.pack(side="left", pady=5)
        self.venda_desconto.bind("<KeyRelease>", lambda evento: self.calcular_prevenda())

        self.tipo_desconto = ctk.CTkOptionMenu(self.container_desconto, values=["%", "R$"], width=40, command=lambda valor: self.calcular_prevenda())
        self.tipo_desconto.pack(side="right", padx=10)

        self.container_prevenda = ctk.CTkFrame(self.container_venda, fg_color="transparent")
        self.container_prevenda.pack(side="right", padx=20)

        self.label_prevenda_total = ctk.CTkLabel(self.container_prevenda, text="Total da Venda: R$ 0.00", font=("Arial", 14))
        self.label_prevenda_total.pack(anchor="w", padx=10, pady=2)

        self.label_prevenda_desconto = ctk.CTkLabel(self.container_prevenda, text="Desconto: R$ 0.00", font=("Arial", 14))
        self.label_prevenda_desconto.pack(anchor="w", padx=10, pady=2)

        self.label_prevenda_lucro = ctk.CTkLabel(self.container_prevenda, text="Lucro: R$ 0.00", font=("Arial", 14, "bold"))
        self.label_prevenda_lucro.pack(anchor="w", padx=10, pady=2)

        self.label_erro = ctk.CTkLabel(self.frame_esquerda, text="", text_color="red")
        self.label_erro.pack(pady=5)

        self.venda_efetuar_venda = ctk.CTkButton(self.frame_direita, text="Finalizar Venda", command=self.finalizar_venda)
        self.venda_efetuar_venda.pack(side="bottom", fill="x", padx=10, pady=10)

    def carregar_lista_produtos(self):
        produtos = ver_produtos()

        for produto in produtos:
            id = produto[0]
            nome = produto[1]
            descricao = produto[3]
            quantidade = produto[4]

            var_checkbox = ctk.BooleanVar(value=False)

            checkbox = ctk.CTkCheckBox(self.frame_produtos, text=f"{nome} ({descricao}), {quantidade}", variable=var_checkbox)
            checkbox.pack(anchor="w", pady=2)

            self.checkboxes_produtos[id] = {"var": var_checkbox, "nome": nome}

    def adicionar_ao_carrinho(self):
        ids_no_carrinho = [item["produto_id"] for item in self.carrinho]

        for produto_id, dados in self.checkboxes_produtos.items():
            if not dados["var"].get():
                continue

            if produto_id in ids_no_carrinho:
                self.mostrar_erro(f"'{dados['nome']}' já está no carrinho.")
            else:
                self.criar_linha_carrinho(produto_id, dados["nome"])

            dados["var"].set(False)

        self.calcular_prevenda()

    def criar_linha_carrinho(self, produto_id, nome):
        produto = buscar_produto(produto_id)
        estoque = produto[4]
        preco_compra = produto[5]
        preco_venda = produto[6]

        linha = ctk.CTkFrame(self.frame_carrinho, fg_color="transparent")
        linha.pack(fill="x", pady=2)

        label_nome = ctk.CTkLabel(linha, text=nome, width=150, anchor="w")
        label_nome.pack(side="left", padx=5)

        texto_info = f"Estoque: {estoque} | Compra: R$ {preco_compra:.2f} | Venda: R$ {preco_venda:.2f}"
        label_info = ctk.CTkLabel(linha, text=texto_info, anchor="w")
        label_info.pack(side="left", padx=5)

        entry_quantidade = ctk.CTkEntry(linha, placeholder_text="Quantidade", width=100)
        entry_quantidade.pack(side="left", padx=5)
        entry_quantidade.bind("<KeyRelease>", lambda evento: self.calcular_prevenda())

        item = {
            "produto_id": produto_id,
            "nome": nome,
            "entry_quantidade": entry_quantidade,
            "preco_compra": preco_compra,
            "preco_venda": preco_venda,
            "linha": linha
        }

        botao_remover = ctk.CTkButton(linha, text="Remover", width=80, command=lambda: self.remover_do_carrinho(item))
        botao_remover.pack(side="left", padx=5)

        self.carrinho.append(item)

    def remover_do_carrinho(self, item):
        item["linha"].destroy()
        self.carrinho.remove(item)
        self.calcular_prevenda()

    def calcular_prevenda(self):
        total_venda = 0.0
        lucro_bruto = 0.0

        for item in self.carrinho:
            quantidade_texto = item["entry_quantidade"].get()

            if not quantidade_texto.isdigit():
                continue

            quantidade = int(quantidade_texto)
            total_venda += item["preco_venda"] * quantidade
            lucro_bruto += (item["preco_venda"] - item["preco_compra"]) * quantidade

        desconto_texto = self.venda_desconto.get()
        if desconto_texto == "" or not desconto_texto.replace(".", "", 1).isdigit():
            desconto_texto = "0"

        valor_digitado = float(desconto_texto)
        tipo_desconto = self.tipo_desconto.get()

        if tipo_desconto == "%":
            valor_desconto = total_venda * (valor_digitado / 100)
        else:
            valor_desconto = valor_digitado

        total_final = total_venda - valor_desconto
        lucro_final = lucro_bruto - valor_desconto

        self.label_prevenda_total.configure(text=f"Total da Venda: R$ {total_final:.2f}")
        self.label_prevenda_desconto.configure(text=f"Desconto: R$ {valor_desconto:.2f}")
        self.label_prevenda_lucro.configure(text=f"Lucro: R$ {lucro_final:.2f}")

    def validar_venda(self):
        if len(self.carrinho) == 0:
            return False, "Adicione ao menos um produto ao carrinho."

        forma_pagamento = self.venda_forma_pagamento.get()
        if not forma_pagamento:
            return False, "Selecione a forma de pagamento."

        desconto_texto = self.venda_desconto.get()
        if desconto_texto == "":
            desconto_texto = "0"

        if not desconto_texto.replace(".", "", 1).isdigit():
            return False, "Digite um valor de desconto válido."

        if float(desconto_texto) < 0:
            return False, "O desconto não pode ser negativo."

        for item in self.carrinho:
            quantidade_texto = item["entry_quantidade"].get()

            if not quantidade_texto.isdigit():
                return False, f"Digite uma quantidade válida para '{item['nome']}'."

            quantidade = int(quantidade_texto)

            if quantidade <= 0:
                return False, f"A quantidade de '{item['nome']}' deve ser maior que zero."

            produto = buscar_produto(item["produto_id"])

            if produto is None:
                return False, f"O produto '{item['nome']}' não existe mais no estoque."

            estoque_disponivel = produto[4]

            if quantidade > estoque_disponivel:
                return False, f"Estoque insuficiente para '{item['nome']}'. Disponível: {estoque_disponivel}."

        return True, ""

    def mostrar_erro(self, mensagem):
        self.label_erro.configure(text=mensagem)
        self.label_erro.after(4000, lambda: self.label_erro.configure(text=""))

    def finalizar_venda(self):
        valido, mensagem = self.validar_venda()

        if not valido:
            self.mostrar_erro(mensagem)
            return

        forma_pagamento = self.venda_forma_pagamento.get()
        tipo_desconto = self.tipo_desconto.get()
        desconto_texto = self.venda_desconto.get()
        desconto = float(desconto_texto) if desconto_texto != "" else 0.0

        itens = []
        for item in self.carrinho:
            quantidade = int(item["entry_quantidade"].get())
            itens.append({
                "produto_id": item["produto_id"],
                "quantidade": quantidade
            })

        sucesso, resultado = registrar_venda(itens, forma_pagamento, desconto, tipo_desconto)

        if sucesso:
            self.atualizar_tela()
        else:
            self.mostrar_erro(str(resultado))

    def atualizar_tela(self):
        for widget in self.frame_produtos.winfo_children():
            widget.destroy()

        for widget in self.frame_carrinho.winfo_children():
            widget.destroy()

        self.checkboxes_produtos = {}
        self.carrinho = []

        self.carregar_lista_produtos()
        self.calcular_prevenda()

class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller, usuario="Usuário", cargo="Vendedor"):
        super().__init__(master)

        self.controller = controller
        self.usuario = usuario
        self.cargo = cargo

        self.cor_fundo = "#F1F5F9"
        self.cor_cards = "#FFFFFF"
        self.cor_primaria = "#00569D"
        self.cor_secundaria = "#000020"
        self.cor_texto_principal = "#0C162E"
        self.cor_texto_secundario = "#475569"
        self.cor_bordas = "#E2E8F0"

        self.carregar_imagens()
        self.menu_topo()

        self.menu_sair()
        self.frame_sair.place_forget()

        self.menu_desconectar()
        self.frame_desconectar.place_forget()

    # Menus

    def menu_topo(self):
        self.frame_menu = ctk.CTkFrame(self, fg_color=self.cor_primaria, height=80, corner_radius=0)
        self.frame_menu.pack(pady=0, padx=0, fill="x", anchor="n")
        self.frame_menu.pack_propagate(False)

        self.imagem_logo = ctk.CTkLabel(self.frame_menu, image=self.imagem_logo, text="")
        self.imagem_logo.pack(padx=(30, 30), pady=5, side="left")

        self.container_botoes_menu = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        self.container_botoes_menu.pack(padx=(30, 20), anchor="e", side="right")

        self.botao_desconectar = ctk.CTkButton(self.container_botoes_menu, width=15, height=20, border_width=1, corner_radius=50, border_color=self.cor_bordas, text="", fg_color="transparent", image=self.imagem_usuario_config, command=self.menu_desconectar)
        self.botao_desconectar.pack(pady=(0, 8))

        self.botao_sair = ctk.CTkButton(self.container_botoes_menu, width=15, height=20, border_width=1, corner_radius=50, border_color=self.cor_bordas, text="", fg_color="transparent", image=self.imagem_sair, command=self.menu_sair)
        self.botao_sair.pack()

        self.informacoes_menu = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        self.informacoes_menu.pack(side="left", padx=(0, 30), pady=15, anchor="w")

        self.nome_aplicativo = ctk.CTkLabel(self.informacoes_menu, text="StockDesk", text_color=self.cor_fundo, font=ctk.CTkFont(size=18, weight="bold"))
        self.nome_aplicativo.pack(anchor="w")

        self.informacoes_conta = ctk.CTkLabel(self.informacoes_menu, text=f"{self.usuario}, {self.cargo}", text_color=self.cor_cards, font=("Arial", 12))
        self.informacoes_conta.pack(side="left", pady=(2, 0))

        self.container_botoes = ctk.CTkFrame(self, fg_color=self.cor_secundaria, height=40)
        self.container_botoes.pack(fill="x", pady=0, padx=0, anchor="n")

        self.botao_vendas = ctk.CTkButton(self.container_botoes, text="Vendas", hover_color=self.cor_texto_secundario, fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_carrinho, font=("Arial", 15, "bold"))
        self.botao_vendas.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.botao_estoque = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Estoque", fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_caixa_menu_bold, command=self.abrir_estoque)
        self.botao_estoque.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.botao_historico = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Hist. Vendas", fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_grafico, command=self.abrir_historico)
        self.botao_historico.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.container_destaques = ctk.CTkFrame(self, fg_color="transparent", height=2)
        self.container_destaques.pack(fill="x", pady=0, anchor="n")

        self.destaque_vendas = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_primaria, height=3)
        self.destaque_vendas.pack(side="left", padx=0, pady=0, expand=True, fill="x")

        self.destaque_estoque = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_fundo, height=3)
        self.destaque_estoque.pack(side="left", padx=0, pady=0, expand=True, fill="x")

        self.destaque_historico = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_fundo, height=3)
        self.destaque_historico.pack(side="left", padx=0, pady=0, expand=True, fill="x")
    def menu_desconectar(self):
        if hasattr(self, "frame_desconectar") and self.frame_desconectar.winfo_exists():
            self.frame_desconectar.destroy()

        self.frame_desconectar = ctk.CTkFrame(self.winfo_toplevel(), fg_color=self.cor_cards, height=150, width=300, corner_radius=5)
        self.frame_desconectar.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_desconectar.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_desconectar)

        self.container_fechar = ctk.CTkFrame(self.frame_desconectar, fg_color=self.cor_primaria, height=30, corner_radius=5)
        self.container_fechar.pack(side="top", fill="x", pady=0)

        self.botao_fechar = ctk.CTkButton(self.container_fechar, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_desconectar.place_forget)
        self.botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        self.texto_principal = ctk.CTkLabel(self.container_fechar, text="Desconectar da conta", font=("Arial", 14, "bold"), text_color=self.cor_bordas)
        self.texto_principal.pack(padx=(8, 10), side="left", pady=3)

        self.texto_secundario = ctk.CTkLabel(self.frame_desconectar, text="Tem certeza que deseja sair da conta?", font=("Arial", 14), text_color=self.cor_texto_secundario)
        self.texto_secundario.pack(pady=10)

        self.botao_desconectar = ctk.CTkButton(self.frame_desconectar, fg_color=self.cor_primaria, corner_radius=5, text="Confirmar", height=30, command=self.desconectar)
        self.botao_desconectar.pack(side="left", anchor="sw", padx=(8, 8), pady=8)

        self.botao_cancelar = ctk.CTkButton(self.frame_desconectar, fg_color="transparent", corner_radius=5, border_width=2, border_color=self.cor_primaria, text="Cancelar", text_color=self.cor_primaria, height=30, hover_color=self.cor_fundo, command=self.frame_desconectar.place_forget)
        self.botao_cancelar.pack(side="left", anchor="se", padx=(0, 8), pady=8)
    def menu_sair(self):
        if hasattr(self, "frame_sair") and self.frame_sair.winfo_exists():
            self.frame_sair.destroy()

        self.frame_sair = ctk.CTkFrame(self.winfo_toplevel(), fg_color=self.cor_cards, height=150, width=300, corner_radius=5)
        self.frame_sair.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_sair.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_sair)

        self.container_fechar = ctk.CTkFrame(self.frame_sair, fg_color=self.cor_primaria, height=30, corner_radius=5)
        self.container_fechar.pack(side="top", fill="x", pady=0)

        self.botao_fechar = ctk.CTkButton(self.container_fechar, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_sair.place_forget)
        self.botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        self.texto_principal = ctk.CTkLabel(self.container_fechar, text="Sair do aplicativo", font=("Arial", 14, "bold"), text_color=self.cor_bordas)
        self.texto_principal.pack(padx=(8, 10), side="left", pady=3)

        self.texto_secundario = ctk.CTkLabel(self.frame_sair, text="Tem certeza que deseja sair?", font=("Arial", 14), text_color=self.cor_texto_secundario)
        self.texto_secundario.pack(pady=10)

        self.botao_sair = ctk.CTkButton(self.frame_sair, fg_color=self.cor_primaria, corner_radius=5, text="Confirmar", height=30, command=self.controller.destroy)
        self.botao_sair.pack(side="left", anchor="sw", padx=(8, 8), pady=8)

        self.botao_cancelar = ctk.CTkButton(self.frame_sair, fg_color="transparent", corner_radius=5, border_width=2, border_color=self.cor_primaria, text="Cancelar", text_color=self.cor_primaria, height=30, hover_color=self.cor_fundo, command=self.frame_sair.place_forget)
        self.botao_cancelar.pack(side="left", anchor="se", padx=(0, 8), pady=8)

    # Funções/Carregamento

    def desconectar(self):
        self.frame_desconectar.place_forget()
        self.controller.deslogar()
    def carregar_imagens(self):
        try:
            self.imagem_grafico = ctk.CTkImage(Image.open("imagens/grafico.png"), size=(15, 15))
            self.imagem_caixa_menu_bold = ctk.CTkImage(Image.open("imagens/caixa_menu_bold.png"), size=(15, 15))
            self.imagem_carrinho = ctk.CTkImage(Image.open("imagens/carrinho.png"), size=(15, 15))
            self.imagem_usuario_config = ctk.CTkImage(Image.open("imagens/usuario_config.png"), size=(17, 17))
            self.imagem_sair = ctk.CTkImage(Image.open("imagens/sair_branco.png"), size=(17, 17))
            self.imagem_logo = ctk.CTkImage(Image.open("imagens/caixa_branca.png"), size=(45, 45))
            self.imagem_x = ctk.CTkImage(Image.open("imagens/x.png"), size=(19, 19))

        except Exception:
            self.imagem_grafico = None
            self.imagem_caixa_menu_bold = None
            self.imagem_carrinho = None
            self.imagem_usuario_config = None
            self.imagem_sair = None
            self.imagem_logo = None
            self.imagem_x = None
    def atualizar_informacoes(self, usuario, cargo):
        self.usuario = usuario
        self.cargo = cargo
        self.informacoes_conta.configure(text=f"{self.cargo}, {self.usuario}")

    # Mudança de Telas

    def abrir_estoque(self):
        self.controller.abrir_estoque(self.usuario, self.cargo)
    def abrir_historico(self):
        self.controller.abrir_historico(self.usuario, self.cargo)