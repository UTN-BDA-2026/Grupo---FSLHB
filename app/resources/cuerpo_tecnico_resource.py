from flask import Blueprint, request, jsonify
from app.services.cuerpo_tecnico_service import CuerpoTecnicoService
from app.models.cuerpo_tecnico import CuerpoTecnico

bp_cuerpo_tecnico = Blueprint('cuerpo_tecnico', __name__, url_prefix='/cuerpo-tecnico')

@bp_cuerpo_tecnico.route('/', methods=['GET'])
def listar():
    club_id = request.args.get('club_id', type=int)
    rows = CuerpoTecnicoService.listar(club_id)
    return jsonify([
        {
            'id': r.id,
            'club_id': r.club_id,
            'nombre': r.nombre,
            'apellido': r.apellido,
            'dni': r.dni,
            'rol': r.rol,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in rows
    ])

@bp_cuerpo_tecnico.route('/<int:id>', methods=['GET'])
def obtener(id):
    ct = CuerpoTecnico.query.get(id)
    if not ct:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify({
        'id': ct.id,
        'club_id': ct.club_id,
        'nombre': ct.nombre,
        'apellido': ct.apellido,
        'dni': ct.dni,
        'rol': ct.rol,
        'created_at': ct.created_at.isoformat() if ct.created_at else None
    })

@bp_cuerpo_tecnico.route('/', methods=['POST'])
def crear():
    data = request.json or {}
    required = ['club_id', 'nombre', 'apellido', 'dni', 'rol']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({
            'error': 'Faltan campos requeridos',
            'missing': missing
        }), 400
    try:
        ct = CuerpoTecnicoService.crear(data)
        return jsonify({'id': ct.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Loggear e si se desea, pero devolver JSON
        return jsonify({'error': 'No se pudo crear', 'detail': str(e)}), 500

@bp_cuerpo_tecnico.route('/<int:id>', methods=['PUT'])
def actualizar(id):
    data = request.json
    try:
        ct = CuerpoTecnicoService.actualizar(id, data)
        if ct:
            return jsonify({'ok': True})
        return jsonify({'error': 'No encontrado'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp_cuerpo_tecnico.route('/<int:id>', methods=['DELETE'])
def eliminar(id):
    ok = CuerpoTecnicoService.eliminar(id)
    return jsonify({'ok': ok})
