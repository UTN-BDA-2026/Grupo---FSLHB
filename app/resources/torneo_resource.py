from flask import Blueprint, jsonify, request
torneo_bp = Blueprint('torneo', __name__)
from app.services.torneo_service import TorneoService

torneo_bp = Blueprint('torneo', __name__)

@torneo_bp.route('/torneo/seleccion', methods=['GET', 'POST', 'OPTIONS'])
def seleccion_torneos():
    if request.method == 'GET':
        torneos = TorneoService.obtener_torneos()
        return jsonify(torneos)
    elif request.method == 'POST':
        data = request.get_json()
        resultado = TorneoService.guardar_seleccion(data)
        return jsonify(resultado), 201
    elif request.method == 'OPTIONS':
        return '', 204
