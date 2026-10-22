import customtkinter as ctk
from PIL import Image
from funcoes import vendas
from funcoes.produtos import buscar_produto


class TelaHistorico(ctk.CTkFrame):
    def __init__(self, master, controller, usuario="Usuário", cargo="Vendedor"):
        super().__init__(master)
        self.controller = controller

        self.usuario = usuario
        self.cargo = cargo
        self.cargo_gerente = cargo == "Gerente"

        self.cor_fundo = "#F1F5F9"
        self.cor_cards = "#FFFFFF"
        self.cor_primaria = "#00569D"
        self.cor_texto_principal = "#0C162E"
        self.cor_texto_secundario = "#475569"
        self.cor_bordas = "#E2E8F0"

        self.larguras_colunas = [60, 100, 80, 220, 100, 120, 110, 110, 100]

        self.configure(fg_color=self.cor_fundo)

        self.configurar_imagens()

        self.menu = MenuPrincipal(self, controller, usuario, cargo)
        self.menu.pack(side="top", fill="x")

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.criar_cabecalho_tabela()
        self.criar_container_vendas()
        self.configurar_cargo(cargo)

    def configurar_cargo(self, cargo):
        self.cargo = cargo
        self.cargo_gerente = cargo == "Gerente"

        self.criar_colunas_tabela(self.frame_header)

        if self.cargo_gerente:
            self.acoes_header.grid(row=0, column=8, sticky="nsew", pady=5)
        else:
            self.acoes_header.grid_remove()

        self.atualizar_lista_vendas()

    def configurar_imagens(self):
        try:
            self.imagem_lixeira = ctk.CTkImage(Image.open("imagens/lixeira.png"), size=(15, 15))
            self.imagem_voltar = ctk.CTkImage(Image.open("imagens/voltar.png"), size=(15, 15))
            self.imagem_x = ctk.CTkImage(Image.open("imagens/x.png"), size=(19, 19))

        except Exception:
            self.imagem_lixeira = None
            self.imagem_voltar = None
            self.imagem_x = None

    def criar_colunas_tabela(self, frame):
        ultima = len(self.larguras_colunas) - 1

        for coluna, largura in enumerate(self.larguras_colunas):
            if coluna == ultima and not self.cargo_gerente:
                frame.grid_columnconfigure(coluna, weight=0, minsize=0, uniform="")
            else:
                frame.grid_columnconfigure(coluna, weight=largura, minsize=largura, uniform="tabela")

    def criar_cabecalho_tabela(self):
        self.frame_topo = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        self.frame_topo.pack(fill="x", pady=35)

        self.titulo_historico = ctk.CTkLabel(self.frame_topo, text="Histórico de Vendas", font=("Arial", 20, "bold"), text_color=self.cor_texto_principal)
        self.titulo_historico.pack(side="left")

        self.frame_header = ctk.CTkFrame(self.frame_conteudo, height=40, fg_color=self.cor_cards, corner_radius=6, border_width=1, border_color=self.cor_bordas)
        self.frame_header.pack(fill="x", pady=(0, 10))
        self.frame_header.pack_propagate(False)

        self.criar_colunas_tabela(self.frame_header)

        self.id_header = ctk.CTkLabel(self.frame_header, text="ID", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.id_header.grid(row=0, column=0, sticky="nsew", pady=5)

        self.data_header = ctk.CTkLabel(self.frame_header, text="Data", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.data_header.grid(row=0, column=1, sticky="nsew", pady=5)

        self.hora_header = ctk.CTkLabel(self.frame_header, text="Hora", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.hora_header.grid(row=0, column=2, sticky="nsew", pady=5)

        self.produtos_header = ctk.CTkLabel(self.frame_header, text="Produtos", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.produtos_header.grid(row=0, column=3, sticky="nsew", pady=5)

        self.forma_pagamento_header = ctk.CTkLabel(self.frame_header, text="Pagamento", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.forma_pagamento_header.grid(row=0, column=4, sticky="nsew", pady=5)

        self.desconto_header = ctk.CTkLabel(self.frame_header, text="Desconto", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.desconto_header.grid(row=0, column=5, sticky="nsew", pady=5)

        self.valor_total_header = ctk.CTkLabel(self.frame_header, text="Valor total", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.valor_total_header.grid(row=0, column=6, sticky="nsew", pady=5)

        self.lucro_header = ctk.CTkLabel(self.frame_header, text="Lucro total", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.lucro_header.grid(row=0, column=7, sticky="nsew", pady=5)

        self.acoes_header = ctk.CTkLabel(self.frame_header, text="Ações", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")

    def criar_container_vendas(self):
        self.container_vendas = ctk.CTkScrollableFrame(self.frame_conteudo, fg_color="transparent", corner_radius=0, border_width=0)
        self.container_vendas.pack(fill="both", expand=True, pady=(8, 0), padx=0)
        self.container_vendas._scrollbar.grid_forget()

    def atualizar_lista_vendas(self):
        for widget in self.container_vendas.winfo_children():
            widget.destroy()

        for venda in vendas.ver_vendas():
            self.criar_linha_venda(venda)

    def formatar_desconto(self, texto, subtotal, valor_total):
        if texto.startswith("R$"):
            valor = float(texto.replace("R$", ""))
            return f"R$ {valor:.2f}"

        if texto.startswith("%"):
            percentual = float(texto.replace("%", ""))
            valor_em_reais = subtotal - valor_total
            return f"R$ {valor_em_reais:.2f} ({percentual:.0f}%)"

        return texto

    def criar_linha_venda(self, venda):
        venda_id, data_venda, forma_pagamento, desconto, subtotal, valor_total, lucro_total = venda
        data, hora = data_venda.split(" ")

        nomes_produtos = []
        for item in vendas.ver_itens_venda(venda_id):
            produto = buscar_produto(item[2])
            if produto:
                nomes_produtos.append(produto[1])

        texto_produtos = ", ".join(nomes_produtos[:2]) or "-"
        if len(nomes_produtos) > 2:
            texto_produtos += f" +{len(nomes_produtos) - 2}"

        card = ctk.CTkFrame(self.container_vendas, height=40, fg_color=self.cor_cards, border_width=1, border_color=self.cor_bordas, corner_radius=6)
        card.pack(fill="x", pady=(0, 5))
        card.pack_propagate(False)

        self.criar_colunas_tabela(card)

        label_id = ctk.CTkLabel(card, text=f"#{venda_id}", text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        label_id.grid(row=0, column=0, sticky="nsew", pady=10)

        label_data = ctk.CTkLabel(card, text=data, text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        label_data.grid(row=0, column=1, sticky="nsew", pady=5)

        label_hora = ctk.CTkLabel(card, text=hora, text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        label_hora.grid(row=0, column=2, sticky="nsew", pady=5)

        label_produtos = ctk.CTkLabel(card, text=texto_produtos, text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        label_produtos.grid(row=0, column=3, sticky="nsew", pady=5)

        label_pagamento = ctk.CTkLabel(card, text=forma_pagamento, text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        label_pagamento.grid(row=0, column=4, sticky="nsew", pady=5)

        label_desconto = ctk.CTkLabel(card, text=self.formatar_desconto(desconto, subtotal, valor_total), text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        label_desconto.grid(row=0, column=5, sticky="nsew", pady=5)

        label_valor_total = ctk.CTkLabel(card, text=f"R$ {valor_total:.2f}", text_color=self.cor_texto_secundario, font=("Arial", 12, "bold"), anchor="center")
        label_valor_total.grid(row=0, column=6, sticky="nsew", pady=5)

        label_lucro_total = ctk.CTkLabel(card, text=f"R$ {lucro_total:.2f}", text_color="#16A34A", font=("Arial", 12, "bold"), anchor="center")
        label_lucro_total.grid(row=0, column=7, sticky="nsew", pady=5)

        if self.cargo_gerente:
            frame_acoes = ctk.CTkFrame(card, fg_color="transparent")
            frame_acoes.grid(row=0, column=8)

            botao_reverter = ctk.CTkButton(frame_acoes, text="", image=self.imagem_voltar, width=35, height=35, corner_radius=6, fg_color=self.cor_primaria, hover_color="#00477F", command=lambda: self.tela_reverter(venda_id))
            botao_reverter.pack(side="left", padx=5)

            botao_excluir = ctk.CTkButton(frame_acoes, text="", image=self.imagem_lixeira, width=35, height=35, corner_radius=6, fg_color="#DC2626", hover_color="#B91C1C", command=lambda: self.tela_excluir(venda_id))
            botao_excluir.pack(side="left", padx=5)

    def tela_excluir(self, venda_id):
        if hasattr(self, "frame_excluir") and self.frame_excluir.winfo_exists():
            self.frame_excluir.destroy()

        self.frame_excluir = ctk.CTkFrame(self, fg_color=self.cor_cards, height=150, width=300, corner_radius=5)
        self.frame_excluir.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_excluir.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_excluir)

        container_fechar = ctk.CTkFrame(self.frame_excluir, fg_color=self.cor_primaria, height=30, corner_radius=5)
        container_fechar.pack(side="top", fill="x", pady=0)

        botao_fechar = ctk.CTkButton(container_fechar, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_excluir.place_forget)
        botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        texto_principal = ctk.CTkLabel(container_fechar, text="Excluir venda", font=("Arial", 14, "bold"), text_color=self.cor_bordas)
        texto_principal.pack(padx=(8, 10), side="left", pady=3)

        texto_secundario = ctk.CTkLabel(self.frame_excluir, text="Tem certeza que deseja excluir essa venda?\nO estoque NÃO será alterado.", font=("Arial", 13), text_color=self.cor_texto_secundario, justify="center")
        texto_secundario.pack(pady=10)

        botao_confirmar = ctk.CTkButton(self.frame_excluir, fg_color=self.cor_primaria, corner_radius=5, text="Confirmar", height=30, command=lambda: self.excluir(venda_id))
        botao_confirmar.pack(side="left", anchor="sw", padx=(8, 8), pady=8)

        botao_cancelar = ctk.CTkButton(self.frame_excluir, fg_color="transparent", corner_radius=5, border_width=2, border_color=self.cor_primaria, text="Cancelar", text_color=self.cor_primaria, height=30, hover_color=self.cor_fundo, command=self.frame_excluir.place_forget)
        botao_cancelar.pack(side="left", anchor="se", padx=(0, 8), pady=8)

    def excluir(self, venda_id):
        vendas.excluir_venda(venda_id)
        self.frame_excluir.place_forget()
        self.atualizar_lista_vendas()

    def tela_reverter(self, venda_id):
        if hasattr(self, "frame_reverter") and self.frame_reverter.winfo_exists():
            self.frame_reverter.destroy()

        self.frame_reverter = ctk.CTkFrame(self, fg_color=self.cor_cards, height=150, width=300, corner_radius=5)
        self.frame_reverter.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_reverter.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_reverter)

        container_fechar = ctk.CTkFrame(self.frame_reverter, fg_color=self.cor_primaria, height=30, corner_radius=5)
        container_fechar.pack(side="top", fill="x", pady=0)

        botao_fechar = ctk.CTkButton(container_fechar, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_reverter.place_forget)
        botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        texto_principal = ctk.CTkLabel(container_fechar, text="Reverter venda", font=("Arial", 14, "bold"), text_color=self.cor_bordas)
        texto_principal.pack(padx=(8, 10), side="left", pady=3)

        texto_secundario = ctk.CTkLabel(self.frame_reverter, text="Tem certeza que deseja reverter essa venda?\nO estoque dos produtos será devolvido.", font=("Arial", 13), text_color=self.cor_texto_secundario, justify="center")
        texto_secundario.pack(pady=10)

        botao_confirmar = ctk.CTkButton(self.frame_reverter, fg_color=self.cor_primaria, corner_radius=5, text="Confirmar", height=30, command=lambda: self.reverter(venda_id))
        botao_confirmar.pack(side="left", anchor="sw", padx=(8, 8), pady=8)

        botao_cancelar = ctk.CTkButton(self.frame_reverter, fg_color="transparent", corner_radius=5, border_width=2, border_color=self.cor_primaria, text="Cancelar", text_color=self.cor_primaria, height=30, hover_color=self.cor_fundo, command=self.frame_reverter.place_forget)
        botao_cancelar.pack(side="left", anchor="se", padx=(0, 8), pady=8)

    def reverter(self, venda_id):
        vendas.reverter_venda(venda_id)
        self.frame_reverter.place_forget()
        self.atualizar_lista_vendas()


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
        self.cor_texto_secundario = "#475569"
        self.cor_bordas = "#E2E8F0"

        self.carregar_imagens()
        self.menu_topo()

        self.menu_sair()
        self.frame_sair.place_forget()

        self.menu_desconectar()
        self.frame_desconectar.place_forget()

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

        self.botao_vendas = ctk.CTkButton(self.container_botoes, text="Vendas", hover_color=self.cor_texto_secundario, fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_carrinho, command=self.abrir_vendas)
        self.botao_vendas.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.botao_estoque = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Estoque", fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_caixa_menu_bold, command=self.abrir_estoque)
        self.botao_estoque.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.botao_historico = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Hist. Vendas", font=("Arial", 15, "bold"), fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_grafico)
        self.botao_historico.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.container_destaques = ctk.CTkFrame(self, fg_color="transparent", height=2)
        self.container_destaques.pack(fill="x", pady=0, anchor="n")

        self.destaque_vendas = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_fundo, height=3)
        self.destaque_vendas.pack(side="left", padx=0, pady=0, expand=True, fill="x")

        self.destaque_estoque = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_fundo, height=3)
        self.destaque_estoque.pack(side="left", padx=0, pady=0, expand=True, fill="x")

        self.destaque_historico = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_primaria, height=3)
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

    def abrir_vendas(self):
        self.controller.abrir_vendas(self.usuario, self.cargo)

    def abrir_estoque(self):
        self.controller.abrir_estoque(self.usuario, self.cargo)