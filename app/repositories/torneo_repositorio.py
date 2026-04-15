from app.models.torneo import Torneo
from app import db


class TorneoRepository:
    @staticmethod
    def agregar_torneo(nombre, max_fechas):
        nuevo_torneo = Torneo(nombre=nombre, max_fechas=max_fechas)
        db.session.add(nuevo_torneo)
        db.session.commit()
        return {
            "mensaje": "Torneo agregado",
            "id": nuevo_torneo.id,
            "nombre": nuevo_torneo.nombre,
            "max_fechas": nuevo_torneo.max_fechas,
        }

    @staticmethod
    def obtener_torneos():
        torneos = Torneo.query.order_by(Torneo.id.asc()).all()
        return [
            {"id": t.id, "nombre": t.nombre, "max_fechas": t.max_fechas}
            for t in torneos
        ]

    @staticmethod
    def actualizar_torneo(torneo_id: int, nombre: str, max_fechas: int):
        torneo = Torneo.query.get(torneo_id)
        if not torneo:
            return None
        torneo.nombre = nombre
        torneo.max_fechas = max_fechas
        db.session.commit()
        return {"id": torneo.id, "nombre": torneo.nombre, "max_fechas": torneo.max_fechas}

    @staticmethod
    def eliminar_torneo(torneo_id: int) -> bool:
        torneo = Torneo.query.get(torneo_id)
        if not torneo:
            return False
        db.session.delete(torneo)
        db.session.commit()
        return True

    @staticmethod
    def guardar_seleccion(data):
        # Aquí podrías guardar la selección en la base de datos si corresponde
        # Por ahora solo retorna el dato recibido
        return {"mensaje": "Selección guardada", "data": data}
