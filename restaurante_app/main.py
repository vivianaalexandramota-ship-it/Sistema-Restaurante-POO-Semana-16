import tkinter as tk
from tkinter import ttk

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante App - Semana 16")
        self.root.geometry("1050x690")
        self.root.minsize(940, 620)

        self._configurar_estilos()
        self.servicio = RestauranteServicio()
        self.vista_actual = None
        self.mostrar_login()

    def _configurar_estilos(self):
        estilo = ttk.Style(self.root)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        estilo.configure("TButton", padding=(10, 6))
        estilo.configure("Treeview", rowheight=26)
        estilo.configure("Error.TLabel", foreground="firebrick")
        estilo.configure("Info.TLabel", font=("Segoe UI", 9, "italic"))

    def _cambiar_vista(self, nueva_vista):
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = nueva_vista

    def mostrar_login(self):
        self._cambiar_vista(LoginView(self.root, self.servicio, self.mostrar_principal))

    def mostrar_principal(self, usuario):
        self._cambiar_vista(MainView(self.root, self.servicio, usuario, self.mostrar_login))

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    RestauranteApp().ejecutar()
