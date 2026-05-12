from bson import ObjectId
from app.extensions import mongo
from app.models.resultado import Resultado


class ResultadoRepository:
    @staticmethod
    def _col():
        return mongo.db.resultados

    @staticmethod
    def agregar_resultado(resultado):
        doc = resultado.to_dict()
        doc.pop('_id', None)
        result = ResultadoRepository._col().insert_one(doc)
        resultado._id = result.inserted_id
        return resultado

    @staticmethod
    def obtener_resultados():
        docs = ResultadoRepository._col().find()
        return [Resultado.from_dict(d) for d in docs]

    @staticmethod
    def obtener_resultado_por_id(resultado_id):
        doc = ResultadoRepository._col().find_one({'_id': ObjectId(resultado_id)})
        return Resultado.from_dict(doc)

    @staticmethod
    def actualizar_resultado(resultado):
        doc = resultado.to_dict()
        doc.pop('_id', None)
        ResultadoRepository._col().update_one(
            {'_id': ObjectId(resultado._id)}, {'$set': doc}
        )

    @staticmethod
    def eliminar_resultado(resultado):
        ResultadoRepository._col().delete_one({'_id': ObjectId(resultado._id)})
