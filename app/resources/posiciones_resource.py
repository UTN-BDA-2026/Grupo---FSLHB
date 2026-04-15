from flask import Blueprint, request, jsonify
from app.services.posiciones_service import obtener_tabla_posiciones

posiciones_bp = Blueprint('posiciones', __name__)

@posiciones_bp.route('/posiciones', methods=['GET'])
def obtener_posiciones():
    torneo = request.args.get('torneo')
    division = request.args.get('division')
    fecha = request.args.get('fecha')
    bloque = request.args.get('bloque')
    # Puedes agregar validaciones aquí
    posiciones = obtener_tabla_posiciones(torneo, division, fecha, bloque)
    return jsonify(posiciones)
