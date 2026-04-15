from app import db
from sqlalchemy import func
from app.models.partido import Partido

class PartidoRepository:
    @staticmethod
    def puede_agregar_fecha(torneo_nombre: str, max_fechas: int) -> bool:
        # Cuenta la cantidad de fechas distintas ya jugadas en el torneo
        fechas_jugadas = db.session.query(Partido.fecha_numero).filter_by(torneo=torneo_nombre).distinct().count()
        return fechas_jugadas < max_fechas
    @staticmethod
    def crear(partido: Partido):
        db.session.add(partido)
        db.session.commit()
        return partido

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Partido).filter_by(id=id).first()

    @staticmethod
    def buscar(filtros: dict):
        q = db.session.query(Partido)
        if filtros.get('torneo'):
            # Emparejar por substring y sin sensibilidad a mayúsculas
            q = q.filter(Partido.torneo.ilike(f"%{filtros['torneo']}%"))
        if filtros.get('categoria'):
            # Emparejar por substring y sin sensibilidad a mayúsculas
            q = q.filter(Partido.categoria.ilike(f"%{filtros['categoria']}%"))
        if filtros.get('club_id'):
            cid = filtros['club_id']
            # Buscar partidos donde el club sea local o visitante
            q = q.filter((Partido.club_local_id == cid) | (Partido.club_visitante_id == cid))
        if filtros.get('fecha_numero'):
            q = q.filter(Partido.fecha_numero == filtros['fecha_numero'])
        # Filtros de estado (opcional)
        if filtros.get('estado'):
            q = q.filter(func.lower(Partido.estado) == filtros['estado'].lower())
        if filtros.get('estado_not'):
            q = q.filter(Partido.estado != filtros['estado_not'])
        return q.order_by(Partido.fecha_hora.nullslast()).all()

    @staticmethod
    def actualizar(partido: Partido):
        db.session.merge(partido)
        db.session.commit()
        return partido

    @staticmethod
    def eliminar(partido: Partido):
        db.session.delete(partido)
        db.session.commit()
