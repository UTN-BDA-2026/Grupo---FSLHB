from app.repositories import ResultadoRepository

class ResultadoService:

    @staticmethod
    def agregar_resultado(resultado):
        ResultadoRepository.agregar_resultado(resultado)

    @staticmethod
    def obtener_resultados():
        return ResultadoRepository.obtener_resultados()

    @staticmethod
    def obtener_resultado_por_id(resultado_id):
        return ResultadoRepository.obtener_resultado_por_id(resultado_id)

    @staticmethod
    def actualizar_resultado(resultado):
        ResultadoRepository.actualizar_resultado(resultado)

    @staticmethod
    def eliminar_resultado(resultado):
        ResultadoRepository.eliminar_resultado(resultado)
