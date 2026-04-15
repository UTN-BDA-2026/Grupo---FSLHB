
from flask import Blueprint, request, jsonify
from app.models import Club
from app.services.club_service import ClubService
from app.mappings.club_mapping import ClubMapping
from app import require_admin

clubs_bp = Blueprint('clubs', __name__)
club_schema = ClubMapping()

@clubs_bp.route('/clubs', methods=['POST'])
@require_admin
def crear():
    club = club_schema.load(request.get_json())
    ClubService.crear(club)
    return club_schema.dump(club), 201

@clubs_bp.route('/clubs', methods=['GET'])
def buscar_todos():
    clubs = ClubService.buscar_todos()
    return club_schema.dump(clubs, many=True), 200

@clubs_bp.route('/clubs/<int:id>', methods=['GET'])
def buscar_por_id(id):
    club = ClubService.buscar_por_id(id)
    if not club:
        return jsonify({'error': 'Club no encontrado'}), 404
    return club_schema.dump(club), 200

@clubs_bp.route('/clubs/<int:id>', methods=['PUT'])
@require_admin
def actualizar(id):
    club = ClubService.buscar_por_id(id)
    if not club:
        return jsonify({'error': 'Club no encontrado'}), 404
    data = club_schema.load(request.get_json())
    club.nombre = data.nombre
    ClubService.actualizar(club)
    return club_schema.dump(club), 200

@clubs_bp.route('/clubs/<int:id>', methods=['DELETE'])
@require_admin
def borrar_por_id(id):
    club = ClubService.borrar_por_id(id)
    if not club:
        return jsonify({'error': 'Club no encontrado'}), 404
    return jsonify({'message': 'Club borrado exitosamente'}), 200

@clubs_bp.route('/clubs/<int:id>/arbitro', methods=['GET'])
def obtener_arbitro_club(id):
    arb = ClubService.obtener_arbitro(id)
    if not arb:
        return jsonify({}), 200
    return jsonify({'id': arb.id, 'nombre': arb.nombre, 'apellido': arb.apellido, 'dni': arb.dni})
