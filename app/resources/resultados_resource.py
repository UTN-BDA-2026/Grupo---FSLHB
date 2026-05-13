from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from app.extensions import mongo
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
    def _sort_key(p):
        fh = getattr(p, 'fecha_hora', None)
        if fh is None:
            return 0
        ts = getattr(fh, 'timestamp', None)
        if callable(ts):
            try:
                return ts()
            except Exception:
                return 0
        if isinstance(fh, str) and fh.strip():
            try:
                # Soporta ISO (y el caso típico con 'Z')
                s = fh.strip().replace('Z', '+00:00')
                return datetime.fromisoformat(s).timestamp()
            except Exception:
                return 0
        # Fallback si llega como número
        try:
            return float(fh)
        except Exception:
            return 0

    partidos = sorted(partidos, key=_sort_key, reverse=True)[:5]

    def _to_oid(value):
        if value is None:
            return None
        if isinstance(value, ObjectId):
            return value
        try:
            return ObjectId(str(value))
        except Exception:
            return None

    # Resolver nombres de clubes para los (máximo) 5 partidos
    club_ids = []
    for p in partidos:
        club_ids.extend([getattr(p, 'club_local_id', None), getattr(p, 'club_visitante_id', None)])
    club_oids = [oid for oid in (_to_oid(cid) for cid in club_ids) if oid is not None]
    club_nombre = {}
    if club_oids:
        for d in mongo.db.clubes.find({'_id': {'$in': club_oids}}, {'nombre': 1}):
            club_nombre[d['_id']] = d.get('nombre') or ''

    # Si el partido no tiene goles cargados, calcularlos desde incidencias (tipo='gol')
    partido_ids = [str(p.id) for p in partidos]
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
            ce = p.cerrado_at
            cerrado_en = ce.isoformat() if hasattr(ce, 'isoformat') else str(ce)
        else:
            mi = max_inc_por_partido.get(p.id)
            if mi is not None and hasattr(mi, 'isoformat'):
                cerrado_en = mi.isoformat()
            else:
                fh = getattr(p, 'fecha_hora', None)
                cerrado_en = fh.isoformat() if fh is not None and hasattr(fh, 'isoformat') else (str(fh) if fh else None)

        clid = _to_oid(getattr(p, 'club_local_id', None))
        cvid = _to_oid(getattr(p, 'club_visitante_id', None))
        fh = getattr(p, 'fecha_hora', None)
        return {
            'id': str(p.id),
            'fecha': fh.isoformat() if fh is not None and hasattr(fh, 'isoformat') else (str(fh) if fh else None),
            'cerrado_en': cerrado_en,
            'torneo': str(p.torneo) if isinstance(getattr(p, 'torneo', None), ObjectId) else getattr(p, 'torneo', None),
            'categoria': p.categoria,
            'local': club_nombre.get(clid, '') if clid else '',
            'visitante': club_nombre.get(cvid, '') if cvid else '',
            'goles_local': goles_local,
            'goles_visitante': goles_visitante
        }

    return jsonify([dump(p) for p in partidos])
