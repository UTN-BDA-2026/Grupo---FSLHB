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


PLANILLA_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'planilla', 'PLANILLA.pdf')
PLANILLAS_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'planillas')

# Ajustes finos de posiciones en milímetros para esta plantilla
# Referencia: página A4, origen abajo-izquierda. Tocar solo si se ve corrido.
POS = {
    'header': {
        'fecha_nro': (35, 264),
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
        'apellido': 4, # Si aumento se mueve mas hacia la derecha
        'nombre': 28,      # más a la izquierda para centrar en NOMBRE/S
        'dni_center': 56,  # más a la izquierda para centrar en D.N.I.
        'v_center': 86,
        'a_center': 92,
        'r_center': 98,
    },
    'lista_right': {
        'base_x': 112,
        'start_y': 240,
        'row_h': 6.4,
        'n_center': 4.8,
        'apellido': 2,
        'nombre': 25,
        'dni_center': 55,
        'v_center': 86,
        'a_center': 92,
        'r_center': 98,
    },
    'goles_left': {
        'x': 18,
        'y_start': 65,
        'row_h': 6.6,
        'offs': {'n':0,'jug':8,'eq':55,'min':70,'par':86}
    },
    'goles_right': {
        'x': 112,
        'y_start': 65,
        'row_h': 6.6,
        'offs': {'n':0,'jug':8,'eq':55,'min':70,'par':86}
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

    # Conteo por jugadora (tarjetas/goles)
    tarjetas_por_jug = {}
    goles_ordenados = []  # (min, club_id, jugadora_nombre)
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
        elif inc.tipo == 'gol':
            nombre = ''
            # busco nombre en listas
            for arr in (jug_local, jug_visit):
                for j in arr:
                    if _get(j, 'id') == _get(inc, 'jugadora_id'):
                        nombre = f"{_get(j, 'apellido', '')} {_get(j, 'nombre', '')}".strip()
                        break
            goles_ordenados.append((_get(inc, 'minuto', None), _get(inc, 'club_id', None), nombre))

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

    # Goles (tabla inferior): N°, JUGADOR, EQUIPO, TIEMPO, PARCIAL
    goles_local = 0
    goles_visit = 0
    y_gol_left = POS['goles_left']['y_start']
    y_gol_right = POS['goles_right']['y_start']
    for idx, (minuto, club_id, nombre) in enumerate(goles_ordenados, start=1):
        equipo_lbl = 'LOC' if club_id == getattr(p, 'club_local_id', None) else 'VIS'
        if equipo_lbl == 'LOC':
            goles_local += 1
        else:
            goles_visit += 1
        parcial = f"{goles_local} - {goles_visit}"
        # izquierda ocupa 7 filas aprox; luego derecha
        if idx <= 7:
            x = POS['goles_left']['x']; y = y_gol_left
            y_gol_left -= POS['goles_left']['row_h']
        else:
            x = POS['goles_right']['x']; y = y_gol_right
            y_gol_right -= POS['goles_right']['row_h']
        offs = POS['goles_left']['offs']
        _draw_text(c, x + offs['n'], y, str(idx), 9, scale_x=scale_x, scale_y=scale_y)
        _draw_text(c, x + offs['jug'], y, nombre or '', 9, scale_x=scale_x, scale_y=scale_y)
        _draw_text(c, x + offs['eq'], y, equipo_lbl, 9, scale_x=scale_x, scale_y=scale_y)
        _draw_text(c, x + offs['min'], y, _string(minuto) if minuto is not None else '', 9, scale_x=scale_x, scale_y=scale_y)
        _draw_text(c, x + offs['par'], y, parcial, 9, scale_x=scale_x, scale_y=scale_y)

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
