from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from app.services.partido_service import PartidoService
from app.services.precarga_service import PrecargaService
from app.services.incidencia_service import IncidenciaService
from app.services.nota_partido_service import NotaPartidoService
from app.services.cuerpo_tecnico_partido_service import CuerpoTecnicoPartidoService
from app.services.cuerpo_tecnico_service import CuerpoTecnicoService
from app.models.cuerpo_tecnico import CuerpoTecnico
from sqlalchemy.exc import ProgrammingError, OperationalError
from flask import send_file
from app.services.planilla_service import generar_planilla_pdf
from app.services.sancion_service import SancionService
from app.services.arbitro_service import ArbitroService
from app.services.arbitro_partido_service import ArbitroPartidoService

partido_bp = Blueprint('partido', __name__)

@partido_bp.route('/partidos', methods=['GET'])
def listar_partidos():
    filtros = {
        'torneo': request.args.get('torneo'),
        'categoria': request.args.get('categoria'),
        'club_id': request.args.get('club_id', type=int),
        'fecha_numero': request.args.get('fecha_numero', type=int),
        'estado': request.args.get('estado'),
        'estado_not': request.args.get('estado_not')
    }
    partidos = PartidoService.listar_partidos({k: v for k, v in filtros.items() if v})
    # Serialización simple
    def dump(p):
        return {
            'id': p.id,
            'torneo': p.torneo,
            'categoria': p.categoria,
            'fecha_numero': p.fecha_numero,
            'bloque': p.bloque,
            'fecha_hora': p.fecha_hora.isoformat() if p.fecha_hora else None,
            'cancha': p.cancha,
            'club_local_id': p.club_local_id,
            'club_visitante_id': p.club_visitante_id,
            'equipo_local_id': p.equipo_local_id,
            'equipo_visitante_id': p.equipo_visitante_id,
            'club_local_nombre': p.club_local.nombre if p.club_local else None,
            'club_visitante_nombre': p.club_visitante.nombre if p.club_visitante else None,
            'equipo_local_nombre': p.equipo_local.nombre if p.equipo_local else None,
            'equipo_visitante_nombre': p.equipo_visitante.nombre if p.equipo_visitante else None,
            'estado': p.estado,
            'goles_local': p.goles_local,
            'goles_visitante': p.goles_visitante
        }
    return jsonify([dump(p) for p in partidos])

@partido_bp.route('/partidos/<int:id>', methods=['GET'])
def obtener_partido(id: int):
    p = PartidoService.obtener_por_id(id)
    if not p:
        return jsonify({'error': 'No encontrado'}), 404
    # incluir info de equipos y clubes para armar el 'Encuentro'
    def dump_detalle(p):
        cl_local = p.club_local
        cl_visit = p.club_visitante
        return {
            'id': p.id,
            'torneo': p.torneo,
            'categoria': p.categoria,
            'fecha_numero': p.fecha_numero,
            'bloque': p.bloque,
            'fecha_hora': p.fecha_hora.isoformat() if p.fecha_hora else None,
            'cancha': p.cancha,
            'club_local_id': p.club_local_id,
            'club_visitante_id': p.club_visitante_id,
            'equipo_local_id': p.equipo_local_id,
            'equipo_visitante_id': p.equipo_visitante_id,
            'club_local_nombre': cl_local.nombre if cl_local else None,
            'club_visitante_nombre': cl_visit.nombre if cl_visit else None,
            'equipo_local_nombre': p.equipo_local.nombre if p.equipo_local else None,
            'equipo_visitante_nombre': p.equipo_visitante.nombre if p.equipo_visitante else None,
            'estado': p.estado,
            'goles_local': p.goles_local,
            'goles_visitante': p.goles_visitante
        }
    return jsonify(dump_detalle(p))

@partido_bp.route('/partidos', methods=['POST'])
def crear_partido():
    data = request.get_json() or {}
    # Simple guard: header X-Admin-Key must match env ADMIN_API_KEY
    admin_key = request.headers.get('X-Admin-Key')
    expected = os.environ.get('ADMIN_API_KEY')
    if not expected or admin_key != expected:
        return jsonify({'error': 'No autorizado'}), 401
    # Validaciones mínimas
    requeridos = ['torneo', 'categoria', 'club_local_id', 'club_visitante_id']
    faltan = [k for k in requeridos if not data.get(k)]
    if faltan:
        return jsonify({'error': f"Faltan campos: {', '.join(faltan)}"}), 400
    if data.get('club_local_id') == data.get('club_visitante_id'):
        return jsonify({'error': 'El club local y visitante no pueden ser el mismo'}), 400
    # Parsear fecha_hora si viene como string ISO (de un input datetime-local por ejemplo)
    fh = data.get('fecha_hora')
    if isinstance(fh, str) and fh.strip():
        try:
            # Acepta formatos 'YYYY-MM-DDTHH:MM' o ISO completos
            data['fecha_hora'] = datetime.fromisoformat(fh)
        except Exception:
            return jsonify({'error': 'Formato de fecha_hora inválido. Use ISO, ej: 2025-10-11T16:30'}), 400
    partido = PartidoService.crear_partido(data)
    return jsonify({'id': partido.id}), 201

