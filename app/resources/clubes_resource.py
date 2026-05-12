from flask import Blueprint, jsonify
from app.repositories.club_repositorio import ClubRepository

clubes_bp = Blueprint('clubes', __name__, url_prefix='/api/clubes')

@clubes_bp.route('/', methods=['GET'])
def listar_clubes():
    clubes = ClubRepository.buscar_todos()
    result = []
    for club in clubes:
        d = club.to_dict()
        d['_id'] = str(d.get('_id', ''))
        result.append(d)
    return jsonify(result)
