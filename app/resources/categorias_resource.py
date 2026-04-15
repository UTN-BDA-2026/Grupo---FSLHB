from flask import Blueprint, jsonify, request
from app import db
from app.models.jugadora import Jugadora

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/api/equipos-categorias', methods=['GET'])
def equipos_categorias_api():
    club_id = request.args.get('club_id', type=int)
    query = db.session.query(
        Jugadora.rama,
        Jugadora.division,
        db.func.count(Jugadora.id).label('jugadores')
    )
    if club_id:
        query = query.filter(Jugadora.club_id == club_id)
    query = query.group_by(Jugadora.rama, Jugadora.division)
    resultados = query.all()
    data = [
        {
            'rama': r or '',
            'division': d or '',
            'bloque': '',  # Si tienes bloque, cámbialo aquí
            'jugadores': j
        }
        for r, d, j in resultados
    ]
    return jsonify(data)
