from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService
from app.mappings.usuario_mapping import UsuarioSchema
from flask_login import login_user, logout_user, login_required
from app import require_admin, csrf

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


@usuario_bp.route('/admin/mesas-control', methods=['GET'])
@require_admin
def listar_mesas_control():
    """Devuelve los usuarios operadores (mesas de control) para el panel admin."""
    usuarios = UsuarioService.listar_operadores()
    data = UsuarioSchema(many=True).dump(usuarios)
    return jsonify(data), 200


@usuario_bp.route('/admin/mesas-control', methods=['POST'])
@csrf.exempt
@require_admin
def crear_mesa_control():
    """Crea un nuevo usuario de mesa de control."""
    payload = request.get_json() or {}
    try:
        usuario = UsuarioService.crear_operador_desde_payload(payload)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    data = UsuarioSchema().dump(usuario)
    return jsonify(data), 201


@usuario_bp.route('/admin/mesas-control/<int:usuario_id>', methods=['DELETE'])
@csrf.exempt
@require_admin
def eliminar_mesa_control(usuario_id: int):
    """Elimina un usuario de mesa de control por id."""
    ok = UsuarioService.eliminar_usuario(usuario_id)
    if not ok:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'ok': True}), 200


@usuario_bp.route('/admin/mesas-control/<int:usuario_id>', methods=['PUT'])
@csrf.exempt
@require_admin
def actualizar_mesa_control(usuario_id: int):
    """Actualiza username y/o contraseña de una mesa de control."""
    payload = request.get_json() or {}
    try:
        usuario = UsuarioService.actualizar_usuario_operador(usuario_id, payload)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    data = UsuarioSchema().dump(usuario)
    return jsonify(data), 200
