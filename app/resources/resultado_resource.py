from flask import Blueprint, request, jsonify
from app.mappings.resultado_mapping import ResultadoSchema
from app.models.resultado import Resultado
from app.repositories.resultado_repositorio import ResultadoRepository

resultado_bp = Blueprint('resultado', __name__)
resultado_schema = ResultadoSchema()

@resultado_bp.route('/resultados', methods=['POST'])
def agregar_resultado():
    datos = request.json
    resultado = resultado_schema.load(datos)
    ResultadoRepository.agregar_resultado(resultado)
    return resultado_schema.dump(resultado), 201

@resultado_bp.route('/resultados', methods=['GET'])
def obtener_resultados():
    resultados = ResultadoRepository.obtener_resultados()
    return resultado_schema.dump(resultados, many=True)

@resultado_bp.route('/resultados/<int:resultado_id>', methods=['GET'])
def obtener_resultado_por_id(resultado_id):
    resultado = ResultadoRepository.obtener_resultado_por_id(resultado_id)
    if not resultado:
        return jsonify({'mensaje': 'Resultado no encontrado'}), 404
    return resultado_schema.dump(resultado)

@resultado_bp.route('/resultados/<int:resultado_id>', methods=['PUT'])
def actualizar_resultado(resultado_id):
    resultado = ResultadoRepository.obtener_resultado_por_id(resultado_id)
    if not resultado:
        return jsonify({'mensaje': 'Resultado no encontrado'}), 404
    datos = request.json
    resultado = resultado_schema.load(datos, instance=resultado)
    ResultadoRepository.actualizar_resultado(resultado)
    return resultado_schema.dump(resultado)

@resultado_bp.route('/resultados/<int:resultado_id>', methods=['DELETE'])
def eliminar_resultado(resultado_id):
    resultado = ResultadoRepository.obtener_resultado_por_id(resultado_id)
    if not resultado:
        return jsonify({'mensaje': 'Resultado no encontrado'}), 404
    ResultadoRepository.eliminar_resultado(resultado)
    return jsonify({'mensaje': 'Resultado eliminado'}), 204
