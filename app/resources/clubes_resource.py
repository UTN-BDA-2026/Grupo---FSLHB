from flask import Blueprint, jsonify
from app.models.club import Club

clubes_bp = Blueprint('clubes', __name__, url_prefix='/api/clubes')

@clubes_bp.route('/', methods=['GET'])
def listar_clubes():
    clubes = Club.query.all()
    return jsonify([club.to_dict() for club in clubes])
