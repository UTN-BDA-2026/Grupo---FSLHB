from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Set, Tuple

from app.models.partido import Partido
from app.repositories.partido_repositorio import PartidoRepository
from app.repositories.incidencia_repositorio import IncidenciaRepository


class SancionService:
    """Calcula suspensiones por tarjetas para un partido y club.

    Reglas:
    - Roja: 1 partido de suspensión (inmediato próximo partido del club en el mismo torneo/categoría).
    - 3 Amarillas acumuladas: 1 partido de suspensión al alcanzar múltiplo de 3.
    - 5 Verdes acumuladas: 1 partido de suspensión al alcanzar múltiplo de 5.

    Notas de alcance:
    - El cálculo se limita al mismo torneo y categoría del partido objetivo.
    - La suspensión aplica solo al partido inmediatamente posterior al que gatilló la sanción.
    - Si un jugador alcanza el umbral en un partido anterior y ya habría cumplido en el siguiente,
      no se arrastra a partidos posteriores.
    """

    @staticmethod
    def jugadores_suspendidos_para_partido(partido_id: int, club_id: int) -> List[dict]:
        # Obtener partido objetivo
        p: Partido = PartidoRepository.buscar_por_id(partido_id)
        if not p:
            return []

        # Partidos de ese torneo/categoría donde participa el club
        partidos = PartidoRepository.buscar({
            'torneo': p.torneo,
            'categoria': p.categoria,
            'club_id': club_id,
        })

        # Orden consistente: por fecha_numero (si existe), luego fecha_hora, luego id
        def sort_key(px: Partido):
            fn = getattr(px, 'fecha_numero', None)
            return (
                10**9 if fn is None else int(fn),
                getattr(px, 'fecha_hora', None) or 0,
                int(getattr(px, 'id', 0) or 0)
            )

        partidos = sorted(partidos, key=sort_key)
        if not partidos:
            return []

        # Ubicar el partido dentro de la secuencia
        try:
            idx = [px.id for px in partidos].index(partido_id)
        except ValueError:
            return []
        if idx == 0:
            # No hay partido anterior => nunca hay suspensión aplicable
            return []

        prev_partido_ids = [px.id for px in partidos[:idx - 1]]  # partidos ANTES del previo
        last_partido_id = partidos[idx - 1].id                     # partido inmediatamente anterior

        # Incidencias de todos los partidos previos (mismo torneo/categoría) del club
        consider_ids = prev_partido_ids + [last_partido_id]
        if not consider_ids:
            return []

        incidencias = IncidenciaRepository.ranking_resumen(p.torneo, p.categoria, fecha_hasta=None)
        # Filtrar: solo del club y solo de partidos en consider_ids
        incidencias = [i for i in incidencias if i.club_id == club_id and i.partido_id in consider_ids and i.tipo == 'tarjeta']

        # Contadores acumulados hasta el partido anterior al último
        amarillas_prev: Dict[int, int] = defaultdict(int)
        verdes_prev: Dict[int, int] = defaultdict(int)
        # En el partido último (inmediato anterior al objetivo)
        amarillas_last: Dict[int, int] = defaultdict(int)
        verdes_last: Dict[int, int] = defaultdict(int)
        roja_last: Set[int] = set()

        for inc in incidencias:
            if inc.partido_id == last_partido_id:
                if inc.color == 'amarilla':
                    amarillas_last[inc.jugadora_id] += 1
                elif inc.color == 'verde':
                    verdes_last[inc.jugadora_id] += 1
                elif inc.color == 'roja':
                    roja_last.add(inc.jugadora_id)
            else:
                if inc.color == 'amarilla':
                    amarillas_prev[inc.jugadora_id] += 1
                elif inc.color == 'verde':
                    verdes_prev[inc.jugadora_id] += 1
                # rojas en partidos anteriores no impactan aquí (ya debieron cumplirse)

        suspendidos: List[dict] = []
        # Reglas de suspensión basadas en el partido inmediatamente anterior
        jugadores = set(list(amarillas_prev.keys()) + list(amarillas_last.keys()) + list(verdes_prev.keys()) + list(verdes_last.keys()) + list(roja_last))
        for jid in jugadores:
            motivo = None
            if jid in roja_last:
                motivo = 'roja'
            else:
                a_prev = amarillas_prev.get(jid, 0)
                a_now = a_prev + amarillas_last.get(jid, 0)
                if (a_prev // 3) < (a_now // 3) and amarillas_last.get(jid, 0) > 0:
                    motivo = '3_amarillas'
                else:
                    v_prev = verdes_prev.get(jid, 0)
                    v_now = v_prev + verdes_last.get(jid, 0)
                    if (v_prev // 5) < (v_now // 5) and verdes_last.get(jid, 0) > 0:
                        motivo = '5_verdes'
            if motivo:
                suspendidos.append({'jugadora_id': jid, 'motivo': motivo})

        return suspendidos
