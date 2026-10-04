import json
from pathlib import Path


class ArchivoServicio:
    @staticmethod
    def leer_json(ruta):
        ruta = Path(ruta)
        if not ruta.exists():
            return []
        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def guardar_json(ruta, datos):
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
