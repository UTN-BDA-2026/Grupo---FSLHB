
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Club
from app.services.club_service import ClubService
from app.mappings.club_mapping import ClubMapping
from app import require_admin

clubs_bp = Blueprint('clubs', __name__)
club_schema = ClubMapping()

@clubs_bp.route('/clubs', methods=['POST'])
@require_admin
def crear():
    data = request.get_json() or {}
    try:
        club_data = club_schema.load(data)
    except ValidationError as error:
        return jsonify({'error': 'Datos inválidos', 'detail': error.messages}), 400

    club = Club.from_dict(club_data)
    club = ClubService.crear(club)
    return jsonify(club_schema.dump(club)), 201

@clubs_bp.route('/clubs', methods=['GET'])
def buscar_todos():
    clubs = ClubService.buscar_todos()
    return club_schema.dump(clubs, many=True), 200

@clubs_bp.route('/clubs/<id>', methods=['GET'])
def buscar_por_id(id):
    club = ClubService.buscar_por_id(id)
    if not club:
        return jsonify({'error': 'Club no encontrado'}), 404
    return club_schema.dump(club), 200

@clubs_bp.route('/clubs/<id>', methods=['PUT'])
@require_admin
def actualizar(id):
    club = ClubService.buscar_por_id(id)
    if not club:
        return jsonify({'error': 'Club no encontrado'}), 404

    data = request.get_json() or {}
    try:
        club_data = club_schema.load(data)
    except ValidationError as error:
        return jsonify({'error': 'Datos inválidos', 'detail': error.messages}), 400

    for field, value in club_data.items():
        if field != '_id':
            setattr(club, field, value)

    club = ClubService.actualizar(club)
    return jsonify(club_schema.dump(club)), 200

@clubs_bp.route('/clubs/<id>', methods=['DELETE'])
@require_admin
def borrar_por_id(id):
    club = ClubService.borrar_por_id(id)
    if not club:
        return jsonify({'error': 'Club no encontrado'}), 404
    return jsonify({'message': 'Club borrado exitosamente'}), 200

@clubs_bp.route('/clubs/<id>/arbitro', methods=['GET'])
def obtener_arbitro_club(id):
    arb = ClubService.obtener_arbitro(id)
    if not arb:
        return jsonify({}), 200
    return jsonify({'id': arb.id, 'nombre': arb.nombre, 'apellido': arb.apellido, 'dni': arb.dni})
