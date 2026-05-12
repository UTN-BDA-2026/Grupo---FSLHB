from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from app.services.partido_service import PartidoService
from app.services.precarga_service import PrecargaService
from app.services.incidencia_service import IncidenciaService
from app.services.nota_partido_service import NotaPartidoService
from app.services.cuerpo_tecnico_partido_service import CuerpoTecnicoPartidoService
from app.services.cuerpo_tecnico_service import CuerpoTecnicoService
from app.repositories.cuerpo_tecnico_repositorio import CuerpoTecnicoRepositorio
from flask import send_file
from app.services.planilla_service import generar_planilla_pdf
from app.services.sancion_service import SancionService
from app.services.arbitro_service import ArbitroService
from app.services.arbitro_partido_service import ArbitroPartidoService
from app.services.partido_fixture_service import cargar_partidos_desde_csv_fileobj
from app import require_admin, csrf
from app.extensions import mongo
from app.models.club import Club
from bson import ObjectId

partido_bp = Blueprint('partido', __name__)

@partido_bp.route('/partidos', methods=['GET'])
def listar_partidos():
    filtros = {
        'torneo': request.args.get('torneo'),
        'categoria': request.args.get('categoria'),
        'club_id': request.args.get('club_id'),
        'fecha_numero': request.args.get('fecha_numero', type=int),
        'estado': request.args.get('estado'),
        'estado_not': request.args.get('estado_not')
    }
    # Convert club_id to ObjectId if present
    if filtros.get('club_id'):
        filtros['club_id'] = ObjectId(filtros['club_id'])
    partidos = PartidoService.listar_partidos({k: v for k, v in filtros.items() if v})

    # Collect unique club/equipo IDs for batch lookup
    club_ids = set()
    equipo_ids = set()
    for p in partidos:
        if p.club_local_id: club_ids.add(p.club_local_id)
        if p.club_visitante_id: club_ids.add(p.club_visitante_id)
        if p.equipo_local_id: equipo_ids.add(p.equipo_local_id)
        if p.equipo_visitante_id: equipo_ids.add(p.equipo_visitante_id)

    clubes = {d['_id']: d for d in mongo.db.clubes.find({'_id': {'$in': list(club_ids)}})} if club_ids else {}
    equipos = {d['_id']: d for d in mongo.db.equipos.find({'_id': {'$in': list(equipo_ids)}})} if equipo_ids else {}

    def dump(p):
        cl = clubes.get(p.club_local_id, {})
        cv = clubes.get(p.club_visitante_id, {})
        el = equipos.get(p.equipo_local_id, {})
        ev = equipos.get(p.equipo_visitante_id, {})
        return {
            'id': str(p.id),
            'torneo': p.torneo,
            'categoria': p.categoria,
            'fecha_numero': p.fecha_numero,
            'bloque': p.bloque,
            'fecha_hora': p.fecha_hora.isoformat() if p.fecha_hora else None,
            'cancha': p.cancha,
            'club_local_id': str(p.club_local_id) if p.club_local_id else None,
            'club_visitante_id': str(p.club_visitante_id) if p.club_visitante_id else None,
            'equipo_local_id': str(p.equipo_local_id) if p.equipo_local_id else None,
            'equipo_visitante_id': str(p.equipo_visitante_id) if p.equipo_visitante_id else None,
            'club_local_nombre': cl.get('nombre'),
            'club_visitante_nombre': cv.get('nombre'),
            'equipo_local_nombre': el.get('nombre'),
            'equipo_visitante_nombre': ev.get('nombre'),
            'estado': p.estado,
            'goles_local': p.goles_local,
            'goles_visitante': p.goles_visitante
        }
    return jsonify([dump(p) for p in partidos])

