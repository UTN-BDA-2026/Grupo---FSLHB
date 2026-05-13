
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Jugadora
from app.repositories.jugadora_repositorio import JugadoraRepository
from app.mappings.jugadora_mapping import JugadoraSchema
from app.extensions import mongo
from bson import ObjectId

jugadora_bp = Blueprint('jugadora', __name__)
jugadora_schema = JugadoraSchema()
jugadoras_schema = JugadoraSchema(many=True)

@jugadora_bp.route('/jugadoras', methods=['POST'])
@login_required
def crear_jugadora():
    # Solo clubes (usuarios con club_id) pueden crear
    if getattr(current_user, 'club_id', None) is None:
        return jsonify({'error': 'No autorizado'}), 403
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

@jugadora_bp.route('/jugadoras/<id>', methods=['GET'])
def obtener_jugadora(id):
    jugadora = JugadoraRepository.buscar_por_id(id)
    if not jugadora:
        return jsonify({'error': 'No encontrada'}), 404
    return jsonify(jugadora_schema.dump(jugadora))

@jugadora_bp.route('/jugadoras', methods=['GET'])
def obtener_jugadoras():
    def _clean(v):
        if v is None:
            return None
        s = str(v).strip()
        if not s or s.lower() in ('null', 'undefined', 'none'):
            return None
        return s

    club_id = _clean(request.args.get('club_id'))
    equipo_id = _clean(request.args.get('equipo_id'))
    if equipo_id:
        from app.repositories.equipo_repositorio import EquipoRepository
        equipo = EquipoRepository.buscar_por_id(equipo_id)
        if not equipo:
            return jsonify({'error': 'Equipo no encontrado'}), 404
        # Buscar jugadoras por club y categoría del equipo
        jugadoras = JugadoraRepository.buscar_por_club(equipo.club_id)
        # Filtrar por categoría si corresponde
        if equipo.categoria:
            def norm(s):
                return (s or '').strip().lower().replace('_',' ')
            ec = norm(equipo.categoria)
            jugadoras = [j for j in jugadoras if norm(j.categoria) == ec]
    elif club_id:
        jugadoras = JugadoraRepository.buscar_por_club(club_id)
    else:
        jugadoras = JugadoraRepository.buscar_todas()
    return jsonify(jugadoras_schema.dump(jugadoras))

@jugadora_bp.route('/jugadoras/resumen', methods=['GET'])
def resumen_jugadoras():
    """Devuelve un resumen de cantidad de jugadoras por club y categoría para depuración."""
    pipeline = [
        {'$group': {
            '_id': {'club_id': '$club_id', 'categoria': '$categoria'},
            'cantidad': {'$sum': 1}
        }},
        {'$sort': {'_id.club_id': 1, '_id.categoria': 1}}
    ]
    results = list(mongo.db.jugadoras.aggregate(pipeline))

    # Obtener nombres de clubes
    club_ids = list(set(r['_id']['club_id'] for r in results if r['_id'].get('club_id')))
    clubes = {d['_id']: d['nombre'] for d in mongo.db.clubes.find({'_id': {'$in': club_ids}}, {'nombre': 1})}

    data = [
        {
            'club_id': str(r['_id']['club_id']),
            'club_nombre': clubes.get(r['_id']['club_id'], ''),
            'categoria': r['_id'].get('categoria') or '',
            'cantidad': r['cantidad']
        } for r in results
    ]
    return jsonify(data), 200

@jugadora_bp.route('/jugadoras/<id>', methods=['PUT'])
@login_required
def actualizar_jugadora(id):
    if getattr(current_user, 'club_id', None) is None:
        return jsonify({'error': 'No autorizado'}), 403
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

@jugadora_bp.route('/jugadoras/<id>', methods=['DELETE'])
@login_required
def borrar_jugadora(id):
    # Verificar permisos: solo usuarios con club_id
    if getattr(current_user, 'club_id', None) is None:
        return jsonify({'error': 'No autorizado'}), 403
    jugadora = JugadoraRepository.borrar_por_id(id)
    if not jugadora:
        return jsonify({'error': 'No encontrada'}), 404
    return jsonify({'resultado': 'Eliminada'})
