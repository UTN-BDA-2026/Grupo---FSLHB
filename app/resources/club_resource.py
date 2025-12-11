
from flask import Blueprint, request, jsonify
from app.models import Club
from app.services.club_service import ClubService
from app.services.arbitro_service import ArbitroService
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

@clubs_bp.route('/clubs/<int:id>/arbitro', methods=['PUT'])
def asignar_arbitro_club(id):
    data = request.get_json() or {}
    # Permite dos modos:
    # 1) Asignar existente: { arbitro_id }
    # 2) Crear y asignar: { nombre, apellido, dni }
    arb_id = data.get('arbitro_id')
    if not arb_id:
        # Crear uno nuevo
        try:
            nuevo = ArbitroService.crear({
                'nombre': data.get('nombre', ''),
                'apellido': data.get('apellido', ''),
                'dni': data.get('dni', ''),
            })
            arb_id = nuevo.id
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'No se pudo crear el árbitro', 'detail': str(e)}), 500
    club = ClubService.asignar_arbitro(id, int(arb_id))
    if not club:
        return jsonify({'error': 'Club no encontrado'}), 404
    return jsonify({'ok': True, 'arbitro_id': club.arbitro_id})