@partido_bp.route('/partidos/<id>', methods=['GET'])
def obtener_partido(id):
    p = PartidoService.obtener_por_id(id)
    if not p:
        return jsonify({'error': 'No encontrado'}), 404

    cl_local = Club.from_dict(mongo.db.clubes.find_one({'_id': p.club_local_id})) if p.club_local_id else None
    cl_visit = Club.from_dict(mongo.db.clubes.find_one({'_id': p.club_visitante_id})) if p.club_visitante_id else None
    el = mongo.db.equipos.find_one({'_id': p.equipo_local_id}) if p.equipo_local_id else None
    ev = mongo.db.equipos.find_one({'_id': p.equipo_visitante_id}) if p.equipo_visitante_id else None

    return jsonify({
        'id': str(p.id),
        'torneo': p.torneo,
        'categoria': p.categoria,
        'fecha_numero': p.fecha_numero,
        'bloque': p.bloque,
        'fecha_hora': p.fecha_hora.isoformat() if p.fecha_hora else None,
        'cancha': p.cancha,
        'club_local_id': str(p.club_local_id) if p.club_local_id else None,
        'club_visitante_id': str(p.club_visitante_id) if p.club_visitante_id else None,
        'equipo_local_id': str(p.equipo_local_id) if p.equipo_local_id else None,
        'equipo_visitante_id': str(p.equipo_visitante_id) if p.equipo_visitante_id else None,
        'club_local_nombre': cl_local.nombre if cl_local else None,
        'club_visitante_nombre': cl_visit.nombre if cl_visit else None,
        'equipo_local_nombre': el.get('nombre') if el else None,
        'equipo_visitante_nombre': ev.get('nombre') if ev else None,
        'equipo_local_categoria': el.get('categoria') if el else None,
        'equipo_visitante_categoria': ev.get('categoria') if ev else None,
        'estado': p.estado,
        'goles_local': p.goles_local,
        'goles_visitante': p.goles_visitante
    })

@partido_bp.route('/partidos/<id>/debug', methods=['GET'])
def debug_partido(id):
    """Endpoint de depuración: muestra enlaces entre partido, clubes y equipos."""
    p = PartidoService.obtener_por_id(id)
    if not p:
        return jsonify({'error': 'No encontrado'}), 404

    cl_local = mongo.db.clubes.find_one({'_id': p.club_local_id}) if p.club_local_id else None
    cl_visit = mongo.db.clubes.find_one({'_id': p.club_visitante_id}) if p.club_visitante_id else None
    el = mongo.db.equipos.find_one({'_id': p.equipo_local_id}) if p.equipo_local_id else None
    ev = mongo.db.equipos.find_one({'_id': p.equipo_visitante_id}) if p.equipo_visitante_id else None

    def dump_equipo(e):
        if not e:
            return None
        return {
            'id': str(e['_id']),
            'nombre': e.get('nombre'),
            'categoria': e.get('categoria'),
            'club_id': str(e.get('club_id')) if e.get('club_id') else None
        }
    return jsonify({
        'partido_id': str(p.id),
        'torneo': p.torneo,
        'partido_categoria': p.categoria,
        'club_local_id': str(p.club_local_id) if p.club_local_id else None,
        'club_visitante_id': str(p.club_visitante_id) if p.club_visitante_id else None,
        'club_local_nombre': cl_local.get('nombre') if cl_local else None,
        'club_visitante_nombre': cl_visit.get('nombre') if cl_visit else None,
        'equipo_local': dump_equipo(el),
        'equipo_visitante': dump_equipo(ev),
    })

@partido_bp.route('/partidos', methods=['POST'])
def crear_partido():
    data = request.get_json() or {}
    admin_key = request.headers.get('X-Admin-Key')
    expected = os.environ.get('ADMIN_API_KEY')
    if not expected or admin_key != expected:
        return jsonify({'error': 'No autorizado'}), 401
    requeridos = ['torneo', 'categoria', 'club_local_id', 'club_visitante_id']
    faltan = [k for k in requeridos if not data.get(k)]
    if faltan:
        return jsonify({'error': f"Faltan campos: {', '.join(faltan)}"}), 400
    if data.get('club_local_id') == data.get('club_visitante_id'):
        return jsonify({'error': 'El club local y visitante no pueden ser el mismo'}), 400
    fh = data.get('fecha_hora')
    if isinstance(fh, str) and fh.strip():
        try:
            data['fecha_hora'] = datetime.fromisoformat(fh)
        except Exception:
            return jsonify({'error': 'Formato de fecha_hora inválido. Use ISO, ej: 2025-10-11T16:30'}), 400
    # Convert string IDs to ObjectId
    for field in ('club_local_id', 'club_visitante_id', 'equipo_local_id', 'equipo_visitante_id'):
        if data.get(field):
            data[field] = ObjectId(data[field])
    partido = PartidoService.crear_partido(data)
    return jsonify({'id': str(partido.id)}), 201

