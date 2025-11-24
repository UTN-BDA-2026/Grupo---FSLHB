# app/services/torneo_service.py
from app.repositories.torneo_repositorio import TorneoRepository

class TorneoService:
    @staticmethod
    def obtener_torneos():
        return TorneoRepository.obtener_torneos()

    @staticmethod
    def guardar_seleccion(data):
        # Aquí podrías guardar la selección en la base de datos si lo necesitas
        return TorneoRepository.guardar_seleccion(data)
