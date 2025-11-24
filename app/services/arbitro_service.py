from app.repositories.arbitro_repositorio import ArbitroRepositorio


class ArbitroService:
    @staticmethod
    def crear(data: dict):
        required = ['nombre', 'apellido', 'dni']
        missing = [k for k in required if not data.get(k)]
        if missing:
            raise ValueError('Faltan campos requeridos: ' + ', '.join(missing))
        return ArbitroRepositorio.crear(data)

    @staticmethod
    def obtener(id: int):
        return ArbitroRepositorio.obtener(id)

    @staticmethod
    def listar():
        return ArbitroRepositorio.listar()

    @staticmethod
    def eliminar(id: int) -> bool:
        return ArbitroRepositorio.eliminar(id)
