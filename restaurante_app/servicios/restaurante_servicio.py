from datetime import datetime
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, carpeta_datos=None):
        # Ruta robusta: se calcula desde este archivo y no desde la terminal.
        base = Path(carpeta_datos) if carpeta_datos else Path(__file__).resolve().parents[1] / "datos"
        self.ruta_productos = base / "productos.json"
        self.ruta_usuarios = base / "usuarios.json"
        self.ruta_ventas = base / "ventas.json"

    # ---------- Usuarios ----------
    def listar_usuarios(self):
        return [Usuario(**dato) for dato in ArchivoServicio.leer_json(self.ruta_usuarios)]

    def buscar_usuario(self, usuario_id):
        usuario_id = str(usuario_id).strip()
        return next((u for u in self.listar_usuarios() if u.id == usuario_id), None)

    def validar_acceso(self, usuario, contrasena):
        usuario = str(usuario).strip()
        for item in self.listar_usuarios():
            if item.usuario == usuario and item.contrasena == str(contrasena):
                return item
        return None

    def registrar_usuario(self, nombre, usuario, contrasena, rol):
        self._validar_datos_usuario(nombre, usuario, contrasena, rol)
        usuarios = self.listar_usuarios()

        nombre_usuario = str(usuario).strip().lower()
        if any(u.usuario.lower() == nombre_usuario for u in usuarios):
            raise ValueError("Ya existe un usuario con ese nombre de acceso.")

        nuevo_id = self._siguiente_id_usuario(usuarios)
        nuevo = Usuario(nuevo_id, nombre, usuario, contrasena, rol)
        usuarios.append(nuevo)
        self._guardar_usuarios(usuarios)
        return nuevo

    def actualizar_usuario(self, usuario_id, nombre, usuario, contrasena, rol):
        usuario_id = str(usuario_id).strip()
        existente = self.buscar_usuario(usuario_id)
        if not existente:
            raise ValueError("No se encontró el usuario seleccionado.")
        if existente.rol == "Administrador":
            raise ValueError("La cuenta Administrador no se modifica desde esta sección.")

        self._validar_datos_usuario(nombre, usuario, contrasena, rol)
        usuarios = self.listar_usuarios()
        nombre_usuario = str(usuario).strip().lower()
        if any(u.id != usuario_id and u.usuario.lower() == nombre_usuario for u in usuarios):
            raise ValueError("Ya existe otro usuario con ese nombre de acceso.")

        actualizado = Usuario(usuario_id, nombre, usuario, contrasena, rol)
        for indice, item in enumerate(usuarios):
            if item.id == usuario_id:
                usuarios[indice] = actualizado
                break
        self._guardar_usuarios(usuarios)
        return actualizado

    def eliminar_usuario(self, usuario_id, usuario_actual_id=None):
        usuario_id = str(usuario_id).strip()
        usuario_actual_id = str(usuario_actual_id).strip() if usuario_actual_id is not None else ""
        existente = self.buscar_usuario(usuario_id)
        if not existente:
            raise ValueError("No se encontró el usuario seleccionado.")
        if usuario_id == usuario_actual_id:
            raise ValueError("No puede eliminar la cuenta con la que inició sesión.")
        if existente.rol == "Administrador":
            raise ValueError("La cuenta Administrador está protegida y no puede eliminarse.")

        usuarios = [u for u in self.listar_usuarios() if u.id != usuario_id]
        self._guardar_usuarios(usuarios)

    @staticmethod
    def _siguiente_id_usuario(usuarios):
        numeros = []
        for item in usuarios:
            texto = item.id.upper()
            if texto.startswith("U") and texto[1:].isdigit():
                numeros.append(int(texto[1:]))
        return f"U{(max(numeros, default=0) + 1):03d}"

    @staticmethod
    def _validar_datos_usuario(nombre, usuario, contrasena, rol):
        if not str(nombre).strip() or not str(usuario).strip() or not str(contrasena):
            raise ValueError("Complete nombre, usuario y contraseña.")
        if str(rol).strip() not in ("Empleado", "Cliente"):
            raise ValueError("Seleccione un rol válido: Empleado o Cliente.")
        if len(str(usuario).strip()) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")
        if len(str(contrasena)) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")

    def _guardar_usuarios(self, usuarios):
        ArchivoServicio.guardar_json(self.ruta_usuarios, [u.a_diccionario() for u in usuarios])

    # ---------- Productos ----------
    def listar_productos(self):
        return [Producto(**dato) for dato in ArchivoServicio.leer_json(self.ruta_productos)]

    def buscar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        return next((p for p in self.listar_productos() if p.id == producto_id), None)

    def registrar_producto(self, producto_id, nombre, categoria, precio, cantidad):
        self._validar_producto(producto_id, nombre, categoria, precio, cantidad)
        if self.buscar_producto(producto_id):
            raise ValueError("Ya existe un producto con ese ID.")

        producto = Producto(producto_id, nombre, categoria, precio, cantidad)
        datos = [p.a_diccionario() for p in self.listar_productos()]
        datos.append(producto.a_diccionario())
        ArchivoServicio.guardar_json(self.ruta_productos, datos)
        return producto

    def actualizar_producto(self, producto_id, nombre, categoria, precio, cantidad):
        self._validar_producto(producto_id, nombre, categoria, precio, cantidad)
        productos = self.listar_productos()
        encontrado = False
        for i, producto in enumerate(productos):
            if producto.id == str(producto_id).strip():
                productos[i] = Producto(producto_id, nombre, categoria, precio, cantidad)
                encontrado = True
                break
        if not encontrado:
            raise ValueError("No se encontró el producto indicado.")
        ArchivoServicio.guardar_json(self.ruta_productos, [p.a_diccionario() for p in productos])
        return productos[i]

    def eliminar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        productos = self.listar_productos()
        nuevos = [p for p in productos if p.id != producto_id]
        if len(nuevos) == len(productos):
            raise ValueError("No se encontró el producto indicado.")
        ArchivoServicio.guardar_json(self.ruta_productos, [p.a_diccionario() for p in nuevos])

    @staticmethod
    def _validar_producto(producto_id, nombre, categoria, precio, cantidad):
        if not str(producto_id).strip() or not str(nombre).strip() or not str(categoria).strip():
            raise ValueError("Complete todos los datos del producto.")
        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("Precio y cantidad deben ser valores numéricos.")
        if precio < 0 or cantidad < 0:
            raise ValueError("Precio y cantidad no pueden ser negativos.")

    # ---------- Ventas ----------
    def listar_ventas(self):
        return [Venta(**dato) for dato in ArchivoServicio.leer_json(self.ruta_ventas)]

    def registrar_venta(self, usuario_id, producto_id):
        usuario_id = str(usuario_id).strip()
        producto_id = str(producto_id).strip()

        usuario = self.buscar_usuario(usuario_id)
        if not usuario:
            raise ValueError("Seleccione un usuario registrado.")

        producto = self.buscar_producto(producto_id)
        if not producto:
            raise ValueError("Seleccione un producto registrado.")

        ventas = self.listar_ventas()
        nuevo_id = f"V{len(ventas) + 1:03d}"
        venta = Venta(
            nuevo_id,
            usuario.id,
            usuario.nombre,
            producto.id,
            producto.nombre,
            datetime.now().strftime("%d/%m/%Y %H:%M"),
        )
        ventas.append(venta)
        ArchivoServicio.guardar_json(self.ruta_ventas, [v.a_diccionario() for v in ventas])
        return venta
