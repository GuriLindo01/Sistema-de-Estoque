import customtkinter as ctk
from PIL import Image
from funcoes import produtos
import json
import os

class TelaEstoque(ctk.CTkFrame):
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

        self.larguras_colunas = [70, 70, 180, 130, 180, 100, 120, 120, 100, 130]

        self.configure(fg_color=self.cor_fundo)

        self.configurar_imagens()

        self.menu = MenuPrincipal(self, controller, usuario, cargo)
        self.menu.pack(side="top", fill="x")

        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.criar_cabecalho_tabela()
        self.criar_container_produtos()
        self.configurar_cargo(cargo)

    def configurar_cargo(self, cargo):
        self.cargo = cargo
        self.cargo_gerente = cargo == "Gerente"

        self.criar_colunas_tabela(self.frame_header)

        if self.cargo_gerente:
            self.botao_configurar.pack(side="left", padx=5)
            self.botao_adicionar.grid(row=0, column=9, pady=5)
        else:
            self.botao_configurar.pack_forget()
            self.botao_adicionar.grid_remove()

        self.atualizar_lista_produtos()

    #Configurações da Tela

    def configurar_imagens(self):
        try:
            self.imagem_lixeira = ctk.CTkImage(Image.open("imagens/lixeira.png"), size=(15, 15))
            self.imagem_editar = ctk.CTkImage(Image.open("imagens/editar.png"), size=(15, 15))
            self.imagem_x = ctk.CTkImage(Image.open("imagens/x.png"), size=(19, 19))
            self.circulo_verde = ctk.CTkImage(Image.open("imagens/circulo_verde.png"), size=(14, 14))
            self.circulo_amarelo = ctk.CTkImage(Image.open("imagens/circulo_amarelo.png"), size=(14, 14))
            self.circulo_vermelho = ctk.CTkImage(Image.open("imagens/circulo_vermelho.png"), size=(14, 14))
            self.imagem_configuracoes = ctk.CTkImage(Image.open("imagens/engrenagem.png"), size=(17, 17))

        except Exception:
            self.imagem_lixeira = None
            self.imagem_editar = None
            self.imagem_x = None
            self.circulo_verde = None
            self.circulo_amarelo = None
            self.circulo_vermelho = None
            self.imagem_configuracoes = None

    def criar_colunas_tabela(self, frame):
        ultima = len(self.larguras_colunas) - 1

        for coluna, largura in enumerate(self.larguras_colunas):
            if coluna == ultima and not self.cargo_gerente:
                frame.grid_columnconfigure(coluna, weight=0, minsize=0, uniform="")
            else:
                frame.grid_columnconfigure(coluna, weight=largura, minsize=largura, uniform="tabela")

    def criar_container_produtos(self):
        self.container_produtos = ctk.CTkScrollableFrame(self.frame_conteudo, fg_color="transparent", corner_radius=0, border_width=0)
        self.container_produtos.pack(fill="both", expand=True, pady=(8, 0), padx=0)
        self.container_produtos._scrollbar.grid_forget()

    #Configurações do Estoque

    def atualizar_lista_produtos(self):
        for widget in self.container_produtos.winfo_children():
            widget.destroy()

        aceitavel, razoavel, baixa = self.carregar_configuracao_quantidade()
        for produto in produtos.ver_produtos():
            self.criar_linha_produto(produto, aceitavel, razoavel, baixa)

    def carregar_configuracao_quantidade(self):
        aceitavel, razoavel, baixa = 100, 50, 10

        if os.path.exists("configuracao.json"):
            try:
                with open("configuracao.json", "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                    if dados.get("configurado") is True:
                        aceitavel = dados.get("aceitavel", aceitavel)
                        razoavel = dados.get("razoavel", razoavel)
                        baixa = dados.get("baixa", baixa)
            except Exception:
                pass
        return int(aceitavel), int(razoavel), int(baixa)

    #Validações

    def destacar_erro(self, entry):
        entry.delete(0, "end")
        entry.configure(border_color="red", placeholder_text_color="red")
        entry.after(3000, lambda: entry.configure(border_color="gray", placeholder_text_color="gray"))

    def preco_float(self, valor_str):
        return float(valor_str.replace(',', '.'))

    def validar_produto(self, nome, categoria, descricao, quantidade, preco_compra, preco_venda):
        if not nome or not categoria or not descricao or not quantidade or not preco_compra or not preco_venda:
            return False, "Preencha todos os campos.", None

        if len(nome) < 3 or len(nome) > 15:
            return False, "O nome do produto deve ter entre 3 e 15 caracteres.", "nome"

        if len(categoria) < 3 or len(categoria) > 15:
            return False, "A categoria do produto deve ter entre 3 e 15 caracteres.", "categoria"

        if len(descricao) > 20:
            return False, "A descrição do produto deve ter no máximo 20 caracteres.", "descricao"

        if len(quantidade) > 6:
            return False, "A quantidade do produto deve ter entre 1 e 6 caracteres.", "quantidade"

        if len(preco_compra) > 10:
            return False, "O preço de compra do produto deve ter entre 1 e 10 caracteres.", "preco_compra"

        if len(preco_venda) > 10:
            return False, "O preço de venda do produto deve ter entre 1 e 10 caracteres.", "preco_venda"

        if not quantidade.isdigit():
            return False, "A quantidade do produto deve ser um número.", "quantidade"

        if not preco_compra.replace(',', '.').replace('.', '', 1).isdigit():
            return False, "O preço de compra do produto deve ser um número.", "preco_compra"

        if not preco_venda.replace(',', '.').replace('.', '', 1).isdigit():
            return False, "O preço de venda do produto deve ser um número.", "preco_venda"

        return True, "", None

    #Criação da Tela

    def criar_cabecalho_tabela(self):
        self.frame_topo = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        self.frame_topo.pack(fill="x", pady=35)

        self.titulo_estoque = ctk.CTkLabel(self.frame_topo, text="Lista de Produtos em Estoque", font=("Arial", 20, "bold"), text_color=self.cor_texto_principal)
        self.titulo_estoque.pack(side="left")

        self.botao_configurar = ctk.CTkButton(self.frame_topo, fg_color="transparent", text="", image=self.imagem_configuracoes, height=20, width=20, hover_color=self.cor_cards, command=self.tela_configuracao)

        self.frame_header = ctk.CTkFrame(self.frame_conteudo, height=40, fg_color=self.cor_cards, corner_radius=6, border_width=1, border_color=self.cor_bordas)
        self.frame_header.pack(fill="x", pady=(0, 10))
        self.frame_header.pack_propagate(False)

        self.criar_colunas_tabela(self.frame_header)

        self.aviso_header = ctk.CTkLabel(self.frame_header, text="Inf.", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.aviso_header.grid(row=0, column=0, sticky="nsew", pady=5)

        self.id_header = ctk.CTkLabel(self.frame_header, text="ID", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.id_header.grid(row=0, column=1, sticky="nsew", pady=5)

        self.nome_header = ctk.CTkLabel(self.frame_header, text="Nome", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.nome_header.grid(row=0, column=2, sticky="nsew", pady=5)

        self.categoria_header = ctk.CTkLabel(self.frame_header, text="Categoria", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.categoria_header.grid(row=0, column=3, sticky="nsew", pady=5)

        self.descricao_header = ctk.CTkLabel(self.frame_header, text="Descrição", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.descricao_header.grid(row=0, column=4, sticky="nsew", pady=5)

        self.quantidade_header = ctk.CTkLabel(self.frame_header, text="Quantidade", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.quantidade_header.grid(row=0, column=5, sticky="nsew", pady=5)

        self.preco_compra_header = ctk.CTkLabel(self.frame_header, text="P. Compra", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.preco_compra_header.grid(row=0, column=6, sticky="nsew", pady=5)

        self.preco_venda_header = ctk.CTkLabel(self.frame_header, text="P. Venda", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.preco_venda_header.grid(row=0, column=7, sticky="nsew", pady=5)

        self.status_header = ctk.CTkLabel(self.frame_header, text="Status", font=("Arial", 12, "bold"), text_color=self.cor_texto_secundario, anchor="center")
        self.status_header.grid(row=0, column=8, sticky="nsew", pady=5)

        self.botao_adicionar = ctk.CTkButton(self.frame_header, text="+ Adicionar", width=120, height=30, font=("Arial", 12, "bold"), fg_color=self.cor_primaria, command=self.tela_cadastro)

    def criar_linha_produto(self, produto, aceitavel, razoavel, baixa):
        produto_id, nome, descricao, categoria, quantidade, preco_compra, preco_venda, _ = produto

        self.card = ctk.CTkFrame(self.container_produtos, height=40, fg_color=self.cor_cards, border_width=1, border_color=self.cor_bordas, corner_radius=6)
        self.card.pack(fill="x", pady=(0, 5))
        self.card.pack_propagate(False)

        self.criar_colunas_tabela(self.card)

        if quantidade > razoavel:
            imagem_aviso = self.circulo_verde
        elif quantidade > baixa:
            imagem_aviso = self.circulo_amarelo
        else:
            imagem_aviso = self.circulo_vermelho

        self.aviso_produto = ctk.CTkLabel(self.card, text="", image=imagem_aviso)
        self.aviso_produto.grid(row=0, column=0, sticky="nsew", pady=5)

        self.id_produto = ctk.CTkLabel(self.card, text=f"#{produto_id}", text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        self.id_produto.grid(row=0, column=1, sticky="nsew", pady=10)

        self.nome_produto = ctk.CTkLabel(self.card, text=nome, text_color=self.cor_texto_secundario, font=("Arial", 12, "bold"), anchor="center")
        self.nome_produto.grid(row=0, column=2, sticky="nsew", pady=5)

        self.categoria_produto = ctk.CTkLabel(self.card, text=categoria, text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        self.categoria_produto.grid(row=0, column=3, sticky="nsew", pady=5)

        self.descricao_produto = ctk.CTkLabel(self.card, text=str(descricao), text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        self.descricao_produto.grid(row=0, column=4, sticky="nsew", pady=5)

        self.quantidade_produto = ctk.CTkLabel(self.card, text=str(quantidade), text_color=self.cor_texto_secundario, font=("Arial", 12, "bold"), anchor="center")
        self.quantidade_produto.grid(row=0, column=5, sticky="nsew", pady=5)

        self.preco_compra_produto = ctk.CTkLabel(self.card, text=f"R$ {preco_compra:.2f}", text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        self.preco_compra_produto.grid(row=0, column=6, sticky="nsew", pady=5)

        self.preco_venda_produto = ctk.CTkLabel(self.card, text=f"R$ {preco_venda:.2f}", text_color=self.cor_texto_secundario, font=("Arial", 12), anchor="center")
        self.preco_venda_produto.grid(row=0, column=7, sticky="nsew", pady=5)

        self.status_produto = ctk.CTkLabel(self.card, text="Ativo", text_color=self.cor_texto_secundario, font=("Arial", 12, "bold"), anchor="center")
        self.status_produto.grid(row=0, column=8, sticky="nsew", pady=5)

        if quantidade <= 0:
            self.status_produto.configure(text="Indisponível", text_color="#DC2626")

        if self.cargo_gerente:
            self.frame_acoes = ctk.CTkFrame(self.card, fg_color="transparent")
            self.frame_acoes.grid(row=0, column=9)

            self.botao_editar = ctk.CTkButton(self.frame_acoes, text="", image=self.imagem_editar, width=35, height=35, corner_radius=6, fg_color=self.cor_primaria, hover_color="#00477F", command=lambda id_produto=produto_id: self.tela_edicao(id_produto))
            self.botao_editar.pack(side="left", padx=5)

            self.botao_excluir = ctk.CTkButton(self.frame_acoes, text="", image=self.imagem_lixeira, width=35, height=35, corner_radius=6, fg_color="#DC2626", hover_color="#B91C1C", command=lambda id_produto=produto_id: self.tela_excluir(id_produto))
            self.botao_excluir.pack(side="left", padx=5)

    #Configurações de Quantidade

    def tela_configuracao(self):
        if hasattr(self, "frame_configurar") and self.frame_configurar.winfo_exists():
            self.frame_configurar.destroy()

        self.frame_configurar = ctk.CTkFrame(self, fg_color=self.cor_cards, height=360, width=430, corner_radius=5)
        self.frame_configurar.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_configurar.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_configurar)

        self.container_fechar = ctk.CTkFrame(self.frame_configurar, fg_color=self.cor_primaria, height=30, corner_radius=5)
        self.container_fechar.pack(side="top", fill="x", pady=0)

        self.botao_fechar = ctk.CTkButton(self.container_fechar, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_configurar.place_forget)
        self.botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        self.texto_principal = ctk.CTkLabel(self.container_fechar, text="Configurações", font=("Arial", 14, "bold"), text_color=self.cor_bordas)
        self.texto_principal.pack(padx=(8, 10), side="left", pady=3)

        self.texto_secundario = ctk.CTkLabel(self.frame_configurar, text="Configure os avisos do seu estoque", font=("Arial", 14, "bold"), text_color=self.cor_texto_secundario)
        self.texto_secundario.pack(pady=20)

        self.container1 = ctk.CTkFrame(self.frame_configurar, fg_color=self.cor_fundo, width=400, height=42)
        self.container1.pack(pady=(0, 15))
        self.container1.pack_propagate(False)

        self.img1 = ctk.CTkLabel(self.container1, text="", image=self.circulo_verde)
        self.img1.pack(side="left", padx=(15, 0))

        self.texto_qtd1 = ctk.CTkLabel(self.container1, text="Quantidade Aceitável", font=("Arial", 14), text_color=self.cor_texto_secundario)
        self.texto_qtd1.pack(side="left", padx=15)

        self.input1 = ctk.CTkEntry(self.container1, placeholder_text="Ex: 100", width=180)
        self.input1.pack(side="right", pady=7, padx=7)

        self.container2 = ctk.CTkFrame(self.frame_configurar, fg_color=self.cor_fundo, width=400, height=42)
        self.container2.pack(pady=(0, 15))
        self.container2.pack_propagate(False)

        self.img2 = ctk.CTkLabel(self.container2, text="", image=self.circulo_amarelo)
        self.img2.pack(side="left", padx=(15, 0))

        self.texto_qtd2 = ctk.CTkLabel(self.container2, text="Quantidade Razoável", font=("Arial", 14), text_color=self.cor_texto_secundario)
        self.texto_qtd2.pack(side="left", padx=15)

        self.input2 = ctk.CTkEntry(self.container2, placeholder_text="Ex: 50", width=180)
        self.input2.pack(side="right", pady=7, padx=7)

        self.container3 = ctk.CTkFrame(self.frame_configurar, fg_color=self.cor_fundo, width=400, height=42)
        self.container3.pack(pady=(0, 15))
        self.container3.pack_propagate(False)

        self.img3 = ctk.CTkLabel(self.container3, text="", image=self.circulo_vermelho)
        self.img3.pack(side="left", padx=(15, 0))

        self.texto_qtd3 = ctk.CTkLabel(self.container3, text="Quantidade Mínima", font=("Arial", 14), text_color=self.cor_texto_secundario)
        self.texto_qtd3.pack(side="left", padx=15)

        self.input3 = ctk.CTkEntry(self.container3, placeholder_text="Ex: 10", width=180)
        self.input3.pack(side="right", pady=7, padx=7)

        self.label_mensagem = ctk.CTkLabel(self.frame_configurar, text="", font=("Arial", 14))
        self.label_mensagem.pack(pady=(0, 10))

        self.botao_confirmacao = ctk.CTkButton(self.frame_configurar, fg_color=self.cor_primaria, corner_radius=5, text="Confirmar", height=30, width=203, command=self.configurar_quantidades)
        self.botao_confirmacao.pack(side="left", anchor="sw", padx=(8, 0), pady=8)

        self.botao_cancelar = ctk.CTkButton(self.frame_configurar, fg_color="transparent", corner_radius=5, border_width=2, border_color=self.cor_primaria, text="Cancelar", text_color=self.cor_primaria, height=30, hover_color=self.cor_fundo, width=203, command=self.frame_configurar.place_forget)
        self.botao_cancelar.pack(side="right", anchor="sw", padx=(0, 8), pady=8)

        aceitavel, razoavel, baixa = self.carregar_configuracao_quantidade()
        self.input1.insert(0, str(aceitavel))
        self.input2.insert(0, str(razoavel))
        self.input3.insert(0, str(baixa))

    def configurar_quantidades(self):
        aceitavel = self.input1.get()
        razoavel = self.input2.get()
        baixa = self.input3.get()

        if len(aceitavel) == 0 or len(razoavel) == 0 or len(baixa) == 0:
            self.label_mensagem.configure(text="Preencha todos os campos.", text_color="red")
            self.label_mensagem.after(3000, lambda: self.label_mensagem.configure(text="", text_color="red"))
            return

        elif len(aceitavel) > 6 or len(razoavel) > 6 or len(baixa) > 6:
            self.label_mensagem.configure(text="Os campos devem ter no máximo 6 caracteres.", text_color="red")
            self.label_mensagem.after(3000, lambda: self.label_mensagem.configure(text="", text_color="red"))
            return

        elif not aceitavel.isdigit() or not razoavel.isdigit() or not baixa.isdigit():
            self.label_mensagem.configure(text="Os campos devem ser números.", text_color="red")
            self.label_mensagem.after(3000, lambda: self.label_mensagem.configure(text="", text_color="red"))
            return

        if int(aceitavel) <= int(razoavel) or int(aceitavel) <= int(baixa):
            self.label_mensagem.configure(text="A quantidade aceitável deve ser maior que as outras.", text_color="red")
            self.label_mensagem.after(3000, lambda: self.label_mensagem.configure(text="", text_color="red"))
            self.destacar_erro(self.input1)
            return

        elif int(razoavel) <= int(baixa):
            self.label_mensagem.configure(text="A quantidade razoável deve ser maior que a quantidade mínima.", text_color="red")
            self.label_mensagem.after(3000, lambda: self.label_mensagem.configure(text="", text_color="red"))
            self.destacar_erro(self.input2)
            return

        else:
            self.salvar_configuracao(aceitavel, razoavel, baixa)
            self.frame_configurar.place_forget()
            self.atualizar_lista_produtos()

    def salvar_configuracao(self, aceitavel, razoavel, baixa):
        configuracoes = {"configurado": True, "aceitavel": aceitavel, "razoavel": razoavel, "baixa": baixa}
        with open("configuracao.json", "w", encoding="utf-8") as nova_configuracao:
            json.dump(configuracoes, nova_configuracao, indent=4)

    #Cadastro de Produtos

    def tela_cadastro(self):
        if hasattr(self, "frame_cadastro") and self.frame_cadastro.winfo_exists():
            self.frame_cadastro.destroy()

        self.frame_cadastro = ctk.CTkFrame(self, fg_color=self.cor_cards, height=180, width=1245, corner_radius=5)
        self.frame_cadastro.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_cadastro.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_cadastro)

        self.container_topo = ctk.CTkFrame(self.frame_cadastro, fg_color=self.cor_primaria, height=20, corner_radius=0)
        self.container_topo.pack(fill="x", anchor="n")

        self.label_cadastro = ctk.CTkLabel(self.container_topo, text="Cadastro de Produto", font=("Arial", 16, "bold"), text_color=self.cor_bordas)
        self.label_cadastro.pack(pady=5, padx=10, side="left")

        self.botao_fechar = ctk.CTkButton(self.container_topo, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_cadastro.place_forget)
        self.botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        self.container_inputs = ctk.CTkFrame(self.frame_cadastro, fg_color="transparent")
        self.container_inputs.pack(anchor="n", side="top")

        self.container_nome = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_nome.pack(pady=5, padx=(5, 0), side="left")

        self.label_nome = ctk.CTkLabel(self.container_nome, text="Nome:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_nome.pack(pady=3, anchor="w")

        self.cadastro_nome = ctk.CTkEntry(self.container_nome, placeholder_text="Nome", width=200)
        self.cadastro_nome.pack()

        self.container_categoria = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_categoria.pack(pady=5, padx=(5, 0), side="left")

        self.label_categoria = ctk.CTkLabel(self.container_categoria, text="Categoria:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_categoria.pack(pady=3, anchor="w")

        self.cadastro_categoria = ctk.CTkEntry(self.container_categoria, placeholder_text="Categoria", width=200)
        self.cadastro_categoria.pack()

        self.container_descricao = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_descricao.pack(pady=5, padx=(5, 0), side="left")

        self.label_descricao = ctk.CTkLabel(self.container_descricao, text="Descrição:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_descricao.pack(pady=3, anchor="w")

        self.cadastro_descricao = ctk.CTkEntry(self.container_descricao, placeholder_text="Descrição", width=200)
        self.cadastro_descricao.pack()

        self.container_quantidade = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_quantidade.pack(pady=5, padx=(5, 0), side="left")

        self.label_quantidade = ctk.CTkLabel(self.container_quantidade, text="Quantidade:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_quantidade.pack(pady=3, anchor="w")

        self.cadastro_quantidade = ctk.CTkEntry(self.container_quantidade, placeholder_text="Quantidade", width=200)
        self.cadastro_quantidade.pack()

        self.container_preco_compra = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_preco_compra.pack(pady=5, padx=(5, 0), side="left")

        self.label_preco_compra = ctk.CTkLabel(self.container_preco_compra, text="Preço de Compra:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_preco_compra.pack(pady=3, anchor="w")

        self.cadastro_preco_compra = ctk.CTkEntry(self.container_preco_compra, placeholder_text="Preço de Compra", width=200)
        self.cadastro_preco_compra.pack()

        self.container_preco_venda = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_preco_venda.pack(pady=5, padx=5, side="left")

        self.label_preco_venda = ctk.CTkLabel(self.container_preco_venda, text="Preço de Venda:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_preco_venda.pack(pady=3, anchor="w")

        self.cadastro_preco_venda = ctk.CTkEntry(self.container_preco_venda, placeholder_text="Preço de Venda", width=200)
        self.cadastro_preco_venda.pack()

        self.mensagem_sucesso = ctk.CTkLabel(self.frame_cadastro, text="", font=("Arial", 12), text_color="#16A34A")
        self.mensagem_sucesso.pack(pady=2)

        self.botao_cadastro = ctk.CTkButton(self.frame_cadastro, text="Cadastrar", width=615, height=30, font=("Arial", 12, "bold"), fg_color=self.cor_primaria, command=self.cadastrar_produto)
        self.botao_cadastro.pack(pady=(0, 5), padx=5, side="left", anchor="sw")

        self.botao_cancelar = ctk.CTkButton(self.frame_cadastro, text="Cancelar", width=615, height=30, font=("Arial", 12, "bold"), fg_color="transparent", border_width=2, border_color=self.cor_primaria, text_color=self.cor_primaria, hover_color=self.cor_fundo, command=self.frame_cadastro.place_forget)
        self.botao_cancelar.pack(pady=(0, 5), padx=(0, 5), side="right", anchor="se")

    def cadastrar_produto(self):
        nome = self.cadastro_nome.get()
        categoria = self.cadastro_categoria.get()
        descricao = self.cadastro_descricao.get()
        quantidade = self.cadastro_quantidade.get()
        preco_compra = self.cadastro_preco_compra.get()
        preco_venda = self.cadastro_preco_venda.get()

        valido, mensagem, atributos = self.validar_produto(nome, categoria, descricao, quantidade, preco_compra, preco_venda)

        if not valido:
            self.mensagem_sucesso.configure(text=mensagem, text_color="red")
            self.mensagem_sucesso.after(3000, lambda: self.mensagem_sucesso.configure(text="", text_color="red"))
            if atributos:
                campo = getattr(self, f"cadastro_{atributos}")
                self.destacar_erro(campo)
            return

        produtos.adicionar_produto(nome, categoria, descricao, quantidade, self.preco_float(preco_compra), self.preco_float(preco_venda))
        self.frame_cadastro.place_forget()
        self.atualizar_lista_produtos()

    #Edição de Produtos

    def tela_edicao(self, id_produto):
        if hasattr(self, "frame_editar") and self.frame_editar.winfo_exists():
            self.frame_editar.destroy()

        self.frame_editar = ctk.CTkFrame(self, fg_color=self.cor_cards, height=180, width=1245, corner_radius=5)
        self.frame_editar.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_editar.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_editar)

        self.container_topo = ctk.CTkFrame(self.frame_editar, fg_color=self.cor_primaria, height=20, corner_radius=0)
        self.container_topo.pack(fill="x", anchor="n")

        self.label_editar = ctk.CTkLabel(self.container_topo, text="Editar Produto", font=("Arial", 16, "bold"), text_color=self.cor_bordas)
        self.label_editar.pack(pady=5, padx=10, side="left")

        self.botao_fechar = ctk.CTkButton(self.container_topo, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_editar.place_forget)
        self.botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        self.container_inputs = ctk.CTkFrame(self.frame_editar, fg_color="transparent")
        self.container_inputs.pack(anchor="n", side="top")

        self.container_nome = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_nome.pack(pady=5, padx=(5, 0), side="left")

        self.label_nome = ctk.CTkLabel(self.container_nome, text="Nome:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_nome.pack(pady=3, anchor="w")

        self.editar_nome = ctk.CTkEntry(self.container_nome, placeholder_text="Nome", width=200)
        self.editar_nome.pack()

        self.container_categoria = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_categoria.pack(pady=5, padx=(5, 0), side="left")

        self.label_categoria = ctk.CTkLabel(self.container_categoria, text="Categoria:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_categoria.pack(pady=3, anchor="w")

        self.editar_categoria = ctk.CTkEntry(self.container_categoria, placeholder_text="Categoria", width=200)
        self.editar_categoria.pack()

        self.container_descricao = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_descricao.pack(pady=5, padx=(5, 0), side="left")

        self.label_descricao = ctk.CTkLabel(self.container_descricao, text="Descrição:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_descricao.pack(pady=3, anchor="w")

        self.editar_descricao = ctk.CTkEntry(self.container_descricao, placeholder_text="Descrição", width=200)
        self.editar_descricao.pack()

        self.container_quantidade = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_quantidade.pack(pady=5, padx=(5, 0), side="left")

        self.label_quantidade = ctk.CTkLabel(self.container_quantidade, text="Quantidade:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_quantidade.pack(pady=3, anchor="w")

        self.editar_quantidade = ctk.CTkEntry(self.container_quantidade, placeholder_text="Quantidade", width=200)
        self.editar_quantidade.pack()

        self.container_preco_compra = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_preco_compra.pack(pady=5, padx=(5, 0), side="left")

        self.label_preco_compra = ctk.CTkLabel(self.container_preco_compra, text="Preço de Compra:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_preco_compra.pack(pady=3, anchor="w")

        self.editar_preco_compra = ctk.CTkEntry(self.container_preco_compra, placeholder_text="Preço de Compra", width=200)
        self.editar_preco_compra.pack()

        self.container_preco_venda = ctk.CTkFrame(self.container_inputs, fg_color="transparent")
        self.container_preco_venda.pack(pady=5, padx=5, side="left")

        self.label_preco_venda = ctk.CTkLabel(self.container_preco_venda, text="Preço de Venda:", font=("Arial", 12, "bold"), text_color=self.cor_texto_principal)
        self.label_preco_venda.pack(pady=3, anchor="w")

        self.editar_preco_venda = ctk.CTkEntry(self.container_preco_venda, placeholder_text="Preço de Venda", width=200)
        self.editar_preco_venda.pack()

        produto = produtos.buscar_produto(id_produto)
        if produto:
            _, nome, descricao, categoria, quantidade, preco_compra, preco_venda, _ = produto

            self.editar_nome.insert(0, nome)
            self.editar_categoria.insert(0, categoria)
            self.editar_descricao.insert(0, str(descricao))
            self.editar_quantidade.insert(0, str(quantidade))
            self.editar_preco_compra.insert(0, f"{preco_compra:.2f}")
            self.editar_preco_venda.insert(0, f"{preco_venda:.2f}")

        self.mensagem_sucesso = ctk.CTkLabel(self.frame_editar, text="", font=("Arial", 12), text_color="#16A34A")
        self.mensagem_sucesso.pack(pady=2)

        self.botao_editar = ctk.CTkButton(self.frame_editar, text="Editar", width=615, height=30, font=("Arial", 12, "bold"), fg_color=self.cor_primaria, command=lambda: self.editar_produto(id_produto))
        self.botao_editar.pack(pady=(0, 5), padx=5, side="left", anchor="sw")

        self.botao_cancelar = ctk.CTkButton(self.frame_editar, text="Cancelar", width=615, height=30, font=("Arial", 12, "bold"), fg_color="transparent", border_width=2, border_color=self.cor_primaria, text_color=self.cor_primaria, hover_color=self.cor_fundo, command=self.frame_editar.place_forget)
        self.botao_cancelar.pack(pady=(0, 5), padx=(0, 5), side="right", anchor="se")

    def editar_produto(self, id_produto):
        nome = self.editar_nome.get()
        categoria = self.editar_categoria.get()
        descricao = self.editar_descricao.get()
        quantidade = self.editar_quantidade.get()
        preco_compra = self.editar_preco_compra.get()
        preco_venda = self.editar_preco_venda.get()

        valido, mensagem, atributos = self.validar_produto(nome, categoria, descricao, quantidade, preco_compra, preco_venda)

        if not valido:
            self.mensagem_sucesso.configure(text=mensagem, text_color="red")
            self.mensagem_sucesso.after(3000, lambda: self.mensagem_sucesso.configure(text="", text_color="red"))
            if atributos:
                campo = getattr(self, f"editar_{atributos}")
                self.destacar_erro(campo)
            return

        produtos.editar_produto(id_produto, nome, categoria, descricao, quantidade, self.preco_float(preco_compra), self.preco_float(preco_venda))
        self.frame_editar.place_forget()
        self.atualizar_lista_produtos()

    #Exclusão de Produtos

    def tela_excluir(self, id_produto):
        if hasattr(self, "frame_excluir") and self.frame_excluir.winfo_exists():
            self.frame_excluir.destroy()

        self.frame_excluir = ctk.CTkFrame(self, fg_color=self.cor_cards, height=150, width=300, corner_radius=5)
        self.frame_excluir.place(rely=0.5, relx=0.5, anchor="center")
        self.frame_excluir.pack_propagate(False)
        self.controller.mostrar_painel(self.frame_excluir)

        self.container_fechar = ctk.CTkFrame(self.frame_excluir, fg_color=self.cor_primaria, height=30, corner_radius=5)
        self.container_fechar.pack(side="top", fill="x", pady=0)

        self.botao_fechar = ctk.CTkButton(self.container_fechar, text="", image=self.imagem_x, fg_color="transparent", width=15, command=self.frame_excluir.place_forget)
        self.botao_fechar.pack(side="right", padx=(10, 5), pady=3)

        self.texto_principal = ctk.CTkLabel(self.container_fechar, text="Excluir produto", font=("Arial", 14, "bold"), text_color=self.cor_bordas)
        self.texto_principal.pack(padx=(8, 10), side="left", pady=3)

        self.texto_secundario = ctk.CTkLabel(self.frame_excluir, text="Tem certeza que deseja excluir o produto?", font=("Arial", 14), text_color=self.cor_texto_secundario)
        self.texto_secundario.pack(pady=10)

        self.botao_excluir = ctk.CTkButton(self.frame_excluir, fg_color=self.cor_primaria, corner_radius=5, text="Confirmar", height=30, command=lambda: self.excluir(id_produto))
        self.botao_excluir.pack(side="left", anchor="sw", padx=(8, 8), pady=8)

        self.botao_cancelar = ctk.CTkButton(self.frame_excluir, fg_color="transparent", corner_radius=5, border_width=2, border_color=self.cor_primaria, text="Cancelar", text_color=self.cor_primaria, height=30, hover_color=self.cor_fundo, command=self.frame_excluir.place_forget)
        self.botao_cancelar.pack(side="left", anchor="se", padx=(0, 8), pady=8)

    def excluir(self, id_produto):
        produtos.excluir_produto(id_produto)
        self.frame_excluir.place_forget()
        self.atualizar_lista_produtos()

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

    #Menus

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

        self.botao_estoque = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Estoque", font=("Arial", 15, "bold"), fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_caixa_menu_bold)
        self.botao_estoque.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.botao_historico = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Hist. Vendas", fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_grafico, command=self.abrir_historico)
        self.botao_historico.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.container_destaques = ctk.CTkFrame(self, fg_color="transparent", height=2)
        self.container_destaques.pack(fill="x", pady=0, anchor="n")

        self.destaque_vendas = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_fundo, height=3)
        self.destaque_vendas.pack(side="left", padx=0, pady=0, expand=True, fill="x")

        self.destaque_estoque = ctk.CTkFrame(self.container_destaques, fg_color=self.cor_primaria, height=3)
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

    #Funções/Carregamento

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

    #Mudança de Telas

    def abrir_vendas(self):
        self.controller.abrir_vendas(self.usuario, self.cargo)

    def abrir_historico(self):
        self.controller.abrir_historico(self.usuario, self.cargo)