@partido_bp.route('/partidos/<id>/resultado', methods=['PATCH'])
def marcar_resultado(id):
    data = request.get_json() or {}
    pl = data.get('goles_local')
    pv = data.get('goles_visitante')
    partido = PartidoService.marcar_resultado(id, pl, pv)
    if not partido:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify({'ok': True})

@partido_bp.route('/partidos/<id>/precarga', methods=['GET', 'PUT'])
def precarga_partido(id):
    club_id = request.args.get('club_id')
    if request.method == 'GET':
        if not club_id:
            return jsonify({'error': 'club_id requerido'}), 400
        filas = PrecargaService.obtener(id, club_id)
        return jsonify([{'jugadora_id': str(f.jugadora_id)} for f in filas])
    else:
        data = request.get_json() or {}
        jugadora_ids = data.get('jugadora_ids') or []
        club_id = data.get('club_id') or club_id
        if not club_id:
            return jsonify({'error': 'club_id requerido'}), 400
        if len(jugadora_ids) < 7 or len(jugadora_ids) > 20:
            return jsonify({'error': 'La precarga debe tener entre 7 y 20 jugadoras'}), 400
        PrecargaService.guardar(id, club_id, jugadora_ids)
        return jsonify({'ok': True})

@partido_bp.route('/partidos/<id>/apertura', methods=['PATCH'])
def apertura_partido(id):
    partido = PartidoService.obtener_por_id(id)
    if not partido:
        return jsonify({'error': 'No encontrado'}), 404
    precarga_local = PrecargaService.obtener(id, partido.club_local_id)
    precarga_visitante = PrecargaService.obtener(id, partido.club_visitante_id)
    faltantes = []
    if not precarga_local:
        cl = mongo.db.clubes.find_one({'_id': partido.club_local_id})
        faltantes.append(cl.get('nombre', 'Club Local') if cl else 'Club Local')
    if not precarga_visitante:
        cv = mongo.db.clubes.find_one({'_id': partido.club_visitante_id})
        faltantes.append(cv.get('nombre', 'Club Visitante') if cv else 'Club Visitante')
    if faltantes:
        return jsonify({'error': f'No es posible hacer la apertura por falta de carga del club: {" y ".join(faltantes)}'}), 400
    partido = PartidoService.abrir_partido(id)
    return jsonify({'ok': True, 'estado': partido.estado})

@partido_bp.route('/partidos/<id>/cierre', methods=['PATCH'])
def cierre_partido(id):
    """Cierra el partido marcando su estado como 'jugado' y devolviendo el estado."""
    partido = PartidoService.cerrar_partido(id)
    if not partido:
        return jsonify({'error': 'No encontrado'}), 404
    planilla_url = None
    try:
        path = generar_planilla_pdf(id)
        planilla_url = f"/partidos/{id}/planilla.pdf"
    except Exception as e:
        planilla_url = None
    return jsonify({'ok': True, 'estado': partido.estado, 'planilla_url': planilla_url})

@partido_bp.route('/partidos/<id>/alineaciones', methods=['GET'])
def alineaciones_partido(id):
    p = PartidoService.obtener_por_id(id)
    if not p:
        return jsonify({'error': 'No encontrado'}), 404
    data = PrecargaService.obtener_alineaciones(id)
    cl = mongo.db.clubes.find_one({'_id': p.club_local_id})
    cv = mongo.db.clubes.find_one({'_id': p.club_visitante_id})
    club_local = cl.get('nombre', 'Club Local') if cl else 'Club Local'
    club_visit = cv.get('nombre', 'Club Visitante') if cv else 'Club Visitante'
    return jsonify({
        'club_local': {'id': str(p.club_local_id), 'nombre': club_local, 'jugadoras': data.get(p.club_local_id, [])},
        'club_visitante': {'id': str(p.club_visitante_id), 'nombre': club_visit, 'jugadoras': data.get(p.club_visitante_id, [])}
    })

