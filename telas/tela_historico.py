import customtkinter as ctk
from PIL import Image

import customtkinter as ctk
from PIL import Image

class TelaHistorico(ctk.CTkFrame):
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

        self.botao_estoque = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Estoque", fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_caixa_menu_bold, command=self.abrir_estoque)
        self.botao_estoque.pack(side="left", padx=0, pady=0, expand=True, fill="both")

        self.botao_historico = ctk.CTkButton(self.container_botoes, hover_color=self.cor_texto_secundario, text="Hist. Vendas", fg_color=self.cor_secundaria, height=35, corner_radius=0, image=self.imagem_grafico, font=("Arial", 15, "bold"))
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

    def abrir_estoque(self):
        self.controller.abrir_estoque(self.usuario, self.cargo)
    def abrir_vendas(self):
        self.controller.abrir_vendas(self.usuario, self.cargo)
