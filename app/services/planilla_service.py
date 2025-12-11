from datetime import datetime
import os
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PyPDF2 import PdfReader, PdfWriter

from app.models.partido import Partido
from app.services.partido_service import PartidoService
from app.services.precarga_service import PrecargaService
from app.services.incidencia_service import IncidenciaService
from app.services.cuerpo_tecnico_partido_service import CuerpoTecnicoPartidoService
from app.services.cuerpo_tecnico_service import CuerpoTecnicoService
from app.services.arbitro_partido_service import ArbitroPartidoService
from app.services.nota_partido_service import NotaPartidoService
from app.models.cuerpo_tecnico import CuerpoTecnico
from app.services.club_service import ClubService


PLANILLA_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'planilla', 'PLANILLA.pdf')
PLANILLAS_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'planillas')

# Ajustes finos de posiciones en milímetros para esta plantilla
# Referencia: página A4, origen abajo-izquierda. Tocar solo si se ve corrido.
POS = {
    'header': {
        'fecha_nro': (26, 264),
        'division': (53.5, 264),
        'cancha':   (97.5, 264),
        'hora':     (144, 264),
        'dia':      (164, 264),
    },
    'equipos': {
        'local': (27, 254.5),       # movido más a la derecha y más abajo
        'visit': (128, 254.5),      # antes 115
    },
    'lista_left': {
        'base_x': 15,
        'start_y': 240,
        'row_h': 6.4,
        'n_center': 4.8,
        'apellido': 0, # Si aumento se mueve mas hacia la derecha
        'nombre': 23,      # más a la izquierda para centrar en NOMBRE/S
        'dni_center': 53,  # más a la izquierda para centrar en D.N.I.
        'v_center': 69.5, #modifica la tarjeta verde
        'a_center': 92, #modifica la tarjeta amarilla
        'r_center': 98, #modifica la tarjeta roja
    },
    'lista_right': {
        'base_x': 112,
        'start_y': 240,
        'row_h': 6.4,
        'n_center': 4.8,
        'apellido': -4,
        'nombre': 21.5,
        'dni_center': 50,
        'v_center': 86,
        'a_center': 74,
        'r_center': 80,
    },
    # Campos adicionales a completar en la planilla
    'ct_left': {
        'entrenador': (31, 117),      # desplazado a la derecha del rótulo "ENTRENADOR:"
        'ayudante':   (44, 116),      # desplazado a la derecha del rótulo "AYUDANTE TÉCNICO:"
        'capitan':    (24, 109),      # opcional si se usa más adelante
    },
    'ct_right': {
        'entrenador': (131, 117),     # desplazado a la derecha del rótulo en columna derecha
        'ayudante':   (146, 116),
        'capitan':    (126, 109),
    },
    'arbitros': {
        'left':  (35, 52.5),            # texto a la derecha del rótulo "ARBITRO:" (izquierda)
        'right': (135, 52.5),           # texto a la derecha del rótulo "ARBITRO:" (derecha)
    },
    'observaciones': {
        'start_x': 8,                # Texto libre a la derecha de "OBSERVACIONES:"
        'start_y': 35,
        'max_width_mm': 150,          # ancho aprox. util
        'line_h': 5.0,
    }
}


def _dia_semana(dt: datetime) -> str:
    if not dt:
        return ''
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    return dias[dt.weekday()]


def _string(v):
    return '' if v is None else str(v)