@partido_bp.route('/partidos/<id>/planilla.pdf', methods=['GET'])
def descargar_planilla(id):
    """Descarga/genera la planilla PDF del partido."""
    try:
        path = generar_planilla_pdf(id)
        return send_file(path, mimetype='application/pdf', as_attachment=True, download_name=f'planilla_partido_{id}.pdf')
    except Exception as e:
        return jsonify({'error': 'No se pudo generar la planilla', 'detail': str(e)}), 500

@partido_bp.route('/partidos/<id>/arbitros', methods=['GET', 'PUT'])
def arbitros_partido(id):
    if request.method == 'GET':
        asignados = ArbitroPartidoService.listar(id)
        p = PartidoService.obtener_por_id(id)
        local_id = getattr(p, 'club_local_id', None)
        visit_id = getattr(p, 'club_visitante_id', None)
        asign_local = next((x for x in asignados if x.get('club_id') == local_id), None)
        asign_visit = next((x for x in asignados if x.get('club_id') == visit_id), None)
        if not asign_local:
            asign_local = next((x for x in asignados if x.get('rol') in ('local', f'club_{local_id}')), None)
        if not asign_visit:
            asign_visit = next((x for x in asignados if x.get('rol') in ('visit', f'club_{visit_id}')), None)
        disponibles = [
            {
                'id': str(a.id),
                'nombre': a.nombre,
                'apellido': a.apellido,
                'dni': a.dni,
            } for a in ArbitroService.listar()
        ]
        return jsonify({'asignados': {'local': asign_local, 'visit': asign_visit}, 'disponibles': disponibles})
    else:
        data = request.get_json(silent=True) or {}
        p = PartidoService.obtener_por_id(id)
        local_club = getattr(p, 'club_local_id', None)
        visit_club = getattr(p, 'club_visitante_id', None)
        local_id = data.get('local_id', None)
        visit_id = data.get('visit_id', None)
        try:
            if local_club is not None:
                ArbitroPartidoService.set_por_equipo(id, local_club, local_id)
            if visit_club is not None:
                ArbitroPartidoService.set_por_equipo(id, visit_club, visit_id)
            return jsonify({'ok': True})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'No se pudo guardar', 'detail': str(e)}), 500

@partido_bp.route('/partidos/<id>/suspensiones', methods=['GET'])
def suspensiones_partido(id):
    club_id = request.args.get('club_id')
    if not club_id:
        return jsonify({'error': 'club_id requerido'}), 400
    try:
        suspendidos = SancionService.jugadores_suspendidos_para_partido(id, club_id)
        return jsonify(suspendidos)
    except Exception as e:
        return jsonify({'error': 'No se pudo calcular suspensiones', 'detail': str(e)}), 500

@partido_bp.route('/partidos/<id>/incidencias', methods=['GET', 'POST'])
def incidencias_partido(id):
    if request.method == 'GET':
        filas = IncidenciaService.listar(id)
        return jsonify([
            {
                'id': str(f.id),
                'partido_id': str(f.partido_id),
                'club_id': str(f.club_id),
                'jugadora_id': str(f.jugadora_id),
                'tipo': f.tipo,
                'color': f.color,
                'minuto': f.minuto,
                'created_at': f.created_at.isoformat() if getattr(f, 'created_at', None) else None,
            } for f in filas
        ])
    else:
        data = request.get_json() or {}
        club_id = data.get('club_id')
        jugadora_id = data.get('jugadora_id')
        tipo = data.get('tipo')
        minuto = data.get('minuto')
        if not (club_id and jugadora_id and tipo):
            return jsonify({'error': 'club_id, jugadora_id y tipo son requeridos'}), 400
        if tipo == 'gol':
            IncidenciaService.registrar_gol(id, club_id, jugadora_id, minuto)
        elif tipo == 'tarjeta':
            color = data.get('color')
            if color not in ('verde', 'amarilla', 'roja'):
                return jsonify({'error': 'color inválido'}), 400
            IncidenciaService.registrar_tarjeta(id, club_id, jugadora_id, color, minuto)
        elif tipo == 'lesion':
            IncidenciaService.registrar_lesion(id, club_id, jugadora_id, minuto)
        else:
            return jsonify({'error': 'tipo inválido'}), 400
        return jsonify({'ok': True}), 201

