from app.models.noticia import Noticia
from app import db

class NoticiaRepositorio:
    @staticmethod
    def obtener_todas(limit=None):
        q = Noticia.query.order_by(Noticia.fecha.desc())
        if limit is not None:
            try:
                # Asegurar entero positivo
                lim = int(limit)
                if lim > 0:
                    q = q.limit(lim)
            except (ValueError, TypeError):
                pass
        return q.all()

    @staticmethod
    def obtener_por_id(noticia_id):
        return Noticia.query.get(noticia_id)

    @staticmethod
    def crear_noticia(data):
        noticia = Noticia(**data)
        db.session.add(noticia)
        db.session.commit()
        return noticia

    @staticmethod
    def eliminar_noticia(noticia_id):
        noticia = Noticia.query.get(noticia_id)
        if noticia:
            db.session.delete(noticia)
            db.session.commit()
            return True
        return False
