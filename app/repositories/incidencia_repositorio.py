from app import db
from app.models.incidencia import Incidencia

class IncidenciaRepository:
    @staticmethod
    def crear(inc: Incidencia):
        db.session.add(inc)
        db.session.commit()
        return inc

    @staticmethod
    def listar_por_partido(partido_id: int):
        return db.session.query(Incidencia).filter_by(partido_id=partido_id).order_by(Incidencia.created_at.asc()).all()

    @staticmethod
    def listar_goles_por_partidos(partido_ids: list[int]):
        if not partido_ids:
            return []
        return (
            db.session.query(Incidencia)
            .filter(Incidencia.partido_id.in_(partido_ids), Incidencia.tipo == 'gol')
            .all()
        )

    @staticmethod
    def max_created_at_por_partido(partido_ids: list[int]):
        """Devuelve dict {partido_id: max_created_at} para un conjunto de partidos."""
        if not partido_ids:
            return {}
        from sqlalchemy import func
        rows = (
            db.session.query(Incidencia.partido_id, func.max(Incidencia.created_at))
            .filter(Incidencia.partido_id.in_(partido_ids))
            .group_by(Incidencia.partido_id)
            .all()
        )
        return {pid: max_dt for pid, max_dt in rows}

    @staticmethod
    def ranking_resumen(torneo: str | None, categoria: str | None, fecha_hasta: int | None = None):
        """Devuelve incidencias (gol y tarjetas) de partidos filtrados.
        Retorna lista de objetos Incidencia para simplificar el consumo aguas arriba."""
        from app.models.partido import Partido  # import local para evitar ciclos
        q = db.session.query(Incidencia).join(Partido, Partido.id == Incidencia.partido_id)
        if torneo:
            # Permitir coincidencia parcial y sin sensibilidad a mayúsculas
            q = q.filter(Partido.torneo.ilike(f"%{torneo}%"))
        if categoria:
            # Permitir coincidencia parcial y sin sensibilidad a mayúsculas
            q = q.filter(Partido.categoria.ilike(f"%{categoria}%"))
        if fecha_hasta is not None:
            try:
                fh = int(fecha_hasta)
                q = q.filter((Partido.fecha_numero == None) | (Partido.fecha_numero <= fh))
            except Exception:
                pass
        return q.all()
