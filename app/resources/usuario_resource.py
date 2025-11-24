from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService
from app.mappings.usuario_mapping import UsuarioSchema
from flask_login import login_user, logout_user, login_required

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    usuario = UsuarioService.autenticar(username, password)
    if usuario:
        login_user(usuario)
        return UsuarioSchema().dump(usuario), 200
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401


@usuario_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'ok': True}), 200