@partido_bp.route('/partidos/<int:id>/resultado', methods=['PATCH'])
def marcar_resultado(id: int):
    data = request.get_json() or {}
    pl = data.get('goles_local')
    pv = data.get('goles_visitante')
    partido = PartidoService.marcar_resultado(id, pl, pv)
    if not partido:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify({'ok': True})

@partido_bp.route('/partidos/<int:id>/precarga', methods=['GET', 'PUT'])
def precarga_partido(id: int):
    club_id = request.args.get('club_id', type=int)
    if request.method == 'GET':
        if not club_id:
            return jsonify({'error': 'club_id requerido'}), 400
        filas = PrecargaService.obtener(id, club_id)
        return jsonify([{'jugadora_id': f.jugadora_id} for f in filas])
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

@partido_bp.route('/partidos/<int:id>/apertura', methods=['PATCH'])
def apertura_partido(id: int):
    from app.services.precarga_service import PrecargaService
    from app.models.partido import Partido
    partido = PartidoService.obtener_por_id(id)
    if not partido:
        return jsonify({'error': 'No encontrado'}), 404
    # Verificar precarga de ambos clubes
    precarga_local = PrecargaService.obtener(id, partido.club_local_id)
    precarga_visitante = PrecargaService.obtener(id, partido.club_visitante_id)
    faltantes = []
    if not precarga_local:
        faltantes.append(partido.club_local.nombre if partido.club_local else 'Club Local')
    if not precarga_visitante:
        faltantes.append(partido.club_visitante.nombre if partido.club_visitante else 'Club Visitante')
    if faltantes:
        return jsonify({'error': f'No es posible hacer la apertura por falta de carga del club: {" y ".join(faltantes)}'}), 400
    partido = PartidoService.abrir_partido(id)
    return jsonify({'ok': True, 'estado': partido.estado})

@partido_bp.route('/partidos/<int:id>/cierre', methods=['PATCH'])
def cierre_partido(id: int):
    """Cierra el partido marcando su estado como 'jugado' y devolviendo el estado."""
    partido = PartidoService.cerrar_partido(id)
    if not partido:
        return jsonify({'error': 'No encontrado'}), 404
    # Generar planilla PDF al cerrar el partido (si falla, no bloquea el cierre)
    planilla_url = None
    try:
        path = generar_planilla_pdf(id)
        # Serviremos desde endpoint dedicado /partidos/<id>/planilla.pdf
        planilla_url = f"/partidos/{id}/planilla.pdf"
    except Exception as e:
        planilla_url = None
    return jsonify({'ok': True, 'estado': partido.estado, 'planilla_url': planilla_url})

@partido_bp.route('/partidos/<int:id>/alineaciones', methods=['GET'])
def alineaciones_partido(id: int):
    p = PartidoService.obtener_por_id(id)
    if not p:
        return jsonify({'error': 'No encontrado'}), 404
    data = PrecargaService.obtener_alineaciones(id)
    # Formato de respuesta con nombres de clubes
    club_local = p.club_local.nombre if p.club_local else 'Club Local'
    club_visit = p.club_visitante.nombre if p.club_visitante else 'Club Visitante'
    return jsonify({
        'club_local': {'id': p.club_local_id, 'nombre': club_local, 'jugadoras': data.get(p.club_local_id, [])},
        'club_visitante': {'id': p.club_visitante_id, 'nombre': club_visit, 'jugadoras': data.get(p.club_visitante_id, [])}
    })

@partido_bp.route('/partidos/<int:id>/planilla.pdf', methods=['GET'])
def descargar_planilla(id: int):
    """Descarga/genera la planilla PDF del partido."""
    try:
        path = generar_planilla_pdf(id)
        return send_file(path, mimetype='application/pdf', as_attachment=True, download_name=f'planilla_partido_{id}.pdf')
    except Exception as e:
        return jsonify({'error': 'No se pudo generar la planilla', 'detail': str(e)}), 500