def _get(obj, key, default=None):
    """Obtiene un atributo o clave tanto de objetos como de dicts."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _draw_text(c: canvas.Canvas, x_mm: float, y_mm: float, text: str, size: int = 9, bold: bool = False, *, scale_x: float = 1.0, scale_y: float = 1.0):
    """Dibuja texto en coordenadas milimétricas.

    scale_x/scale_y permiten ajustar cuando la plantilla no es A4
    (p.ej. Carta/Letter). Se asume que las posiciones base están medidas
    sobre A4 (210x297 mm) y se escalan proporcionalmente a la página real.
    """
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    c.drawString(x_mm * scale_x * mm, y_mm * scale_y * mm, text)

def _draw_centered(c: canvas.Canvas, x_mm: float, y_mm: float, text: str, size: int = 9, bold: bool = False, *, scale_x: float = 1.0, scale_y: float = 1.0):
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    c.drawCentredString(x_mm * scale_x * mm, y_mm * scale_y * mm, text)


def generar_planilla_pdf(partido_id: int) -> str:
    """
    Genera un PDF de planilla superponiendo datos sobre app/planilla/PLANILLA.pdf.
    Devuelve la ruta absoluta del archivo generado.
    """
    # Asegurar rutas
    os.makedirs(PLANILLAS_OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(PLANILLAS_OUTPUT_DIR, f'planilla_partido_{partido_id}.pdf')

    # Datos de partido
    p: Partido = PartidoService.obtener_por_id(partido_id)
    if not p:
        raise ValueError('Partido no encontrado')

    # Alineaciones por club
    alineaciones = PrecargaService.obtener_alineaciones(partido_id) or {}
    jug_local = alineaciones.get(getattr(p, 'club_local_id', None), []) or alineaciones.get('club_local', [])
    jug_visit = alineaciones.get(getattr(p, 'club_visitante_id', None), []) or alineaciones.get('club_visitante', [])

    # Incidencias
    incidencias = IncidenciaService.listar(partido_id) or []

    # Cuerpo técnico seleccionados (DT y PF por club)
    ct_sel = CuerpoTecnicoPartidoService.listar_por_partido(partido_id) or []
    def _norm_rol(s: str | None) -> str | None:
        if not s:
            return None
        t = str(s).strip().lower()
        # normalizar variantes comunes
        t = t.replace('-', ' ').replace('_', ' ')
        t = ' '.join(t.split())
        # mapear sinónimos habituales
        if (
            t in ('dt', 'director tecnico', 'director', 'directortecnico', 'director tecnico.', 'd.t.', 'd t')
            or 'director' in t or 'entrenador' in t
        ):
            return 'director_tecnico'
        if (
            t in ('pf', 'preparador fisico', 'preparador', 'preparadorfisico', 'preparador fisico.', 'p.f.', 'p f')
            or 'ayudante' in t or 'fisico' in t
        ):
            return 'preparador_fisico'
        return t
    def _ct_name(ct_id):
        try:
            row = CuerpoTecnico.query.get(int(ct_id)) if ct_id else None
            if not row:
                return ''
            return f"{row.apellido} {row.nombre}".strip()
        except Exception:
            return ''
    dt_local = pf_local = dt_visit = pf_visit = ''
    for r in ct_sel:
        try:
            roln = _norm_rol(getattr(r, 'rol', None))
            if r.club_id == getattr(p, 'club_local_id', None):
                if roln == 'director_tecnico':
                    dt_local = _ct_name(r.cuerpo_tecnico_id)
                elif roln == 'preparador_fisico':
                    pf_local = _ct_name(r.cuerpo_tecnico_id)
            elif r.club_id == getattr(p, 'club_visitante_id', None):
                if roln == 'director_tecnico':
                    dt_visit = _ct_name(r.cuerpo_tecnico_id)
                elif roln == 'preparador_fisico':
                    pf_visit = _ct_name(r.cuerpo_tecnico_id)
        except Exception:
            continue

    # Fallback: si no hay DT seleccionado en el partido, usar el DT del club (rol 'DT')
    try:
        if not dt_local and getattr(p, 'club_local_id', None):
            lista_ct_local = CuerpoTecnicoService.listar(getattr(p, 'club_local_id', None)) or []
            for ct in lista_ct_local:
                if str(getattr(ct, 'rol', '')).upper() == 'DT':
                    dt_local = f"{getattr(ct,'apellido','')} {getattr(ct,'nombre','')}".strip()
                    break
        if not dt_visit and getattr(p, 'club_visitante_id', None):
            lista_ct_visit = CuerpoTecnicoService.listar(getattr(p, 'club_visitante_id', None)) or []
            for ct in lista_ct_visit:
                if str(getattr(ct, 'rol', '')).upper() == 'DT':
                    dt_visit = f"{getattr(ct,'apellido','')} {getattr(ct,'nombre','')}".strip()
                    break
    except Exception:
        pass

    # Árbitros del partido (hasta 2)
    arbitros = []
    try:
        for row in ArbitroPartidoService.listar(partido_id) or []:
            if isinstance(row, dict):
                a = row.get('arbitro', {})
                nom = f"{a.get('apellido','')} {a.get('nombre','')}".strip()
            else:
                a = getattr(row, 'arbitro', None)
                if a is not None:
                    nom = f"{getattr(a,'apellido','')} {getattr(a,'nombre','')}".strip()
                else:
                    nom = ''
            if nom:
                arbitros.append(nom)
    except Exception:
        arbitros = []

    # Fallback: si el partido no tiene árbitros asignados, usar árbitros por defecto de cada club
    if not arbitros:
        try:
            arb_local = ClubService.obtener_arbitro(getattr(p, 'club_local_id', None)) if getattr(p, 'club_local_id', None) else None
            arb_visit = ClubService.obtener_arbitro(getattr(p, 'club_visitante_id', None)) if getattr(p, 'club_visitante_id', None) else None
            if arb_local:
                nombre = f"{getattr(arb_local,'apellido','')} {getattr(arb_local,'nombre','')}".strip()
                if nombre:
                    arbitros.append(nombre)
            if arb_visit:
                nombre = f"{getattr(arb_visit,'apellido','')} {getattr(arb_visit,'nombre','')}".strip()
                if nombre:
                    arbitros.append(nombre)
        except Exception:
            pass

    # Observaciones
    try:
        nota = NotaPartidoService.obtener(partido_id)
        observaciones = getattr(nota, 'detalle', '') or ''
    except Exception:
        observaciones = ''

    # Conteo por jugadora (tarjetas/goles)
    tarjetas_por_jug = {}
    # Eliminamos el renderizado de la tabla de goles en la planilla
    goles_ordenados = []
    for inc in incidencias:
        if inc.tipo == 'tarjeta':
            key = int(_get(inc, 'jugadora_id')) if _get(inc, 'jugadora_id') is not None else None
            if key is None:
                continue
            d = tarjetas_por_jug.setdefault(key, {'v': 0, 'a': 0, 'r': 0})
            col = str(_get(inc, 'color', '')).lower()
            if col.startswith('ver'): d['v'] += 1
            elif col.startswith('ama'): d['a'] += 1
            elif col.startswith('roj'): d['r'] += 1
        # Se omite el procesamiento de goles para no dibujarlos

    goles_ordenados.sort(key=lambda x: (x[0] is None, x[0]))

    # Abrimos la plantilla primero para obtener su tamaño real
    template_reader = PdfReader(open(PLANILLA_TEMPLATE_PATH, 'rb'))
    base_page = template_reader.pages[0]
    # PyPDF2 maneja cajas en puntos (1 pt = 1/72"). mm es conversión a puntos
    try:
        width_pt = float(base_page.mediabox.right) - float(base_page.mediabox.left)
        height_pt = float(base_page.mediabox.top) - float(base_page.mediabox.bottom)
    except Exception:
        # Fallback conservador
        width_pt = 210 * mm
        height_pt = 297 * mm

    width_mm = width_pt / mm
    height_mm = height_pt / mm

    # Escalas contra A4 (coordenadas base fueron diseñadas para A4)
    scale_x = width_mm / 210.0
    scale_y = height_mm / 297.0

    # Crear una capa con el mismo tamaño que la plantilla
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width_pt, height_pt))

    # Encabezado
    torneo = _string(getattr(p, 'torneo', ''))
    division = _string(getattr(p, 'categoria', ''))
    fecha_nro = _string(getattr(p, 'fecha_numero', ''))
    cancha = _string(getattr(p, 'cancha', ''))
    fh: datetime = getattr(p, 'fecha_hora', None)
    hora = fh.strftime('%H:%M') if isinstance(fh, datetime) else ''
    dia = _dia_semana(fh)

    # Posiciones aproximadas (en milímetros) – se pueden ajustar luego
    _draw_text(c, *POS['header']['fecha_nro'], fecha_nro, 10, True, scale_x=scale_x, scale_y=scale_y)
    _draw_text(c, *POS['header']['division'], division, 10, True, scale_x=scale_x, scale_y=scale_y)
    _draw_text(c, *POS['header']['cancha'], cancha, 10, scale_x=scale_x, scale_y=scale_y)
    _draw_text(c, *POS['header']['hora'], hora, 10, scale_x=scale_x, scale_y=scale_y)
    _draw_text(c, *POS['header']['dia'], dia, 10, scale_x=scale_x, scale_y=scale_y)
    # Dibuja torneo solo si la clave existe para evitar KeyError
    if 'torneo' in POS.get('header', {}):
        _draw_text(c, *POS['header']['torneo'], torneo, 12, True, scale_x=scale_x, scale_y=scale_y)

    # Nombres equipos
    local_name = getattr(p, 'equipo_local', None).nombre if getattr(p, 'equipo_local', None) else (getattr(p, 'club_local', None).nombre if getattr(p, 'club_local', None) else 'Local')
    visit_name = getattr(p, 'equipo_visitante', None).nombre if getattr(p, 'equipo_visitante', None) else (getattr(p, 'club_visitante', None).nombre if getattr(p, 'club_visitante', None) else 'Visitante')
    _draw_text(c, *POS['equipos']['local'], local_name, 11, True, scale_x=scale_x, scale_y=scale_y)
    _draw_text(c, *POS['equipos']['visit'], visit_name, 11, True, scale_x=scale_x, scale_y=scale_y)

    # Listas de jugadoras (primeras 20)
    def draw_lista(conf: dict, jugadoras: list):
        base_x_mm = conf['base_x']
        y = conf['start_y']
        n = 1
        for j in (jugadoras or [])[:20]:
            apellido = _string(_get(j, 'apellido', ''))
            nombre = _string(_get(j, 'nombre', ''))
            dni = _string(_get(j, 'dni', ''))
            # Eliminado: no se dibuja el número de jugadora
            _draw_text(c, base_x_mm + conf['apellido'], y, apellido, 9, scale_x=scale_x, scale_y=scale_y)
            _draw_text(c, base_x_mm + conf['nombre'], y, nombre, 9, scale_x=scale_x, scale_y=scale_y)
            _draw_centered(c, base_x_mm + conf['dni_center'], y, dni, 9, scale_x=scale_x, scale_y=scale_y)
            # Tarjetas
            tid = _get(j, 'id', None)
            mark = tarjetas_por_jug.get(int(tid)) if tid is not None else None
            if mark:
                if mark.get('v'): _draw_centered(c, base_x_mm + conf['v_center'], y, 'X', 9, scale_x=scale_x, scale_y=scale_y)
                if mark.get('a'): _draw_centered(c, base_x_mm + conf['a_center'], y, 'X', 9, scale_x=scale_x, scale_y=scale_y)
                if mark.get('r'): _draw_centered(c, base_x_mm + conf['r_center'], y, 'X', 9, scale_x=scale_x, scale_y=scale_y)
            y -= conf['row_h']
            n += 1

    # Coordenadas aproximadas de inicio de filas (ajustables)
    draw_lista(POS['lista_left'], jug_local)
    draw_lista(POS['lista_right'], jug_visit)

    # Se omite la sección de dibujo de goles en la planilla

    # Cuerpo técnico: mostrar solo Director Técnico (no imprimir Ayudante/Preparador Físico)
    _draw_text(c, *POS['ct_left']['entrenador'], dt_local, 9, scale_x=scale_x, scale_y=scale_y)
    _draw_text(c, *POS['ct_right']['entrenador'], dt_visit, 9, scale_x=scale_x, scale_y=scale_y)

    # Árbitros (primero a izquierda, segundo a derecha). Solo nombres; el rótulo ya está impreso.
    if arbitros:
        _draw_text(c, *POS['arbitros']['left'], arbitros[0], 9, scale_x=scale_x, scale_y=scale_y)
        if len(arbitros) > 1:
            _draw_text(c, *POS['arbitros']['right'], arbitros[1], 9, scale_x=scale_x, scale_y=scale_y)
    
    # Observaciones (envolviendo en varias líneas si excede)
    if observaciones:
        max_w = POS['observaciones']['max_width_mm'] * scale_x * mm
        x0 = POS['observaciones']['start_x'] * scale_x
        y0 = POS['observaciones']['start_y'] * scale_y
        # partir por palabras usando ancho textual
        words = str(observaciones).split()
        line = ''
        lines = []
        for w in words:
            test = f"{line} {w}".strip()
            if c.stringWidth(test, 'Helvetica', 9) <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        y = y0
        for ln in lines[:5]:  # limitar a 5 líneas para no invadir márgenes
            _draw_text(c, x0, y, ln, 9, scale_x=1.0, scale_y=1.0)
            y -= POS['observaciones']['line_h']

    c.save()

    # Fusionar con la plantilla (sin reescalar)
    packet.seek(0)
    overlay_reader = PdfReader(packet)
    writer = PdfWriter()

    # Tomamos solo la primera página de la plantilla y superponemos
    base_page = template_reader.pages[0]
    base_page.merge_page(overlay_reader.pages[0])
    writer.add_page(base_page)

    with open(out_path, 'wb') as f:
        writer.write(f)

    return os.path.abspath(out_path)
