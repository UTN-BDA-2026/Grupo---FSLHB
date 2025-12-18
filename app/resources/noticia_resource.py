from flask import Blueprint, jsonify, request
from app.services.noticia_service import NoticiaService
from app import csrf, require_admin

noticia_bp = Blueprint('noticia', __name__, url_prefix='/api/noticias')

@noticia_bp.route('/', methods=['GET'])
def listar_noticias():
    limit = request.args.get('limit', type=int)
    noticias = NoticiaService.listar_noticias(limit=limit)
    return jsonify(noticias)

@noticia_bp.route('/<int:noticia_id>', methods=['GET'])
def obtener_noticia(noticia_id):
    noticia = NoticiaService.obtener_noticia(noticia_id)
    if noticia:
        return jsonify(noticia)
    return jsonify({'error': 'Noticia no encontrada'}), 404

@noticia_bp.route('/', methods=['POST'])
@csrf.exempt
@require_admin
def crear_noticia():
    data = request.get_json() or {}
    noticia = NoticiaService.crear_noticia(data)
    return jsonify(noticia), 201


@noticia_bp.route('/<int:noticia_id>', methods=['DELETE'])
@csrf.exempt
@require_admin
def eliminar_noticia(noticia_id):
    ok = NoticiaService.eliminar_noticia(noticia_id)
    if ok:
        return jsonify({'msg': 'Noticia eliminada'})
    return jsonify({'error': 'No encontrada'}), 404
