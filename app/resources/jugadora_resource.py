
from flask import Blueprint, request, jsonify
from app.models import Jugadora
from app.repositories.jugadora_repositorio import JugadoraRepository
from app.mappings.jugadora_mapping import JugadoraSchema

jugadora_bp = Blueprint('jugadora', __name__)
jugadora_schema = JugadoraSchema()
jugadoras_schema = JugadoraSchema(many=True)

@jugadora_bp.route('/jugadoras', methods=['POST'])
def crear_jugadora():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos incompletos'}), 400
    errors = jugadora_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    from app.services.jugadora_service import JugadoraService
    jugadora, error = JugadoraService.crear_jugadora(data)
    if error:
        return jsonify({'error': error}), 409
    return jsonify(jugadora_schema.dump(jugadora)), 201

@jugadora_bp.route('/jugadoras/<int:id>', methods=['GET'])
def obtener_jugadora(id):
    jugadora = JugadoraRepository.buscar_por_id(id)
    if not jugadora:
        return jsonify({'error': 'No encontrada'}), 404
    return jsonify(jugadora_schema.dump(jugadora))

@jugadora_bp.route('/jugadoras', methods=['GET'])
def obtener_jugadoras():
    club_id = request.args.get('club_id', type=int)
    equipo_id = request.args.get('equipo_id', type=int)
    if equipo_id:
        from app.repositories.equipo_repositorio import EquipoRepository
        equipo = EquipoRepository.buscar_por_id(equipo_id)
        if not equipo:
            return jsonify({'error': 'Equipo no encontrado'}), 404
        # Buscar jugadoras por club y categoría del equipo
        jugadoras = JugadoraRepository.buscar_por_club(equipo.club_id)
        # Filtrar por categoría si corresponde
        if equipo.categoria:
            jugadoras = [j for j in jugadoras if (j.categoria or '').lower() == (equipo.categoria or '').lower()]
    elif club_id:
        jugadoras = JugadoraRepository.buscar_por_club(club_id)
    else:
        jugadoras = JugadoraRepository.buscar_todas()
    return jsonify(jugadoras_schema.dump(jugadoras))

@jugadora_bp.route('/jugadoras/<int:id>', methods=['PUT'])
def actualizar_jugadora(id):
    data = request.get_json()
    jugadora = JugadoraRepository.buscar_por_id(id)
    if not jugadora:
        return jsonify({'error': 'No encontrada'}), 404
    errors = jugadora_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(jugadora, key, value)
    JugadoraRepository.actualizar_jugadora(jugadora)
    return jsonify(jugadora_schema.dump(jugadora))

@jugadora_bp.route('/jugadoras/<int:id>', methods=['DELETE'])
def borrar_jugadora(id):
    jugadora = JugadoraRepository.borrar_por_id(id)
    if not jugadora:
        return jsonify({'error': 'No encontrada'}), 404
    return jsonify({'resultado': 'Eliminada'})
