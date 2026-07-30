from telas.tela_login import TelaAutenticacao
from telas.tela_vendas import TelaVendas
from telas.tela_estoque import TelaEstoque
from telas.tela_historico import TelaHistorico
import json
import os

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
        self.historico = TelaHistorico(master = self, controller = self)

        self.verificar_sessao()

    def verificar_sessao(self):
        if os.path.exists("sessao.json"):
            try:
                with open("sessao.json", "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if dados.get("logado") is True:

                        usuario = dados.get("usuario", "Usuario")
                        cargo = dados.get("cargo", "Vendedor")
                        self.abrir_estoque(cargo, usuario)
                        return
            except Exception:
                pass
        self.abrir_login()

    def abrir_vendas(self, cargo, usuario):
        self.login.pack_forget()
        self.estoque.pack_forget()
        self.historico.pack_forget()
        self.vendas.menu.atualizar_informacoes(cargo, usuario)
        self.vendas.pack(fill="both", expand=True)

    def abrir_estoque(self, cargo, usuario):
        self.login.pack_forget()
        self.vendas.pack_forget()
        self.historico.pack_forget()
        self.estoque.menu.atualizar_informacoes(cargo, usuario)
        self.estoque.pack(fill="both", expand=True)

    def abrir_historico(self, cargo, usuario):
        self.login.pack_forget()
        self.vendas.pack_forget()
        self.estoque.pack_forget()
        self.historico.menu.atualizar_informacoes(cargo, usuario)
        self.historico.pack(fill="both", expand=True)

    def abrir_login(self):
        self.estoque.pack_forget()
        self.vendas.pack_forget()
        self.historico.pack_forget()
        self.login.pack(fill="both", expand=True)

    def deslogar(self):
        if os.path.exists("sessao.json"):
            os.remove("sessao.json")
        self.abrir_login()

app = App()
app.mainloop()