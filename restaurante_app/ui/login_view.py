import tkinter as tk
from tkinter import ttk
from pathlib import Path


class LoginView(ttk.Frame):
    def __init__(self, master, servicio, al_ingresar):
        super().__init__(master, padding=24)
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.mensaje_var = tk.StringVar()
        self._crear_interfaz()

    def _crear_interfaz(self):
        self.pack(fill="both", expand=True)

        tarjeta = ttk.Frame(self, padding=28)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        ruta_logo = Path(__file__).resolve().parents[1] / "assets" / "logo.png"
        self.logo = tk.PhotoImage(file=str(ruta_logo))
        ttk.Label(tarjeta, image=self.logo).grid(row=0, column=0, columnspan=2, pady=(0, 12))

        ttk.Label(tarjeta, text="Sistema Restaurante", style="Title.TLabel").grid(
            row=1, column=0, columnspan=2, pady=(0, 18)
        )
        ttk.Label(tarjeta, text="Usuario:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(tarjeta, textvariable=self.usuario_var, width=28).grid(row=2, column=1, pady=6)

        ttk.Label(tarjeta, text="Contraseña:").grid(row=3, column=0, sticky="w", pady=6)
        entrada = ttk.Entry(tarjeta, textvariable=self.contrasena_var, show="*", width=28)
        entrada.grid(row=3, column=1, pady=6)

        # Fundamento de eventos: command= asocia el botón con el callback.
        ttk.Button(tarjeta, text="Ingresar", command=self._callback_ingresar).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(14, 6)
        )
        ttk.Label(tarjeta, textvariable=self.mensaje_var, style="Error.TLabel").grid(
            row=5, column=0, columnspan=2
        )
        entrada.bind("<Return>", lambda _evento: self._callback_ingresar())

    def _callback_ingresar(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get()
        if not usuario or not contrasena:
            self.mensaje_var.set("Ingrese usuario y contraseña.")
            return
        encontrado = self.servicio.validar_acceso(usuario, contrasena)
        if encontrado:
            self.mensaje_var.set("")
            self.al_ingresar(encontrado)
        else:
            self.mensaje_var.set("Credenciales incorrectas.")
