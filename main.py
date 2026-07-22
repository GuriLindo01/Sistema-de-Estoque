from telas.tela_login import TelaAutenticacao
from telas.tela_vendas import TelaVendas
from telas.tela_estoque import TelaEstoque

from database.tabelas import criar_tabelas
import customtkinter as ctk

criar_tabelas()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.after(0, lambda: self.state("zoomed"))

        self.login = TelaAutenticacao(master = self, controller = self)
        self.vendas = TelaVendas(master = self, controller = self)
        self.estoque = TelaEstoque(master = self, controller = self)

        self.login.pack(fill="both", expand=True)

    def abrir_vendas(self, cargo):
        self.login.pack_forget()
        self.vendas.atualizar_cargo(cargo)
        self.vendas.pack(fill="both", expand=True)

app = App()
app.mainloop()