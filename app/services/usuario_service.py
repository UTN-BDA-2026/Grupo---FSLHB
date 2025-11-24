from app.repositories.usuario_repositorio import UsuarioRepositorio
from werkzeug.security import check_password_hash, generate_password_hash
import re

class UsuarioService:
    @staticmethod
    def autenticar(username, password):
        usuario = UsuarioRepositorio.buscar_por_username(username)
        if usuario and check_password_hash(usuario.password, password):
            return usuario
        return None

    @staticmethod
    def validar_password(password: str) -> tuple[bool, str | None]:
        """Reglas mínimas: >= 8 chars, 1 mayúscula, 1 minúscula, 1 dígito."""
        if not password or len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        if not re.search(r"[A-Z]", password):
            return False, "Debe incluir al menos una letra mayúscula."
        if not re.search(r"[a-z]", password):
            return False, "Debe incluir al menos una letra minúscula."
        if not re.search(r"\d", password):
            return False, "Debe incluir al menos un dígito."
        return True, None

    @staticmethod
    def hashear_password(password: str) -> str:
        """Usa el algoritmo por defecto de Werkzeug (PBKDF2-SHA256 con sal)."""
        return generate_password_hash(password)
