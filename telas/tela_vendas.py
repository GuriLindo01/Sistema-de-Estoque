import customtkinter as ctk
from PIL import Image

class TelaVendas(ctk.CTkFrame):
    def __init__(self, master, controller, cargo="Vendedor"):
        super().__init__(master)

        self.controller = controller

        self.cargo = cargo
        self.configure(fg_color="#F0F0F0")

        self.label_teste = ctk.CTkLabel(self, text=f"", font=("Arial", 24, "bold"),text_color="#0F172A")
        self.label_teste.pack(pady=50)

    def atualizar_cargo(self, cargo):
        self.cargo = cargo
        self.label_teste.configure(text=f"Nível de acesso:  {self.cargo}")
