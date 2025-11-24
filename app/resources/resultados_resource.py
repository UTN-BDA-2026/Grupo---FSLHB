from flask import Blueprint, request, jsonify
from app.services.partido_service import PartidoService
from app.repositories.incidencia_repositorio import IncidenciaRepository

resultados_bp = Blueprint('resultados', __name__, url_prefix='/resultados')

@resultados_bp.route('/ultimos', methods=['GET'])
def ultimos_resultados():
    categoria = request.args.get('categoria')
    filtros = {'estado': 'jugado'}
    if categoria:
        filtros['categoria'] = categoria
    partidos = PartidoService.listar_partidos(filtros)
    # Ordenar por fecha descendente y limitar a los últimos 5
    partidos = sorted(partidos, key=lambda x: x.fecha_hora or 0, reverse=True)[:5]

    # Si el partido no tiene goles cargados, calcularlos desde incidencias (tipo='gol')
    partido_ids = [p.id for p in partidos]
    incidencias_gol = IncidenciaRepository.listar_goles_por_partidos(partido_ids)
    max_inc_por_partido = IncidenciaRepository.max_created_at_por_partido(partido_ids)
    goles_por_partido = {}
    for inc in incidencias_gol:
        pid = inc.partido_id
        goles_por_partido.setdefault(pid, {})
        goles_por_partido[pid][inc.club_id] = goles_por_partido[pid].get(inc.club_id, 0) + 1

    def dump(p):
        goles_local = p.goles_local
        goles_visitante = p.goles_visitante
        # Completar desde incidencias si es None
        if goles_local is None or goles_visitante is None:
            mapa = goles_por_partido.get(p.id, {})
            goles_local = mapa.get(p.club_local_id, 0) if goles_local is None else goles_local
            goles_visitante = mapa.get(p.club_visitante_id, 0) if goles_visitante is None else goles_visitante
        # Fecha de cierre
        cerrado_en = None
        if getattr(p, 'cerrado_at', None):
            cerrado_en = p.cerrado_at.isoformat()
        else:
            mi = max_inc_por_partido.get(p.id)
            cerrado_en = mi.isoformat() if mi else (p.fecha_hora.isoformat() if p.fecha_hora else None)
        return {
            'id': p.id,
            'fecha': p.fecha_hora.isoformat() if p.fecha_hora else None,
            'cerrado_en': cerrado_en,
            'torneo': p.torneo,
            'categoria': p.categoria,
            'local': p.club_local.nombre if p.club_local else '',
            'visitante': p.club_visitante.nombre if p.club_visitante else '',
            'goles_local': goles_local,
            'goles_visitante': goles_visitante
        }

    return jsonify([dump(p) for p in partidos])
