from app.repositories.noticia_repositorio import NoticiaRepositorio

class NoticiaService:
    @staticmethod
    def listar_noticias(limit=None):
        noticias = NoticiaRepositorio.obtener_todas(limit=limit)
        return [n.to_dict() for n in noticias]

    @staticmethod
    def obtener_noticia(noticia_id):
        noticia = NoticiaRepositorio.obtener_por_id(noticia_id)
        return noticia.to_dict() if noticia else None

    @staticmethod
    def crear_noticia(data):
        noticia = NoticiaRepositorio.crear_noticia(data)
        return noticia.to_dict()

    @staticmethod
    def eliminar_noticia(noticia_id):
        return NoticiaRepositorio.eliminar_noticia(noticia_id)