@partido_bp.route('/partidos/<int:id>/arbitros', methods=['GET', 'PUT'])
def arbitros_partido(id: int):
    """GET: devuelve árbitros asignados al partido y la lista de disponibles.
    PUT: setea la lista de árbitros del partido (máx 2). Cuerpo: { arbitro_ids: [..] }
    """
    if request.method == 'GET':
        asignados = ArbitroPartidoService.listar(id)
        disponibles = [
            {
                'id': a.id,
                'nombre': a.nombre,
                'apellido': a.apellido,
                'dni': a.dni,
            } for a in ArbitroService.listar()
        ]
        return jsonify({'asignados': asignados, 'disponibles': disponibles})
    else:
        data = request.get_json() or {}
        arbitro_ids = data.get('arbitro_ids') or []
        try:
            ArbitroPartidoService.set_lista(id, arbitro_ids)
            return jsonify({'ok': True})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'No se pudo guardar', 'detail': str(e)}), 500

@partido_bp.route('/partidos/<int:id>/suspensiones', methods=['GET'])
def suspensiones_partido(id: int):
    """Devuelve jugadoras suspendidas para el partido dado y club indicado.

    Query params:
    - club_id: club al que se evalúan las suspensiones (requerido)
    """
    club_id = request.args.get('club_id', type=int)
    if not club_id:
        return jsonify({'error': 'club_id requerido'}), 400
    try:
        suspendidos = SancionService.jugadores_suspendidos_para_partido(id, club_id)
        return jsonify(suspendidos)
    except Exception as e:
        return jsonify({'error': 'No se pudo calcular suspensiones', 'detail': str(e)}), 500

@partido_bp.route('/partidos/<int:id>/incidencias', methods=['GET', 'POST'])
def incidencias_partido(id: int):
    if request.method == 'GET':
        filas = IncidenciaService.listar(id)
        return jsonify([
            {
                'id': f.id,
                'partido_id': f.partido_id,
                'club_id': f.club_id,
                'jugadora_id': f.jugadora_id,
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
        tipo = data.get('tipo')  # 'gol' o 'tarjeta'
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

@partido_bp.route('/partidos/<int:id>/notas', methods=['GET', 'PUT'])
def notas_partido(id: int):
    if request.method == 'GET':
        nota = NotaPartidoService.obtener(id)
        return jsonify({'detalle': getattr(nota, 'detalle', '')})
    else:
        data = request.get_json() or {}
        detalle = data.get('detalle', '')
        NotaPartidoService.guardar(id, detalle)
        return jsonify({'ok': True})

@partido_bp.route('/partidos/<int:id>/cuerpo-tecnico', methods=['GET', 'PUT'])
def cuerpo_tecnico_partido(id: int):
    if request.method == 'GET':
        # Devolver seleccionados por partido, y opcionalmente lista disponible por club_id
        club_id = request.args.get('club_id', type=int)
        try:
            filas = CuerpoTecnicoPartidoService.listar_por_partido(id)
            resp = [
                {
                    'id': f.id,
                    'partido_id': f.partido_id,
                    'club_id': f.club_id,
                    'rol': f.rol,
                    'cuerpo_tecnico_id': f.cuerpo_tecnico_id,
                } for f in filas
            ]
        except ProgrammingError:
            # Si la tabla aún no existe (migración pendiente), devolver vacío para no romper la UI
            resp = []
        if club_id:
            lista = CuerpoTecnicoService.listar(club_id)
            disponibles = [
                {
                    'id': r.id,
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
            # Validar que el integrante exista y pertenezca al club indicado
            ct = CuerpoTecnico.query.get(int(cuerpo_tecnico_id))
            if not ct:
                return jsonify({'error': 'Integrante no encontrado'}), 400
            if int(ct.club_id) != int(club_id):
                return jsonify({'error': 'El integrante no pertenece a ese club'}), 400
            row = CuerpoTecnicoPartidoService.guardar(id, int(club_id), str(rol), int(cuerpo_tecnico_id))
            return jsonify({'ok': True, 'id': row.id})
        except (ProgrammingError, OperationalError) as e:
            # Posible tabla faltante por migración no aplicada
            return jsonify({'error': 'Migración pendiente: ejecute "flask db upgrade"', 'detail': str(e)}), 500
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'No se pudo guardar', 'detail': str(e)}), 500
