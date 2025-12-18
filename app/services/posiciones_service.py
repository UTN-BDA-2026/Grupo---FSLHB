from collections import defaultdict
from app.repositories.partido_repositorio import PartidoRepository
from app.repositories.incidencia_repositorio import IncidenciaRepository
from app.repositories.equipo_repositorio import EquipoRepository


def obtener_tabla_posiciones(torneo, division, fecha, bloque):
    """
    Calcula la tabla de posiciones basada en:
    - Partidos del torneo/categoría seleccionados (y opcionalmente fecha)
    - Incidencias de tipo 'gol' para computar GF/GC
    Reglas simples:
    - 3 puntos por victoria, 1 por empate, 0 por derrota
    - PJ/PG/PE/PP, GF, GC y Dif (GF-GC)
    - Bonus queda en 0 por ahora (puede derivar luego de otras reglas)
    """
    # 1) Obtener partidos según filtros
    filtros = {}
    if torneo:
        filtros['torneo'] = torneo
    if division:
        filtros['categoria'] = division
    partidos = PartidoRepository.buscar(filtros)
    if fecha:
        try:
            fecha_int = int(fecha)
            partidos = [p for p in partidos if (p.fecha_numero or 0) <= fecha_int]
        except Exception:
            pass

    # Nota: si no hay partidos, igualmente mostraremos los equipos de la categoría con stats en cero

    # 2) Cargar goles por partido desde Incidencias
    partido_ids = [p.id for p in partidos]
    goles = IncidenciaRepository.listar_goles_por_partidos(partido_ids) if partido_ids else []

    # Map: partido_id -> {club_id: goles}
    goles_por_partido = defaultdict(lambda: defaultdict(int))
    for inc in goles:
        # cada gol suma +1 al club de la incidencia
        goles_por_partido[inc.partido_id][inc.club_id] += 1

    # 3) Acumular estadísticas por equipo
    tabla = defaultdict(lambda: {
        'equipo_id': None,
        'club_id': None,
        'equipo': None,  # nombre del equipo
        'club': None,    # nombre del club
        'categoria': division or '',
        'pj': 0, 'pg': 0, 'pe': 0, 'pp': 0,
        'gf': 0, 'gc': 0, 'dif': 0,
        'bonus': 0,
        'pts': 0,
        'zona': 'A',
        'logo': None,
    })

    partidos_con_goles = {g.partido_id for g in goles}

    # Obtener todos los equipos de la categoría
    equipos_cat = EquipoRepository.buscar_por_categoria(division)
    equipos_por_club = defaultdict(list)
    equipos_por_id = {}
    for eq in equipos_cat:
        equipos_por_club[eq.club_id].append(eq)
        equipos_por_id[eq.id] = eq

    # Procesar partidos y asignar estadísticas por equipo
    for p in partidos:
        if not (p.estado == 'jugado' or p.id in partidos_con_goles):
            continue
        # Buscar equipos locales y visitantes en la categoría
        # Si el partido tiene equipo_*_id, lo usamos para diferenciar A/B/C; si no, buscamos por club
        eq_local = equipos_por_id.get(getattr(p, 'equipo_local_id', None)) if getattr(p, 'equipo_local_id', None) else None
        eq_vis = equipos_por_id.get(getattr(p, 'equipo_visitante_id', None)) if getattr(p, 'equipo_visitante_id', None) else None
        if not eq_local:
            eq_local = next((eq for eq in equipos_cat if eq.club_id == p.club_local_id and (eq.categoria == division)), None)
        if not eq_vis:
            eq_vis = next((eq for eq in equipos_cat if eq.club_id == p.club_visitante_id and (eq.categoria == division)), None)
        # Si no se encuentra el equipo, continuar
        if not eq_local or not eq_vis:
            continue
        loc = goles_por_partido.get(p.id, {}).get(p.club_local_id, 0)
        vis = goles_por_partido.get(p.id, {}).get(p.club_visitante_id, 0)
        if loc == 0 and vis == 0 and p.estado == 'jugado':
            loc = p.goles_local or 0
            vis = p.goles_visitante or 0

        # Local
        tloc = tabla[eq_local.id]
        tloc['equipo_id'] = eq_local.id
        tloc['club_id'] = eq_local.club_id
        tloc['equipo'] = eq_local.nombre
        tloc['club'] = eq_local.club.nombre if eq_local.club else f"Club {eq_local.club_id}"
        tloc['categoria'] = eq_local.categoria or division or ''
        tloc['pj'] += 1
        tloc['gf'] += loc
        tloc['gc'] += vis
        # Visitante
        tvis = tabla[eq_vis.id]
        tvis['equipo_id'] = eq_vis.id
        tvis['club_id'] = eq_vis.club_id
        tvis['equipo'] = eq_vis.nombre
        tvis['club'] = eq_vis.club.nombre if eq_vis.club else f"Club {eq_vis.club_id}"
        tvis['categoria'] = eq_vis.categoria or division or ''
        tvis['pj'] += 1
        tvis['gf'] += vis
        tvis['gc'] += loc

        # Resultado para PG/PE/PP y puntos
        if loc > vis:
            tloc['pg'] += 1
            tvis['pp'] += 1
            tloc['pts'] += 3
        elif vis > loc:
            tvis['pg'] += 1
            tloc['pp'] += 1
            tvis['pts'] += 3
        else:
            tloc['pe'] += 1
            tvis['pe'] += 1
            tloc['pts'] += 1
            tvis['pts'] += 1

    # 4) Completar DIF y ordenar
    filas = []
    # Agregar equipos de la categoría aunque no tengan partidos
    for eq in equipos_cat:
        if eq.id not in tabla:
            tabla[eq.id] = {
                'equipo_id': eq.id,
                'club_id': eq.club_id,
                'equipo': eq.nombre,
                'club': eq.club.nombre if eq.club else f"Club {eq.club_id}",
                'categoria': eq.categoria or division or '',
                'pj': 0, 'pg': 0, 'pe': 0, 'pp': 0,
                'gf': 0, 'gc': 0, 'dif': 0,
                'bonus': 0, 'pts': 0,
                'zona': 'A', 'logo': None
            }

    # Si es categoría Caballeros y falta CUAM, la incorporamos manualmente con valores en cero
    if division and division.lower().startswith('caballeros'):
        nombre_normalizados = { (v['equipo'] or '').lower(): k for k,v in tabla.items() }
        if 'cuam' not in nombre_normalizados:
            fake_id = -9999  # id ficticio para fila virtual
            tabla[fake_id] = {
                'equipo_id': fake_id,
                'club_id': fake_id,
                'equipo': 'Cuam',
                'club': 'Cuam',
                'categoria': division or '',
                'pj': 0, 'pg': 0, 'pe': 0, 'pp': 0,
                'gf': 0, 'gc': 0, 'dif': 0,
                'bonus': 0, 'pts': 0,
                'zona': 'A', 'logo': None
            }
    for equipo_id, row in tabla.items():
        row['dif'] = row['gf'] - row['gc']
        filas.append(row)

    filas.sort(key=lambda r: (r['pts'], r['dif'], r['gf'], r['equipo']), reverse=True)

    # 5) Generar salida con posición
    # Selección robusta de logo: patrones por substring para cubrir sufijos (A/B/C) en nombres de equipos
    logo_patterns = [
        ('cuadro nacional', 'CuadroNacional.png'),
        ('banco municipal', 'Banco Municipal.png'),
        ('banco mendoza', 'BancoMendoza.png'),
        ('belgrano', 'Belgrano.png'),
        ('maristas', 'Maristas.png'),
        ('san jorge', 'SanJorge.png'),
        ('tenis club', 'TenisClub.png'),
        ('volantes', 'Volantes.png'),
        ('guerreras goudge', 'Guerreras Goudge.png'),
        ('goudge', 'Goudge.png'),
        ('deportivo argentino', 'DeportivoArgentino.png'),
        ('xeneizes', 'Xeneizes.png'),
        ('ateneo', 'Ateneo.png'),
        ('cuam', 'logo-asociacion.png'),  # placeholder si no hay logo propio
    ]
    salida = []
    for i, r in enumerate(filas, start=1):
        nombre_lower = (r['equipo'] or '').lower()
        club_lower = (r.get('club') or '').lower()
        logo_file = None
        for pattern, file in logo_patterns:
            if pattern in nombre_lower or pattern in club_lower:
                logo_file = file
                break
        salida.append({
            'pos': i,
            'equipo_id': r['equipo_id'],
            'logo': f"/static/assets/img/{logo_file}" if logo_file else None,
            'zona': r['zona'],
            'equipo': r['equipo'],
            'club': r.get('club'),
            'categoria': r.get('categoria', division or ''),
            'pj': r['pj'], 'pg': r['pg'], 'pe': r['pe'], 'pp': r['pp'],
            'gf': r['gf'], 'ge': r['gc'], 'dif': r['dif'],
            'bonus': r['bonus'], 'pts': r['pts']
        })
    return salida
