import customtkinter as ctk
from PIL import Image
from funcoes.login import funcaologin, funcaocadastro

class TelaAutenticacao(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.cor_fundo = "#F1F5F9"
        self.cor_cards = "#FFFFFF"
        self.cor_primaria = "#2563EB"
        self.cor_textoprincipal = "#0F172A"
        self.cor_textosecundario = "#475569"
        self.cor_bordas = "#E2E8F0"

        self.configure(fg_color=self.cor_fundo)

        self.carregar_imagens()
        self.criar_tela_login()
        self.criar_tela_cadastro()
        self.mostrar_login()

    def carregar_imagens(self):
        try:
            self.imagem_engrenagem = ctk.CTkImage(Image.open("imagens/engrenagem.png"), size=(20, 20))
            self.imagemcaixa = ctk.CTkImage(Image.open("imagens/caixa.png"), size=(60, 60))
            self.imagemusuario = ctk.CTkImage(Image.open("imagens/usuario.png"), size=(15, 15))
            self.imagemcadeado = ctk.CTkImage(Image.open("imagens/cadeado.png"), size=(15, 15))
        except (FileNotFoundError, Exception):
            self.imagem_engrenagem = None
            self.imagemcaixa = None
            self.imagemusuario = None
            self.imagemcadeado = None

    def mostrar_senha(self, checkbox, campo_senha):
        if checkbox.get() == 1:
            campo_senha.configure(show="")
        else:
            campo_senha.configure(show="*")

    def criar_tela_login(self):
        self.painellogin = ctk.CTkFrame(self, fg_color=self.cor_cards, corner_radius=30, border_width=3, border_color=self.cor_bordas, width=470, height=610)
        self.painellogin.pack_propagate(False)

        self.login_labelimagem = ctk.CTkLabel(self.painellogin, image=self.imagemcaixa, text="")
        self.login_labelimagem.pack(pady=(40, 20))

        self.login_textoinicial = ctk.CTkLabel(self.painellogin, text="Bem-vindo ao Sistema!", font=("Arial", 24, "bold"), text_color=self.cor_textoprincipal)
        self.login_textoinicial.pack(pady=(0, 25))

        self.login_textousuario = ctk.CTkLabel(self.painellogin, text=" Usuário", font=("Arial", 14, "bold"), text_color=self.cor_textosecundario, image=self.imagemusuario, compound="left")
        self.login_textousuario.pack(anchor="w", padx=40, pady=(0, 5))

        self.login_usuarioinput = ctk.CTkEntry(self.painellogin, placeholder_text="Ex: User", width=400, height=40, corner_radius=8)
        self.login_usuarioinput.pack(pady=(0, 15))

        self.login_textosenha = ctk.CTkLabel(self.painellogin, text=" Senha", font=("Arial", 14, "bold"), text_color=self.cor_textosecundario, image=self.imagemcadeado, compound="left")
        self.login_textosenha.pack(anchor="w", padx=40, pady=(0, 5))

        self.login_senhainput = ctk.CTkEntry(self.painellogin, placeholder_text="********", show="*", width=400, height=40, corner_radius=8)
        self.login_senhainput.pack(pady=(0, 8))

        self.login_ver_senha = ctk.CTkCheckBox(self.painellogin, text="Mostrar senha", font=("Arial", 13), text_color=self.cor_textosecundario, checkbox_width=16, checkbox_height=16, command=lambda: self.mostrar_senha(self.login_ver_senha, self.login_senhainput))
        self.login_ver_senha.pack(anchor="w", padx=40, pady=(0, 70))

        self.login_botaologin = ctk.CTkButton(self.painellogin, text="Entrar", text_color="#FFFFFF", width=400, height=45, fg_color=self.cor_primaria, font=("Arial", 15, "bold"), corner_radius=8, command=self.fazer_login)
        self.login_botaologin.pack(pady=(0, 10))

        self.login_botaocadastro = ctk.CTkButton(self.painellogin, text="Criar Conta", text_color=self.cor_primaria, width=400, height=45, fg_color="transparent", hover_color="#E2E8F0", font=("Arial", 15, "bold"), corner_radius=8, command=self.mostrar_cadastro)
        self.login_botaocadastro.pack(pady=(0, 10))

        self.mensagemlogin = ctk.CTkLabel(self.painellogin, text="", font=("Arial", 12), text_color="red")
        self.mensagemlogin.pack(pady=(0, 10))

    def criar_tela_cadastro(self):
        self.painelcadastro = ctk.CTkFrame(self, fg_color=self.cor_cards, corner_radius=30, border_width=3, border_color=self.cor_bordas, width=470, height=610)
        self.painelcadastro.pack_propagate(False)

        self.cadastro_labelimagem = ctk.CTkLabel(self.painelcadastro, image=self.imagemcaixa, text="")
        self.cadastro_labelimagem.pack(pady=(25, 15))

        self.cadastro_textoinicial = ctk.CTkLabel(self.painelcadastro, text="Criar Nova Conta", font=("Arial", 24, "bold"), text_color=self.cor_textoprincipal)
        self.cadastro_textoinicial.pack(pady=(0, 15))

        self.cadastro_textousuario = ctk.CTkLabel(self.painelcadastro, text=" Crie um usuário", font=("Arial", 14, "bold"), text_color=self.cor_textosecundario, image=self.imagemusuario, compound="left")
        self.cadastro_textousuario.pack(anchor="w", padx=40, pady=(0, 5))

        self.cadastro_usuarioinput = ctk.CTkEntry(self.painelcadastro, placeholder_text="Ex: User", width=400, height=40, corner_radius=8)
        self.cadastro_usuarioinput.pack(pady=(0, 15))

        self.cadastro_textosenha = ctk.CTkLabel(self.painelcadastro, text=" Crie uma Senha", font=("Arial", 14, "bold"), text_color=self.cor_textosecundario, image=self.imagemcadeado, compound="left")
        self.cadastro_textosenha.pack(anchor="w", padx=40, pady=(0, 5))

        self.cadastro_senhainput = ctk.CTkEntry(self.painelcadastro, placeholder_text="********", show="*", width=400, height=40, corner_radius=8)
        self.cadastro_senhainput.pack(pady=(0, 5))

        self.cadastro_ver_senha = ctk.CTkCheckBox(self.painelcadastro, text="Mostrar senha", font=("Arial", 13), text_color=self.cor_textosecundario, checkbox_width=16, checkbox_height=16, command=lambda: self.mostrar_senha(self.cadastro_ver_senha, self.cadastro_senhainput))
        self.cadastro_ver_senha.pack(anchor="w", padx=40, pady=(0, 15))

        self.cadastro_textocargo = ctk.CTkLabel(self.painelcadastro, text="Selecione o Cargo", font=("Arial", 14, "bold"), text_color=self.cor_textosecundario)
        self.cadastro_textocargo.pack(anchor="w", padx=40, pady=(0, 5))

        self.cadastro_cargo_input = ctk.CTkOptionMenu(self.painelcadastro, values=["Vendedor", "Gerente"], width=400, height=38, corner_radius=8, fg_color=self.cor_fundo, button_color=self.cor_primaria, text_color=self.cor_textoprincipal, dropdown_hover_color=self.cor_bordas)
        self.cadastro_cargo_input.pack(pady=(0, 35))

        self.cadastro_botaocadastrar = ctk.CTkButton(self.painelcadastro, text="Cadastrar", text_color="#FFFFFF", width=400, height=45, fg_color=self.cor_primaria, font=("Arial", 15, "bold"), corner_radius=8, command=self.fazer_cadastro)
        self.cadastro_botaocadastrar.pack(pady=(0, 10))

        self.cadastro_botaovoltar = ctk.CTkButton(self.painelcadastro, text="Login", text_color=self.cor_primaria, width=400, height=45, fg_color="transparent", hover_color="#E2E8F0", font=("Arial", 15, "bold"), corner_radius=8, command=self.mostrar_login)
        self.cadastro_botaovoltar.pack(pady=(0, 7))

        self.mensagemcadastro = ctk.CTkLabel(self.painelcadastro, text="", font=("Arial", 12), text_color="red")
        self.mensagemcadastro.pack(pady=(0, 10))

    def mostrar_login(self):
        self.painelcadastro.place_forget()
        self.painellogin.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_cadastro(self):
        self.painellogin.place_forget()
        self.painelcadastro.place(relx=0.5, rely=0.5, anchor="center")

    def fazer_login(self):
        usuario = self.login_usuarioinput.get()
        senha = self.login_senhainput.get()

        sucesso, resultado = funcaologin(usuario, senha)

        if sucesso:
            cargo = resultado
            self.mensagemlogin.configure(
                text="Login bem sucedido!",
                text_color="green")
            self.mensagemlogin.after(5000, lambda: self.mensagemlogin.configure(text="", text_color="red"))
            self.login_usuarioinput.delete(0, "end")
            self.login_senhainput.delete(0, "end")
            self.after(1000, lambda: self.controller.abrir_vendas(cargo))
        else:
            self.mensagemlogin.configure(
                text=resultado,
                text_color="red"
            )
            self.mensagemlogin.after(5000, lambda: self.mensagemlogin.configure(text="", text_color="red"))

    def fazer_cadastro(self):
        usuario = self.cadastro_usuarioinput.get()
        senha = self.cadastro_senhainput.get()
        cargo = self.cadastro_cargo_input.get()

        if len(str(senha)) < 4:
            self.mensagemcadastro.configure(
                text="Erro: A senha deve ter pelo menos 4 caracteres",
                text_color="red"
            )
            self.mensagemcadastro.after(5000, lambda: self.mensagemcadastro.configure(text="", text_color="red"))
            return
        elif len(str(senha)) > 10:
            self.mensagemcadastro.configure(
                text="Erro: A senha deve ter no máximo 10 caracteres",
                text_color="red"
            )
            self.mensagemcadastro.after(5000, lambda: self.mensagemcadastro.configure(text="", text_color="red"))
            return
        elif len(str(usuario)) < 4:
            self.mensagemcadastro.configure(
                text="Erro: O nome de usuário deve ter no mínimo 4 caracteres",
                text_color="red"
            )
            self.mensagemcadastro.after(5000, lambda: self.mensagemcadastro.configure(text="", text_color="red"))
            return
        elif len(str(usuario)) > 20:
            self.mensagemcadastro.configure(
                text="Erro: O nome de usuário deve ter no máximo 20 caracteres",
                text_color="red"
            )
            self.mensagemcadastro.after(5000, lambda: self.mensagemcadastro.configure(text="", text_color="red"))
            return

        sucesso, resultado = funcaocadastro(usuario, senha, cargo)

        if sucesso:
            cargo = resultado
            print("Conta criada" + f" com sucesso! Usuário: {usuario}, Senha: {senha}, Cargo: {cargo}")
            self.mensagemcadastro.configure(
                text="Conta criada com sucesso!",
                text_color="green"
            )
            self.mensagemcadastro.after(5000, lambda: self.mensagemcadastro.configure(text="", text_color="red"))
            self.cadastro_usuarioinput.delete(0, "end")
            self.cadastro_senhainput.delete(0, "end")
            self.after(1000, lambda: self.controller.abrir_vendas(cargo))
        else:
            self.mensagemcadastro.configure(
                text=resultado,
                text_color="red"
            )
            self.mensagemcadastro.after(5000, lambda: self.mensagemcadastro.configure(text="", text_color="red"))

if __name__ == "__main__":
    app = TelaAutenticacao()
    app.mainloop()