class Producto:
    def __init__(self, id, nombre, categoria, precio, cantidad):
        self.id = str(id).strip()
        self.nombre = str(nombre).strip()
        self.categoria = str(categoria).strip()
        self.precio = float(precio)
        self.cantidad = int(cantidad)

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "cantidad": self.cantidad,
        }
