from datetime import date, datetime

from bson import ObjectId
from flask import Blueprint, jsonify, request
from app.services.noticia_service import NoticiaService
from app import csrf, require_admin

noticia_bp = Blueprint('noticia', __name__, url_prefix='/api/noticias')


def _to_jsonable(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    return value


def _jsonify_doc(doc: dict | None):
    if doc is None:
        return None
    return _to_jsonable(doc)

@noticia_bp.route('/', methods=['GET'])
def listar_noticias():
    limit = request.args.get('limit', type=int)
    noticias = NoticiaService.listar_noticias(limit=limit)
    return jsonify([_jsonify_doc(n) for n in noticias])

@noticia_bp.route('/<noticia_id>', methods=['GET'])
def obtener_noticia(noticia_id):
    noticia = NoticiaService.obtener_noticia(noticia_id)
    if noticia:
        return jsonify(_jsonify_doc(noticia))
    return jsonify({'error': 'Noticia no encontrada'}), 404

@noticia_bp.route('/', methods=['POST'])
@csrf.exempt
@require_admin
def crear_noticia():
    data = request.get_json() or {}
    noticia = NoticiaService.crear_noticia(data)
    return jsonify(_jsonify_doc(noticia)), 201


@noticia_bp.route('/<noticia_id>', methods=['DELETE'])
@csrf.exempt
@require_admin
def eliminar_noticia(noticia_id):
    ok = NoticiaService.eliminar_noticia(noticia_id)
    if ok:
        return jsonify({'msg': 'Noticia eliminada'})
    return jsonify({'error': 'No encontrada'}), 404
