import customtkinter as ctk
from PIL import Image

class TelaEstoque(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.configure(fg_color="#F0F0F0")