@partido_bp.route('/partidos/<id>/incidencias/<incidencia_id>', methods=['DELETE'])
def eliminar_incidencia(id, incidencia_id):
    ok = IncidenciaService.eliminar(id, incidencia_id)
    if not ok:
        return jsonify({'error': 'Incidencia no encontrada'}), 404
    return jsonify({'ok': True})

@partido_bp.route('/partidos/<id>/notas', methods=['GET', 'PUT'])
def notas_partido(id):
    if request.method == 'GET':
        nota = NotaPartidoService.obtener(id)
        return jsonify({'detalle': getattr(nota, 'detalle', '')})
    else:
        data = request.get_json() or {}
        detalle = data.get('detalle', '')
        NotaPartidoService.guardar(id, detalle)
        return jsonify({'ok': True})

@partido_bp.route('/partidos/<id>/cuerpo-tecnico', methods=['GET', 'PUT'])
def cuerpo_tecnico_partido(id):
    if request.method == 'GET':
        club_id = request.args.get('club_id')
        filas = CuerpoTecnicoPartidoService.listar_por_partido(id)
        resp = [
            {
                'id': str(f.id),
                'partido_id': str(f.partido_id),
                'club_id': str(f.club_id),
                'rol': f.rol,
                'cuerpo_tecnico_id': str(f.cuerpo_tecnico_id),
            } for f in filas
        ]
        if club_id:
            lista = CuerpoTecnicoService.listar(club_id)
            disponibles = [
                {
                    'id': str(r.id),
                    'nombre': r.nombre,
                    'apellido': r.apellido,
                    'dni': r.dni,
                    'rol': r.rol,
                } for r in lista
            ]
            return jsonify({'seleccionados': resp, 'disponibles': disponibles})
        return jsonify({'seleccionados': resp})
    else:
        data = request.get_json() or {}
        club_id = data.get('club_id')
        rol = data.get('rol')
        cuerpo_tecnico_id = data.get('cuerpo_tecnico_id')
        if not all([club_id, rol, cuerpo_tecnico_id]):
            return jsonify({'error': 'club_id, rol y cuerpo_tecnico_id son requeridos'}), 400
        try:
            ct_doc = mongo.db.cuerpo_tecnico.find_one({'_id': ObjectId(cuerpo_tecnico_id)})
            if not ct_doc:
                return jsonify({'error': 'Integrante no encontrado'}), 400
            if str(ct_doc.get('club_id')) != str(ObjectId(club_id)):
                return jsonify({'error': 'El integrante no pertenece a ese club'}), 400
            row = CuerpoTecnicoPartidoService.guardar(id, club_id, str(rol), cuerpo_tecnico_id)
            return jsonify({'ok': True, 'id': str(row.id)})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'No se pudo guardar', 'detail': str(e)}), 500


@partido_bp.route('/admin/partidos/fixture', methods=['POST'])
@csrf.exempt
@require_admin
def cargar_fixture_partidos_admin():
    """Carga partidos desde un CSV subido por el panel admin."""
    if 'archivo' not in request.files:
        return jsonify({'error': 'Debe enviar un archivo CSV en el campo "archivo"'}), 400

    file_storage = request.files['archivo']
    if not file_storage.filename:
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    try:
        import io
        raw = file_storage.read()
        text = raw.decode('utf-8-sig')
        f = io.StringIO(text)
        creados = cargar_partidos_desde_csv_fileobj(f)
        return jsonify({'ok': True, 'creados': creados})
    except Exception as exc:
        return jsonify({'error': 'No se pudo procesar el CSV de partidos', 'detail': str(exc)}), 500
