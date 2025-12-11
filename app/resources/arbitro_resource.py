from flask import Blueprint, request, jsonify
from app.services.arbitro_service import ArbitroService
from app import require_admin, csrf

arbitro_bp = Blueprint('arbitros', __name__, url_prefix='/arbitros')


@arbitro_bp.route('/', methods=['GET'])
def listar():
    lista = ArbitroService.listar()
    return jsonify([
        {
            'id': a.id,
            'nombre': a.nombre,
            'apellido': a.apellido,
            'dni': a.dni,
            'created_at': a.created_at.isoformat() if a.created_at else None,
        } for a in lista
    ])


@arbitro_bp.route('/<int:id>', methods=['GET'])
def obtener(id: int):
    a = ArbitroService.obtener(id)
    if not a:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify({'id': a.id, 'nombre': a.nombre, 'apellido': a.apellido, 'dni': a.dni})


@arbitro_bp.route('/', methods=['POST'])
@csrf.exempt
@require_admin
def crear():
    data = request.get_json() or {}
    try:
        a = ArbitroService.crear(data)
        return jsonify({'id': a.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'No se pudo crear', 'detail': str(e)}), 500


@arbitro_bp.route('/<int:id>', methods=['PUT'])
@csrf.exempt
@require_admin
def actualizar(id: int):
    data = request.get_json() or {}
    try:
        a = ArbitroService.actualizar(id, data)
        if not a:
            return jsonify({'error': 'No encontrado'}), 404
        return jsonify({'id': a.id, 'nombre': a.nombre, 'apellido': a.apellido, 'dni': a.dni})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'No se pudo actualizar', 'detail': str(e)}), 500


@arbitro_bp.route('/<int:id>', methods=['DELETE'])
@csrf.exempt
@require_admin
def eliminar(id: int):
    ok = ArbitroService.eliminar(id)
    if not ok:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify({'mensaje': 'Eliminado'}), 200
