from app import db
from app.models import Resultado

class ResultadoRepository:

    @staticmethod
    def agregar_resultado(resultado: Resultado):
        db.session.add(resultado)
        db.session.commit()

    @staticmethod
    def obtener_resultados():
        return Resultado.query.all()

    @staticmethod
    def obtener_resultado_por_id(resultado_id: int):
        return Resultado.query.get(resultado_id)

    @staticmethod
    def actualizar_resultado(resultado: Resultado):
        db.session.commit()

    @staticmethod
    def eliminar_resultado(resultado: Resultado):
        db.session.delete(resultado)
        db.session.commit()
