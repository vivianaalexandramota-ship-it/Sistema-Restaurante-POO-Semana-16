class Usuario:
    ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, id, nombre, usuario, contrasena, rol="Cliente"):
        self.id = str(id).strip()
        self.nombre = str(nombre).strip()
        self.usuario = str(usuario).strip()
        self.contrasena = str(contrasena)
        self.rol = str(rol).strip()

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }
