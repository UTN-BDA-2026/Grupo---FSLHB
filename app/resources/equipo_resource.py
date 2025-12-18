from flask import Blueprint, request, jsonify
from app.models.equipo import Equipo
from app.repositories.equipo_repositorio import EquipoRepository
from app.mappings.equipo_mapping import EquipoSchema
from app import require_admin, csrf

equipo_bp = Blueprint('equipo', __name__)
equipo_schema = EquipoSchema()
equipos_schema = EquipoSchema(many=True)

@equipo_bp.route('/equipos', methods=['POST'])
def crear_equipo():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos incompletos'}), 400
    errors = equipo_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    equipo = equipo_schema.load(data)
    EquipoRepository.crear(equipo)
    return jsonify(equipo_schema.dump(equipo)), 201

@equipo_bp.route('/equipos', methods=['GET'])
def obtener_equipos():
    club_id = request.args.get('club_id', type=int)
    if club_id:
        equipos = EquipoRepository.buscar_por_club(club_id)
    else:
        equipos = EquipoRepository.buscar_todos()
    return jsonify(equipos_schema.dump(equipos))

@equipo_bp.route('/equipos/<int:id>', methods=['PUT'])
def actualizar_equipo(id):
    data = request.get_json()
    equipo = EquipoRepository.buscar_por_id(id)
    if not equipo:
        return jsonify({'error': 'No encontrado'}), 404
    errors = equipo_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(equipo, key, value)
    EquipoRepository.actualizar_equipo(equipo)
    return jsonify(equipo_schema.dump(equipo))

@equipo_bp.route('/equipos/<int:id>', methods=['DELETE'])
def borrar_equipo(id):
    equipo = EquipoRepository.borrar_por_id(id)
    if not equipo:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify({'resultado': 'Eliminado'})


@equipo_bp.route('/admin/equipos/<int:id>/categoria', methods=['PUT'])
@csrf.exempt
@require_admin
def actualizar_categoria_equipo_admin(id: int):
    data = request.get_json() or {}
    nueva_cat = (data.get('categoria') or '').strip()
    if not nueva_cat:
        return jsonify({'error': 'La categoría es obligatoria'}), 400
    equipo = EquipoRepository.buscar_por_id(id)
    if not equipo:
        return jsonify({'error': 'No encontrado'}), 404
    equipo.categoria = nueva_cat
    EquipoRepository.actualizar_equipo(equipo)
    return jsonify({'id': equipo.id, 'categoria': equipo.categoria}), 200
