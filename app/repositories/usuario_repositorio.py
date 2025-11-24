from app.models.usuario import Usuario

class UsuarioRepositorio:
    @staticmethod
    def buscar_por_username(username):
        return Usuario.query.filter_by(username=username).first()

    @staticmethod
    def buscar_por_id(user_id):
        return Usuario.query.get(int(user_id))
