from app.resources.club_resource import clubs_bp
from app.resources.jugadora_resource import jugadora_bp
from app.resources.resultado_resource import resultado_bp
from app.resources.usuario_resource import usuario_bp
from app.resources.equipo_resource import equipo_bp
from app.resources.categorias_resource import categorias_bp
from app.resources.posiciones_resource import posiciones_bp
from app.resources.torneo_resource import torneo_bp
from app.resources.noticia_resource import noticia_bp
from app.resources.partido_resource import partido_bp
from app.resources.incidencia_resource import incidencia_bp
from app.resources.cuerpo_tecnico_resource import bp_cuerpo_tecnico
from app.resources.arbitro_resource import arbitro_bp
from app.resources.resultados_resource import resultados_bp
from app.routes_static import static_bp

ALL_BLUEPRINTS = [
    clubs_bp,
    jugadora_bp,
    resultado_bp,
    usuario_bp,
    equipo_bp,
    categorias_bp,
    posiciones_bp,
    torneo_bp,
    noticia_bp,
    partido_bp,
    incidencia_bp,
    bp_cuerpo_tecnico,
    arbitro_bp,
    resultados_bp,
    static_bp,
]
