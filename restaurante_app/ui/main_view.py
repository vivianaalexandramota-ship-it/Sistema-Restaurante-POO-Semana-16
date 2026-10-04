import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


class MainView(ttk.Frame):
    def __init__(self, master, servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master)
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        self.usuario_seleccionado_id = None

        # Variables de usuarios (Semana 16)
        self.usr_id = tk.StringVar()
        self.usr_nombre = tk.StringVar()
        self.usr_usuario = tk.StringVar()
        self.usr_contrasena = tk.StringVar()
        self.usr_rol = tk.StringVar(value="Cliente")
        self.usr_estado = tk.StringVar(value="Seleccione un usuario o registre uno nuevo.")

        # Variables ya existentes de productos
        self.prod_id = tk.StringVar()
        self.prod_nombre = tk.StringVar()
        self.prod_categoria = tk.StringVar()
        self.prod_precio = tk.StringVar()
        self.prod_cantidad = tk.StringVar()

        # Variables ya existentes de ventas
        self.venta_usuario = tk.StringVar()
        self.venta_producto = tk.StringVar()

        self._crear_interfaz()
        self._actualizar_todo()

    def _crear_interfaz(self):
        self.pack(fill="both", expand=True)

        encabezado = ttk.Frame(self, padding=(16, 10))
        encabezado.pack(fill="x")

        ruta_icono = Path(__file__).resolve().parents[1] / "assets" / "icon.png"
        self.icono = tk.PhotoImage(file=str(ruta_icono))
        ttk.Label(encabezado, image=self.icono).pack(side="left", padx=(0, 8))
        ttk.Label(encabezado, text="Restaurante App", style="Title.TLabel").pack(side="left")
        ttk.Label(
            encabezado,
            text=f"Sesión: {self.usuario_actual.nombre} | Rol: {self.usuario_actual.rol}",
        ).pack(side="right", padx=12)
        ttk.Button(encabezado, text="Cerrar sesión", command=self.al_cerrar_sesion).pack(side="right")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.tab_usuarios = ttk.Frame(self.notebook, padding=12)
        self.tab_productos = ttk.Frame(self.notebook, padding=12)
        self.tab_ventas = ttk.Frame(self.notebook, padding=12)

        # Solo Administrador accede a la gestión administrativa de usuarios.
        if self.usuario_actual.rol == "Administrador":
            self.notebook.add(self.tab_usuarios, text="Usuarios")
            self._crear_usuarios()

        self.notebook.add(self.tab_productos, text="Productos")
        self.notebook.add(self.tab_ventas, text="Ventas")

        self._crear_productos()
        self._crear_ventas()

    # ================================================================
    # USUARIOS - SEMANA 16
    # ================================================================
    def _crear_usuarios(self):
        formulario = ttk.LabelFrame(self.tab_usuarios, text="Gestión administrativa de usuarios", padding=12)
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="ID").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Label(formulario, text="Nombre").grid(row=0, column=1, sticky="w", padx=4)
        ttk.Label(formulario, text="Usuario").grid(row=0, column=2, sticky="w", padx=4)
        ttk.Label(formulario, text="Contraseña").grid(row=0, column=3, sticky="w", padx=4)
        ttk.Label(formulario, text="Rol").grid(row=0, column=4, sticky="w", padx=4)

        entrada_id = ttk.Entry(formulario, textvariable=self.usr_id, width=11, state="readonly")
        entrada_nombre = ttk.Entry(formulario, textvariable=self.usr_nombre, width=24)
        entrada_usuario = ttk.Entry(formulario, textvariable=self.usr_usuario, width=18)
        entrada_clave = ttk.Entry(formulario, textvariable=self.usr_contrasena, show="*", width=18)
        self.combo_rol = ttk.Combobox(
            formulario,
            textvariable=self.usr_rol,
            values=("Empleado", "Cliente"),
            state="readonly",
            width=16,
        )

        entrada_id.grid(row=1, column=0, padx=4, pady=4)
        entrada_nombre.grid(row=1, column=1, padx=4, pady=4)
        entrada_usuario.grid(row=1, column=2, padx=4, pady=4)
        entrada_clave.grid(row=1, column=3, padx=4, pady=4)
        self.combo_rol.grid(row=1, column=4, padx=4, pady=4)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, sticky="w", pady=(8, 0))

        # Los botones conservan command=, tal como exige la rúbrica.
        ttk.Button(acciones, text="Registrar", command=self._callback_registrar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Actualizar", command=self._callback_actualizar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Eliminar", command=self._callback_eliminar_usuario).pack(side="left", padx=3)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_usuario).pack(side="left", padx=3)

        ttk.Label(formulario, textvariable=self.usr_estado, style="Info.TLabel").grid(
            row=3, column=0, columnspan=5, sticky="w", padx=4, pady=(9, 0)
        )
        ttk.Label(
            formulario,
            text="Atajos: Enter = registrar | Esc = limpiar/cancelar selección",
        ).grid(row=4, column=0, columnspan=5, sticky="w", padx=4, pady=(4, 0))

        columnas = ("id", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(
            self.tab_usuarios,
            columns=columnas,
            show="headings",
            height=13,
            selectmode="browse",
        )
        for col, titulo, ancho in [
            ("id", "ID", 90),
            ("nombre", "Nombre", 250),
            ("usuario", "Usuario", 180),
            ("rol", "Rol", 160),
        ]:
            self.tabla_usuarios.heading(col, text=titulo)
            self.tabla_usuarios.column(col, width=ancho, anchor="center")
        self.tabla_usuarios.pack(fill="both", expand=True)

        # Eventos obligatorios de Semana 16 mediante bind().
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self._evento_seleccionar_usuario)
        self.combo_rol.bind("<<ComboboxSelected>>", self._evento_cambio_rol)

        for widget in (entrada_nombre, entrada_usuario, entrada_clave, self.combo_rol):
            widget.bind("<Return>", self._evento_enter_usuario)
            widget.bind("<Escape>", self._evento_escape_usuario)
        self.tabla_usuarios.bind("<Escape>", self._evento_escape_usuario)

    def _evento_seleccionar_usuario(self, _evento):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return

        # La tabla entrega únicamente el ID; el objeto completo se consulta al servicio.
        usuario_id = str(valores[0])
        usuario = self.servicio.buscar_usuario(usuario_id)
        if not usuario:
            messagebox.showwarning("Usuarios", "No fue posible recuperar el usuario seleccionado.")
            return

        self.usuario_seleccionado_id = usuario.id
        self.usr_id.set(usuario.id)
        self.usr_nombre.set(usuario.nombre)
        self.usr_usuario.set(usuario.usuario)
        self.usr_contrasena.set(usuario.contrasena)
        self.usr_rol.set(usuario.rol)

        if usuario.rol == "Administrador":
            self.usr_estado.set("Cuenta Administrador protegida: solo consulta desde esta sección.")
        else:
            self.usr_estado.set(f"Usuario {usuario.id} cargado para actualizar o eliminar.")

    def _evento_enter_usuario(self, _evento):
        # Reutiliza el método existente: no duplica la lógica de registro.
        self._callback_registrar_usuario()
        return "break"

    def _evento_escape_usuario(self, _evento):
        self._limpiar_usuario()
        return "break"

    def _evento_cambio_rol(self, _evento):
        rol = self.usr_rol.get()
        self.usr_estado.set(f"Rol seleccionado: {rol}.")

    def _callback_registrar_usuario(self):
        try:
            nuevo = self.servicio.registrar_usuario(
                self.usr_nombre.get(),
                self.usr_usuario.get(),
                self.usr_contrasena.get(),
                self.usr_rol.get(),
            )
            self._actualizar_usuarios()
            self._actualizar_selectores_venta()
            self._limpiar_usuario()
            messagebox.showinfo("Usuarios", f"Usuario {nuevo.id} registrado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Usuarios", str(error))

    def _callback_actualizar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Usuarios", "Seleccione primero un usuario en la tabla.")
            return
        try:
            actualizado = self.servicio.actualizar_usuario(
                self.usuario_seleccionado_id,
                self.usr_nombre.get(),
                self.usr_usuario.get(),
                self.usr_contrasena.get(),
                self.usr_rol.get(),
            )
            self._actualizar_usuarios()
            self._actualizar_selectores_venta()
            self._limpiar_usuario()
            messagebox.showinfo("Usuarios", f"Usuario {actualizado.id} actualizado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Usuarios", str(error))

    def _callback_eliminar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Usuarios", "Seleccione primero un usuario en la tabla.")
            return

        usuario = self.servicio.buscar_usuario(self.usuario_seleccionado_id)
        if not usuario:
            messagebox.showwarning("Usuarios", "No se encontró el usuario seleccionado.")
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar a {usuario.nombre} ({usuario.usuario})?",
        ):
            return

        try:
            self.servicio.eliminar_usuario(
                self.usuario_seleccionado_id,
                usuario_actual_id=self.usuario_actual.id,
            )
            self._actualizar_usuarios()
            self._actualizar_selectores_venta()
            self._limpiar_usuario()
            messagebox.showinfo("Usuarios", "Usuario eliminado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Usuarios", str(error))

    def _limpiar_usuario(self):
        self.usuario_seleccionado_id = None
        self.usr_id.set("")
        self.usr_nombre.set("")
        self.usr_usuario.set("")
        self.usr_contrasena.set("")
        self.usr_rol.set("Cliente")
        self.usr_estado.set("Formulario limpio. Puede registrar un nuevo usuario.")
        if hasattr(self, "tabla_usuarios"):
            self.tabla_usuarios.selection_remove(self.tabla_usuarios.selection())

    # ================================================================
    # PRODUCTOS - FUNCIONALIDAD CONSERVADA
    # ================================================================
    def _crear_productos(self):
        formulario = ttk.LabelFrame(self.tab_productos, text="Gestión de productos", padding=12)
        formulario.pack(fill="x", pady=(0, 10))

        campos = [
            ("ID", self.prod_id),
            ("Nombre", self.prod_nombre),
            ("Categoría", self.prod_categoria),
            ("Precio", self.prod_precio),
            ("Cantidad", self.prod_cantidad),
        ]
        for i, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(row=0, column=i, padx=4, sticky="w")
            ttk.Entry(formulario, textvariable=variable, width=17).grid(row=1, column=i, padx=4, pady=4)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, sticky="w", pady=(8, 0))
        ttk.Button(acciones, text="Registrar", command=self._callback_registrar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Cargar/Consultar", command=self._callback_cargar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Actualizar", command=self._callback_actualizar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Eliminar", command=self._callback_eliminar_producto).pack(side="left", padx=3)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_producto).pack(side="left", padx=3)

        columnas = ("id", "nombre", "categoria", "precio", "cantidad")
        self.tabla_productos = ttk.Treeview(self.tab_productos, columns=columnas, show="headings", height=12)
        titulos = [
            ("id", "ID", 80),
            ("nombre", "Nombre", 220),
            ("categoria", "Categoría", 160),
            ("precio", "Precio", 100),
            ("cantidad", "Cantidad", 100),
        ]
        for col, titulo, ancho in titulos:
            self.tabla_productos.heading(col, text=titulo)
            self.tabla_productos.column(col, width=ancho, anchor="center")
        self.tabla_productos.pack(fill="both", expand=True)

    def _callback_registrar_producto(self):
        try:
            self.servicio.registrar_producto(
                self.prod_id.get(), self.prod_nombre.get(), self.prod_categoria.get(),
                self.prod_precio.get(), self.prod_cantidad.get()
            )
            self._actualizar_productos()
            self._actualizar_selectores_venta()
            self._limpiar_producto()
            messagebox.showinfo("Productos", "Producto registrado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Productos", str(error))

    def _callback_cargar_producto(self):
        producto = self.servicio.buscar_producto(self.prod_id.get())
        if not producto:
            messagebox.showwarning("Productos", "No se encontró el producto indicado.")
            return
        self.prod_nombre.set(producto.nombre)
        self.prod_categoria.set(producto.categoria)
        self.prod_precio.set(str(producto.precio))
        self.prod_cantidad.set(str(producto.cantidad))

    def _callback_actualizar_producto(self):
        try:
            self.servicio.actualizar_producto(
                self.prod_id.get(), self.prod_nombre.get(), self.prod_categoria.get(),
                self.prod_precio.get(), self.prod_cantidad.get()
            )
            self._actualizar_productos()
            self._actualizar_selectores_venta()
            messagebox.showinfo("Productos", "Producto actualizado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Productos", str(error))

    def _callback_eliminar_producto(self):
        try:
            self.servicio.eliminar_producto(self.prod_id.get())
            self._actualizar_productos()
            self._actualizar_selectores_venta()
            self._limpiar_producto()
            messagebox.showinfo("Productos", "Producto eliminado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Productos", str(error))

    # ================================================================
    # VENTAS - FUNCIONALIDAD CONSERVADA DE SEMANA 15
    # ================================================================
    def _crear_ventas(self):
        panel = ttk.LabelFrame(self.tab_ventas, text="Registrar venta", padding=14)
        panel.pack(fill="x", pady=(0, 10))

        ttk.Label(panel, text="Usuario").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(panel, text="Producto").grid(row=0, column=1, sticky="w", padx=5)

        self.combo_usuario = ttk.Combobox(panel, textvariable=self.venta_usuario, state="readonly", width=35)
        self.combo_producto = ttk.Combobox(panel, textvariable=self.venta_producto, state="readonly", width=40)
        self.combo_usuario.grid(row=1, column=0, padx=5, pady=5)
        self.combo_producto.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(panel, text="Registrar venta", command=self._callback_registrar_venta).grid(
            row=1, column=2, padx=10, pady=5
        )

        columnas = ("id", "usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(self.tab_ventas, columns=columnas, show="headings", height=15)
        for col, titulo, ancho in [
            ("id", "ID", 80),
            ("usuario", "Usuario", 210),
            ("producto", "Producto", 240),
            ("fecha", "Fecha", 170),
        ]:
            self.tabla_ventas.heading(col, text=titulo)
            self.tabla_ventas.column(col, width=ancho, anchor="center")
        self.tabla_ventas.pack(fill="both", expand=True)

    def _callback_registrar_venta(self):
        try:
            usuario_id = self._extraer_id(self.venta_usuario.get())
            producto_id = self._extraer_id(self.venta_producto.get())
            venta = self.servicio.registrar_venta(usuario_id, producto_id)
            self._actualizar_ventas()
            self.venta_usuario.set("")
            self.venta_producto.set("")
            messagebox.showinfo("Ventas", f"Venta {venta.id} registrada correctamente.")
        except ValueError as error:
            messagebox.showwarning("Ventas", str(error))

    @staticmethod
    def _extraer_id(texto):
        if not texto or " - " not in texto:
            return ""
        return texto.split(" - ", 1)[0].strip()

    # ================================================================
    # ACTUALIZACIÓN VISUAL
    # ================================================================
    def _actualizar_todo(self):
        if self.usuario_actual.rol == "Administrador":
            self._actualizar_usuarios()
        self._actualizar_productos()
        self._actualizar_selectores_venta()
        self._actualizar_ventas()

    def _actualizar_usuarios(self):
        if not hasattr(self, "tabla_usuarios"):
            return
        self._vaciar(self.tabla_usuarios)
        for u in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert("", "end", values=(u.id, u.nombre, u.usuario, u.rol))

    def _actualizar_productos(self):
        self._vaciar(self.tabla_productos)
        for p in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "", "end", values=(p.id, p.nombre, p.categoria, f"${p.precio:.2f}", p.cantidad)
            )

    def _actualizar_selectores_venta(self):
        self.combo_usuario["values"] = [f"{u.id} - {u.nombre}" for u in self.servicio.listar_usuarios()]
        self.combo_producto["values"] = [f"{p.id} - {p.nombre}" for p in self.servicio.listar_productos()]

    def _actualizar_ventas(self):
        self._vaciar(self.tabla_ventas)
        for v in self.servicio.listar_ventas():
            self.tabla_ventas.insert("", "end", values=(v.id, v.usuario_nombre, v.producto_nombre, v.fecha))

    @staticmethod
    def _vaciar(tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def _limpiar_producto(self):
        for variable in [self.prod_id, self.prod_nombre, self.prod_categoria, self.prod_precio, self.prod_cantidad]:
            variable.set("")
