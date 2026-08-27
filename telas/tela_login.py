import customtkinter as ctk
from PIL import Image
import json
from funcoes.login import funcao_login, funcao_cadastro

class TelaAutenticacao(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.cor_fundo = "#F1F5F9"
        self.cor_cards = "#FFFFFF"
        self.cor_primaria = "#2563EB"
        self.cor_texto_principal = "#0F172A"
        self.cor_texto_secundario = "#475569"
        self.cor_bordas = "#E2E8F0"

        self.configure(fg_color=self.cor_fundo)

        self.carregar_imagens()
        self.criar_tela_login()
        self.criar_tela_cadastro()
        self.mostrar_login()

    def carregar_imagens(self):
        try:
            self.imagem_engrenagem = ctk.CTkImage(Image.open("imagens/engrenagem.png"), size=(20, 20))
            self.imagem_caixa = ctk.CTkImage(Image.open("imagens/caixa.png"), size=(60, 60))
            self.imagem_usuario = ctk.CTkImage(Image.open("imagens/usuario.png"), size=(15, 15))
            self.imagem_cadeado = ctk.CTkImage(Image.open("imagens/cadeado.png"), size=(15, 15))
        except (FileNotFoundError, Exception):
            self.imagem_engrenagem = None
            self.imagem_caixa = None
            self.imagem_usuario = None
            self.imagem_cadeado = None

    def mostrar_senha(self, checkbox, campo_senha):
        if checkbox.get() == 1:
            campo_senha.configure(show="")
        else:
            campo_senha.configure(show="*")

    def criar_tela_login(self):
        self.painel_login = ctk.CTkFrame(self, fg_color=self.cor_cards, corner_radius=30, border_width=3, border_color=self.cor_bordas, width=470, height=610)
        self.painel_login.pack_propagate(False)

        self.login_imagem_logo = ctk.CTkLabel(self.painel_login, image=self.imagem_caixa, text="")
        self.login_imagem_logo.pack(pady=(40, 20))

        self.login_texto_inicial = ctk.CTkLabel(self.painel_login, text="Bem-vindo ao StockDesk!", font=("Arial", 24, "bold"), text_color=self.cor_texto_principal)
        self.login_texto_inicial.pack(pady=(0, 25))

        self.login_texto_usuario = ctk.CTkLabel(self.painel_login, text=" Usuário", font=("Arial", 14, "bold"), text_color=self.cor_texto_secundario, image=self.imagem_usuario, compound="left")
        self.login_texto_usuario.pack(anchor="w", padx=40, pady=(0, 5))

        self.login_usuario_input = ctk.CTkEntry(self.painel_login, placeholder_text="Ex: User", width=400, height=40, corner_radius=8)
        self.login_usuario_input.pack(pady=(0, 15))

        self.login_texto_senha = ctk.CTkLabel(self.painel_login, text=" Senha", font=("Arial", 14, "bold"), text_color=self.cor_texto_secundario, image=self.imagem_cadeado, compound="left")
        self.login_texto_senha.pack(anchor="w", padx=40, pady=(0, 5))

        self.login_senha_input = ctk.CTkEntry(self.painel_login, placeholder_text="********", show="*", width=400, height=40, corner_radius=8)
        self.login_senha_input.pack(pady=(0, 8))

        self.login_ver_senha = ctk.CTkCheckBox(self.painel_login, text="Mostrar senha", font=("Arial", 13), text_color=self.cor_texto_secundario, checkbox_width=16, checkbox_height=16, command=lambda: self.mostrar_senha(self.login_ver_senha, self.login_senha_input))
        self.login_ver_senha.pack(anchor="w", padx=40, pady=(0, 80))

        self.login_botao_login = ctk.CTkButton(self.painel_login, text="Entrar", text_color="#FFFFFF", width=400, height=45, fg_color=self.cor_primaria, font=("Arial", 15, "bold"), corner_radius=8, command=self.fazer_login)
        self.login_botao_login.pack(pady=(0, 10))

        self.login_botao_cadastro = ctk.CTkButton(self.painel_login, text="Criar Conta", text_color=self.cor_primaria, width=400, height=45, fg_color="transparent", hover_color="#E2E8F0", font=("Arial", 15, "bold"), corner_radius=8, command=self.mostrar_cadastro)
        self.login_botao_cadastro.pack(pady=(0, 10))

        self.mensagem_login = ctk.CTkLabel(self.painel_login, text="", font=("Arial", 12), text_color="red")
        self.mensagem_login.pack(pady=(0, 10))

    def criar_tela_cadastro(self):
        self.painel_cadastro = ctk.CTkFrame(self, fg_color=self.cor_cards, corner_radius=30, border_width=3, border_color=self.cor_bordas, width=470, height=610)
        self.painel_cadastro.pack_propagate(False)

        self.cadastro_imagem_logo = ctk.CTkLabel(self.painel_cadastro, image=self.imagem_caixa, text="")
        self.cadastro_imagem_logo.pack(pady=(25, 15))

        self.cadastro_texto_inicial = ctk.CTkLabel(self.painel_cadastro, text="Criar Nova Conta", font=("Arial", 24, "bold"), text_color=self.cor_texto_principal)
        self.cadastro_texto_inicial.pack(pady=(0, 15))

        self.cadastro_texto_usuario = ctk.CTkLabel(self.painel_cadastro, text=" Crie um usuário", font=("Arial", 14, "bold"), text_color=self.cor_texto_secundario, image=self.imagem_usuario, compound="left")
        self.cadastro_texto_usuario.pack(anchor="w", padx=40, pady=(0, 5))

        self.cadastro_usuario_input = ctk.CTkEntry(self.painel_cadastro, placeholder_text="Ex: User", width=400, height=40, corner_radius=8)
        self.cadastro_usuario_input.pack(pady=(0, 15))

        self.cadastro_texto_senha = ctk.CTkLabel(self.painel_cadastro, text=" Crie uma Senha", font=("Arial", 14, "bold"), text_color=self.cor_texto_secundario, image=self.imagem_cadeado, compound="left")
        self.cadastro_texto_senha.pack(anchor="w", padx=40, pady=(0, 5))

        self.cadastro_senha_input = ctk.CTkEntry(self.painel_cadastro, placeholder_text="********", show="*", width=400, height=40, corner_radius=8)
        self.cadastro_senha_input.pack(pady=(0, 5))

        self.cadastro_ver_senha = ctk.CTkCheckBox(self.painel_cadastro, text="Mostrar senha", font=("Arial", 13), text_color=self.cor_texto_secundario, checkbox_width=16, checkbox_height=16, command=lambda: self.mostrar_senha(self.cadastro_ver_senha, self.cadastro_senha_input))
        self.cadastro_ver_senha.pack(anchor="w", padx=40, pady=(0, 15))

        self.cadastro_texto_cargo = ctk.CTkLabel(self.painel_cadastro, text="Selecione o Cargo", font=("Arial", 14, "bold"), text_color=self.cor_texto_secundario)
        self.cadastro_texto_cargo.pack(anchor="w", padx=40, pady=(0, 5))

        self.cadastro_cargo_input = ctk.CTkOptionMenu(self.painel_cadastro, values=["Vendedor", "Gerente"], width=400, height=38, corner_radius=8, fg_color=self.cor_fundo, button_color=self.cor_primaria, text_color=self.cor_texto_principal, dropdown_hover_color=self.cor_bordas)
        self.cadastro_cargo_input.pack(pady=(0, 35))

        self.cadastro_botao_cadastrar = ctk.CTkButton(self.painel_cadastro, text="Cadastrar", text_color="#FFFFFF", width=400, height=45, fg_color=self.cor_primaria, font=("Arial", 15, "bold"), corner_radius=8, command=self.fazer_cadastro)
        self.cadastro_botao_cadastrar.pack(pady=(0, 10))

        self.cadastro_botao_voltar = ctk.CTkButton(self.painel_cadastro, text="Login", text_color=self.cor_primaria, width=400, height=45, fg_color="transparent", hover_color="#E2E8F0", font=("Arial", 15, "bold"), corner_radius=8, command=self.mostrar_login)
        self.cadastro_botao_voltar.pack(pady=(0, 7))

        self.mensagem_cadastro = ctk.CTkLabel(self.painel_cadastro, text="", font=("Arial", 12), text_color="red")
        self.mensagem_cadastro.pack(pady=(0, 10))

    def mostrar_login(self):
        self.painel_cadastro.place_forget()
        self.painel_login.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_cadastro(self):
        self.painel_login.place_forget()
        self.painel_cadastro.place(relx=0.5, rely=0.5, anchor="center")

    def fazer_login(self):
        usuario = self.login_usuario_input.get()
        senha = self.login_senha_input.get()

        sucesso, resultado = funcao_login(usuario, senha)

        if sucesso:
            cargo = resultado
            self.mensagem_login.configure(text="Login bem sucedido!", text_color="green")
            self.mensagem_login.after(5000, lambda: self.mensagem_login.configure(text="", text_color="red"))
            self.login_usuario_input.delete(0, "end")
            self.login_senha_input.delete(0, "end")
            self.after(1000, lambda: self.controller.abrir_vendas(cargo, usuario))
            self.salvar_sessao(usuario, cargo)
        else:
            self.mensagem_login.configure(text=resultado, text_color="red")
            self.mensagem_login.after(5000, lambda: self.mensagem_login.configure(text="", text_color="red"))

    def fazer_cadastro(self):
        usuario = self.cadastro_usuario_input.get()
        senha = self.cadastro_senha_input.get()
        cargo = self.cadastro_cargo_input.get()

        if len(str(senha)) < 4:
            self.mensagem_cadastro.configure(text="Erro: A senha deve ter pelo menos 4 caracteres", text_color="red")
            self.mensagem_cadastro.after(5000, lambda: self.mensagem_cadastro.configure(text="", text_color="red"))
            return
        elif len(str(senha)) > 10:
            self.mensagem_cadastro.configure(text="Erro: A senha deve ter no máximo 10 caracteres", text_color="red")
            self.mensagem_cadastro.after(5000, lambda: self.mensagem_cadastro.configure(text="", text_color="red"))
            return
        elif len(str(usuario)) < 4:
            self.mensagem_cadastro.configure(text="Erro: O nome de usuário deve ter no mínimo 4 caracteres", text_color="red")
            self.mensagem_cadastro.after(5000, lambda: self.mensagem_cadastro.configure(text="", text_color="red"))
            return
        elif len(str(usuario)) > 20:
            self.mensagem_cadastro.configure(text="Erro: O nome de usuário deve ter no máximo 20 caracteres", text_color="red")
            self.mensagem_cadastro.after(5000, lambda: self.mensagem_cadastro.configure(text="", text_color="red"))
            return

        sucesso, resultado = funcao_cadastro(usuario, senha, cargo)

        if sucesso:
            cargo = resultado
            print(f"Conta criada com sucesso! Usuário: {usuario}, Senha: {senha}, Cargo: {cargo}")
            self.mensagem_cadastro.configure(text="Conta criada com sucesso!", text_color="green")
            self.mensagem_cadastro.after(5000, lambda: self.mensagem_cadastro.configure(text="", text_color="red"))
            self.cadastro_usuario_input.delete(0, "end")
            self.cadastro_senha_input.delete(0, "end")
            self.after(1000, lambda: self.controller.abrir_vendas(cargo, usuario))
            self.salvar_sessao(usuario, cargo)
        else:
            self.mensagem_cadastro.configure(text=resultado, text_color="red")
            self.mensagem_cadastro.after(5000, lambda: self.mensagem_cadastro.configure(text="", text_color="red"))

    def salvar_sessao(self, usuario, cargo):
        dados_sessao = {"logado": True, "usuario": usuario, "cargo": cargo}
        with open("sessao.json", "w", encoding="utf-8") as f:
            json.dump(dados_sessao, f, indent=4)

if __name__ == "__main__":
    app = TelaAutenticacao()
    app.mainloop()