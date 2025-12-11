from flask import Blueprint, jsonify, request
from app.services.torneo_service import TorneoService
from app import require_admin, csrf

torneo_bp = Blueprint('torneo', __name__)


@torneo_bp.route('/torneo/seleccion', methods=['GET', 'POST', 'OPTIONS'])
def seleccion_torneos():
    if request.method == 'GET':
        torneos = TorneoService.obtener_torneos()
        return jsonify(torneos)
    elif request.method == 'POST':
        data = request.get_json()
        resultado = TorneoService.guardar_seleccion(data)
        return jsonify(resultado), 201
    elif request.method == 'OPTIONS':
        return '', 204


@torneo_bp.route('/admin/torneos', methods=['GET'])
@require_admin
def listar_torneos_admin():
    torneos = TorneoService.obtener_torneos()
    return jsonify(torneos), 200


@torneo_bp.route('/admin/torneos', methods=['POST'])
@csrf.exempt
@require_admin
def crear_torneo_admin():
    data = request.get_json() or {}
    nombre = (data.get('nombre') or '').strip()
    max_fechas = data.get('max_fechas')
    if not nombre:
        return jsonify({'error': 'El nombre del torneo es obligatorio'}), 400
    try:
        max_fechas_int = int(max_fechas)
    except (TypeError, ValueError):
        return jsonify({'error': 'max_fechas debe ser un número entero'}), 400
    if max_fechas_int <= 0:
        return jsonify({'error': 'max_fechas debe ser mayor a cero'}), 400
    try:
        torneo = TorneoService.crear_torneo(nombre, max_fechas_int)
    except Exception as exc:
        return jsonify({'error': 'No se pudo crear el torneo', 'detail': str(exc)}), 500
    return jsonify(torneo), 201


@torneo_bp.route('/admin/torneos/<int:torneo_id>', methods=['PUT'])
@csrf.exempt
@require_admin
def actualizar_torneo_admin(torneo_id: int):
    data = request.get_json() or {}
    nombre = (data.get('nombre') or '').strip()
    max_fechas = data.get('max_fechas')
    if not nombre:
        return jsonify({'error': 'El nombre del torneo es obligatorio'}), 400
    try:
        max_fechas_int = int(max_fechas)
    except (TypeError, ValueError):
        return jsonify({'error': 'max_fechas debe ser un número entero'}), 400
    if max_fechas_int <= 0:
        return jsonify({'error': 'max_fechas debe ser mayor a cero'}), 400
    torneo = TorneoService.actualizar_torneo(torneo_id, nombre, max_fechas_int)
    if not torneo:
        return jsonify({'error': 'Torneo no encontrado'}), 404
    return jsonify(torneo), 200


@torneo_bp.route('/admin/torneos/<int:torneo_id>', methods=['DELETE'])
@csrf.exempt
@require_admin
def eliminar_torneo_admin(torneo_id: int):
    ok = TorneoService.eliminar_torneo(torneo_id)
    if not ok:
        return jsonify({'error': 'Torneo no encontrado'}), 404
    return jsonify({'ok': True}), 200
