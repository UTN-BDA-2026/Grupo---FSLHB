
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Jugadora
from app.repositories.jugadora_repositorio import JugadoraRepository
from app.mappings.jugadora_mapping import JugadoraSchema
from app import db

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
            def norm(s):
                return (s or '').strip().lower().replace('_',' ').replace('\s+', ' ')
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
    from app.models import Club
    rows = (
        db.session.query(Jugadora.club_id, Club.nombre.label('club_nombre'), Jugadora.categoria, db.func.count(Jugadora.id).label('cantidad'))
        .join(Club, Club.id == Jugadora.club_id)
        .group_by(Jugadora.club_id, Club.nombre, Jugadora.categoria)
        .order_by(Club.nombre.asc(), Jugadora.categoria.asc())
        .all()
    )
    data = [
        {
            'club_id': r.club_id,
            'club_nombre': r.club_nombre,
            'categoria': r.categoria,
            'cantidad': r.cantidad
        } for r in rows
    ]
    return jsonify(data), 200

@jugadora_bp.route('/jugadoras/<int:id>', methods=['PUT'])
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

@jugadora_bp.route('/jugadoras/<int:id>', methods=['DELETE'])
@login_required
def borrar_jugadora(id):
    # Verificar permisos: solo usuarios con club_id
    if getattr(current_user, 'club_id', None) is None:
        return jsonify({'error': 'No autorizado'}), 403
    jugadora = JugadoraRepository.borrar_por_id(id)
    if not jugadora:
        return jsonify({'error': 'No encontrada'}), 404
    return jsonify({'resultado': 'Eliminada'})
