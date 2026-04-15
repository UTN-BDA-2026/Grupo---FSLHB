# app/services/torneo_service.py
from app.repositories.torneo_repositorio import TorneoRepository


class TorneoService:
    @staticmethod
    def obtener_torneos():
        return TorneoRepository.obtener_torneos()

    @staticmethod
    def crear_torneo(nombre: str, max_fechas: int):
        return TorneoRepository.agregar_torneo(nombre, max_fechas)

    @staticmethod
    def actualizar_torneo(torneo_id: int, nombre: str, max_fechas: int):
        return TorneoRepository.actualizar_torneo(torneo_id, nombre, max_fechas)

    @staticmethod
    def eliminar_torneo(torneo_id: int) -> bool:
        return TorneoRepository.eliminar_torneo(torneo_id)

    @staticmethod
    def guardar_seleccion(data):
        # Aquí podrías guardar la selección en la base de datos si lo necesitas
        return TorneoRepository.guardar_seleccion(data)
