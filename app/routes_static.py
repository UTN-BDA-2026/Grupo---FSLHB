
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app import require_admin

static_bp = Blueprint('static_pages', __name__)

@static_bp.route('/')
def index():
    return render_template('index.html')

@static_bp.route('/autoridades')
def autoridades():
    return render_template('autoridades.html')

@static_bp.route('/reglamento')
def reglamento():
    return render_template('reglamento.html')

@static_bp.route('/historial')
def historial():
    return render_template('historial.html')

@static_bp.route('/contacto')
def contacto():
    return render_template('contacto.html')

@static_bp.route('/galeria')
def galeria():
    # Lógica original de galería movida desde __init__.py
    try:
        data = api_galeria()
        if isinstance(data, tuple):
            payload = data[0] or {}
        else:
            payload = data or {}
        imagenes = payload.get('imagenes', [])
    except Exception:
        imagenes = []
    galerias = [
        {
            "titulo": "Campeones del Torneo Clausura 2025",
            "imagenes": [
                {
                    "thumbnail": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_300,h_200,c_fill,g_auto/6_yskusd.jpg",
                    "full": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_1600/6_yskusd.jpg",
                    "id": "6_yskusd"
                },
                {
                    "thumbnail": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_300,h_200,c_fill,g_auto/5_dorzog.jpg",
                    "full": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_1600/5_dorzog.jpg",
                    "id": "5_dorzog"
                },
                {
                    "thumbnail": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_300,h_200,c_fill,g_auto/3_d2lesa.jpg",
                    "full": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_1600/3_d2lesa.jpg",
                    "id": "3_d2lesa"
                },
                {
                    "thumbnail": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_300,h_200,c_fill,g_auto/4_igki5a.jpg",
                    "full": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_1600/4_igki5a.jpg",
                    "id": "4_igki5a"
                },
                {
                    "thumbnail": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_300,h_200,c_fill,g_auto/1_upprui.jpg",
                    "full": "https://res.cloudinary.com/drfomm1hf/image/upload/f_auto,q_auto,w_1600/1_upprui.jpg",
                    "id": "1_upprui"
                }
            ]
        }
    ]
    return render_template('galeria.html', galerias=galerias)


# API galería movida desde __init__.py
@static_bp.route('/api/galeria')
def api_galeria():
    """Devuelve lista de imágenes de Cloudinary carpeta HockeySanRafael.
    Usa Search API y hace fallback a api.resources si Search falla o no indexó aún.
    Requiere CLOUDINARY_URL en entorno (cloudinary://API_KEY:API_SECRET@cloud_name)."""
    FOLDER = 'HockeySanRafael'
    try:
        import cloudinary
        from cloudinary import search, api
        # Validar configuración
        # Reducir timeouts para evitar bloqueos en DNS/red
        cloudinary.config(timeout=7)
        cfg = cloudinary.config()
        if not cfg.cloud_name:
            # Responder 200 con lista vacía para no romper UI
            return {"error": "Cloudinary no configurado (falta CLOUDINARY_URL)", "imagenes": [], "debug": {"stage": "config"}}, 200

        imagenes = []
        recursos = []
        # Intentar Search (puede tardar en indexar primeras subidas)
        try:
            resultado = search.Search()\
                .expression(f'folder={FOLDER}')\
                .sort_by('created_at','desc')\
                .max_results(80)\
                .execute()
            recursos = resultado.get('resources', []) or []
        except Exception as se:
            recursos = []
            search_error = str(se)

        # Fallback si search vacío
        if not recursos:
            try:
                res_api = api.resources(type='upload', resource_type='image', prefix=FOLDER+'/', max_results=80)
                recursos = res_api.get('resources', []) or []
            except Exception as ae:
                try:
                    global_res = api.resources(type='upload', resource_type='image', max_results=50)
                    recursos = global_res.get('resources', []) or []
                    fallback_used = True
                except Exception as ge:
                    return {"error": f"Cloudinary API error: {ae}", "imagenes": [], "debug": {"api_error": str(ae), "global_error": str(ge), "search_error": search_error if 'search_error' in locals() else None}}, 200
            else:
                fallback_used = False
        else:
            fallback_used = False

        base = f"https://res.cloudinary.com/{cfg.cloud_name}/image/upload"
        for r in recursos:
            public_id = r.get('public_id')
            formato = r.get('format')
            if not public_id:
                continue
            thumb = f"{base}/f_auto,q_auto,w_300,h_200,c_fill,g_auto/{public_id}.{formato}" if formato else f"{base}/f_auto,q_auto,w_300,h_200,c_fill,g_auto/{public_id}"
            full = f"{base}/f_auto,q_auto,w_1600/{public_id}.{formato}" if formato else f"{base}/f_auto,q_auto,w_1600/{public_id}"
            imagenes.append({
                "id": public_id,
                "thumbnail": thumb,
                "full": full,
                "format": formato,
                "created_at": r.get('created_at')
            })
        return {"imagenes": imagenes, "debug": {"count": len(imagenes), "fallback_global": fallback_used, "search_error": search_error if 'search_error' in locals() else None}}
    except Exception as e:
        return {"error": f"Excepción general: {e}", "imagenes": [], "debug": {"exception": str(e)}}, 200

@static_bp.route('/club-panel')
def club_panel():
    return render_template('club-panel.html')


@static_bp.route('/admin-panel')
@login_required
def admin_panel():
    if not getattr(current_user, 'is_admin', False):
        return render_template('403.html'), 403
    return render_template('admin-panel.html')


@static_bp.route('/admin/noticias')
@require_admin
def admin_noticias():
    return render_template('admin-noticias.html')

@static_bp.route('/noticias')
def noticias():
    return render_template('noticias.html')

@static_bp.route('/calendario')
def calendario():
    return render_template('calendario.html')

@static_bp.route('/clubes')
def clubes():
    return render_template('clubes.html')

@static_bp.route('/equipos')
def equipos():
    return render_template('equipos.html')

@static_bp.route('/sponsors')
def sponsors():
    return render_template('sponsors.html')

@static_bp.route('/login')
def login_page():
    return render_template('login.html')

@static_bp.route('/panel-clubes')
@login_required
def panel_clubes():
    return render_template('panel-clubes.html')

@static_bp.route('/precarga-equipos')
@login_required
def precarga_equipos():
    return render_template('precarga-equipos.html')

@static_bp.route('/crear-lista-buena-fe')
@login_required
def crear_lista_buena_fe():
    try:
        if getattr(current_user, 'club_id', None) is None:
            return render_template('403.html'), 403
    except Exception:
        return render_template('403.html'), 403
    return render_template('crear-lista-buena-fe.html')

@static_bp.route('/jugadores')
@login_required
def jugadores():
    return render_template('jugadores.html')

@static_bp.route('/equipos-categorias')
@login_required
def equipos_categorias():
    return render_template('equipos-categorias.html')

@static_bp.route('/datos-club')
@login_required
def datos_club():
    return render_template('datos-club.html')

@static_bp.route('/carga-incidencias')
@login_required
def carga_incidencias():
    return render_template('carga-incidencias.html')

@static_bp.route('/cuerpo-tecnico')
@login_required
def cuerpo_tecnico():
    return render_template('cuerpo-tecnico.html')

@static_bp.route('/control-partido')
@login_required
def control_partido():
    return render_template('control-partido.html')

@static_bp.route('/.well-known/appspecific/com.chrome.devtools.json')
def chrome_devtools_probe():
    return ('', 204)
