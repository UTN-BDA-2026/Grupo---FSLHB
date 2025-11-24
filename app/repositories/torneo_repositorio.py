# app/repositories/torneo_repositorio.py
class TorneoRepository:
    @staticmethod
    def obtener_torneos():
        # Aquí deberías consultar la base de datos real
        return [
            {"id": 1, "nombre": "Clausura Damas A", "max_fechas": 14},
            {"id": 2, "nombre": "Clausura Caballeros", "max_fechas": 10},
            {"id": 3, "nombre": "Clausura Mamis", "max_fechas": 12}
        ]

    @staticmethod
    def guardar_seleccion(data):
        # Aquí podrías guardar la selección en la base de datos
        # Por ahora solo retorna el dato recibido
        return {"mensaje": "Selección guardada", "data": data}
