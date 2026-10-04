class Venta:
    def __init__(self, id, usuario_id, usuario_nombre, producto_id, producto_nombre, fecha):
        self.id = str(id).strip()
        self.usuario_id = str(usuario_id).strip()
        self.usuario_nombre = str(usuario_nombre).strip()
        self.producto_id = str(producto_id).strip()
        self.producto_nombre = str(producto_nombre).strip()
        self.fecha = str(fecha).strip()

    def a_diccionario(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "usuario_nombre": self.usuario_nombre,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "fecha": self.fecha,
        }
