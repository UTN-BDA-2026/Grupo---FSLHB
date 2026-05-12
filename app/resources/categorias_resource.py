from flask import Blueprint, jsonify, request
from app.extensions import mongo

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/api/equipos-categorias', methods=['GET'])
def equipos_categorias_api():
    club_id = request.args.get('club_id')

    pipeline = []
    if club_id:
        from bson import ObjectId
        pipeline.append({'$match': {'club_id': ObjectId(club_id)}})
    pipeline.extend([
        {'$group': {
            '_id': {'categoria': '$categoria'},
            'jugadores': {'$sum': 1}
        }},
        {'$sort': {'_id.categoria': 1}}
    ])

    results = mongo.db.jugadoras.aggregate(pipeline)
    data = [
        {
            'rama': '',
            'division': '',
            'categoria': r['_id'].get('categoria') or '',
            'bloque': '',
            'jugadores': r['jugadores']
        }
        for r in results
    ]
    return jsonify(data)
