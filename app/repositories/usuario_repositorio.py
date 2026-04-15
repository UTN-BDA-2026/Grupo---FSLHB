from app.models.usuario import Usuario
from sqlalchemy import or_

class UsuarioRepositorio:
    @staticmethod
    def buscar_por_username(username):
        return Usuario.query.filter_by(username=username).first()

    @staticmethod
    def buscar_por_id(user_id):
        return Usuario.query.get(int(user_id))

    @staticmethod
    def listar_operadores():
        """Devuelve los usuarios que actúan como mesas de control.

        Se consideran mesas de control aquellos usuarios que sean operadores
        generales o tengan permisos especiales de incidencias o precarga.
        """
        return Usuario.query.filter(
            or_(
                Usuario.is_operador.is_(True),
                Usuario.puede_cargar_incidencias.is_(True),
                Usuario.puede_precargar_equipos.is_(True),
            )
        ).all()
