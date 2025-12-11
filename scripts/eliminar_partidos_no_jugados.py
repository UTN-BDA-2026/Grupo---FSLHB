"""Script para eliminar partidos no jugados.

Criterio de eliminación (por defecto):
  - estado = 'programado'
  - fecha_hora es anterior a ahora
  - goles_local y goles_visitante son NULL (None)

Se puede ajustar con flags:
  --solo-estado ESTADO    Cambia el estado que se considera como no jugado (default: programado)
  --incluir-sin-fecha     También elimina partidos sin fecha_hora (NULL) si cumplen estado y sin goles
  --dry-run               No elimina, solo muestra cuantos y sus IDs
  --confirm               Requerido para ejecutar el borrado efectivo (sin dry-run)
  --antes YYYY-MM-DD      Sólo considera partidos con fecha_hora antes de esa fecha (en vez de ahora)

Uso ejemplos (PowerShell):
  python scripts/eliminar_partidos_no_jugados.py --dry-run
  python scripts/eliminar_partidos_no_jugados.py --confirm
  python scripts/eliminar_partidos_no_jugados.py --solo-estado pendiente --confirm
  python scripts/eliminar_partidos_no_jugados.py --antes 2025-10-01 --dry-run

IMPORTANTE: Haz backup antes (ver scripts/backup_db.py).
"""

from __future__ import annotations
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Asegura que el directorio raíz (que contiene el paquete 'app') esté en sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
root_str = str(ROOT_DIR)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

from app import app, db  # noqa: E402
from app.models.partido import Partido  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Eliminar partidos no jugados según criterios.")
    parser.add_argument("--solo-estado", default="programado", help="Estado que se considera no jugado (default: programado)")
    parser.add_argument("--incluir-sin-fecha", action="store_true", help="Incluir partidos sin fecha_hora (NULL)")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar coincidencias sin borrar")
    parser.add_argument("--confirm", action="store_true", help="Confirmar borrado (requerido si no es dry-run)")
    parser.add_argument("--antes", help="Usar una fecha corte YYYY-MM-DD en vez de 'ahora'")
    parser.add_argument("--id", type=int, help="Eliminar solo el partido con este ID (ignora criterios)")
    parser.add_argument("--ids", help="Eliminar varios IDs separados por comas (ignora criterios)")
    return parser.parse_args()


def obtener_corte(args: argparse.Namespace) -> datetime:
    if args.antes:
        try:
            return datetime.strptime(args.antes, "%Y-%m-%d")
        except ValueError:
            print("Formato inválido para --antes. Usa YYYY-MM-DD", file=sys.stderr)
            sys.exit(2)
    return datetime.utcnow()


def construir_query(args: argparse.Namespace, corte: datetime):
    q = Partido.query.filter(Partido.estado == args.solo_estado)
    # Sin goles aún
    q = q.filter(Partido.goles_local.is_(None), Partido.goles_visitante.is_(None))
    # Fecha pasada
    if args.incluir_sin_fecha:
        q = q.filter(
            db.or_(Partido.fecha_hora.is_(None), Partido.fecha_hora < corte)
        )
    else:
        q = q.filter(Partido.fecha_hora.isnot(None), Partido.fecha_hora < corte)
    return q


def main():
    args = parse_args()
    corte = obtener_corte(args)
    modo_ids = bool(args.id) or bool(args.ids)
    if modo_ids:
        print("Modo eliminación por IDs explícitos (se ignoran criterios de estado/fecha).")
    else:
        print(f"Criterios: estado='{args.solo_estado}', corte={corte.isoformat()}, incluir_sin_fecha={args.incluir_sin_fecha}")

    with app.app_context():
        if modo_ids:
            id_list = []
            if args.id:
                id_list.append(args.id)
            if args.ids:
                try:
                    id_list.extend(int(x.strip()) for x in args.ids.split(',') if x.strip())
                except ValueError:
                    print("Error: --ids debe contener enteros separados por comas", file=sys.stderr)
                    sys.exit(2)
            id_list = sorted(set(id_list))
            if not id_list:
                print("No se proporcionaron IDs válidos.")
                return
            partidos = Partido.query.filter(Partido.id.in_(id_list)).all()
            faltantes = set(id_list) - {p.id for p in partidos}
            if faltantes:
                print(f"Advertencia: IDs inexistentes en la base: {sorted(faltantes)}")
        else:
            q = construir_query(args, corte)
            partidos = q.all()
        if not partidos:
            print("No se encontraron partidos no jugados según criterio.")
            return
        print(f"Encontrados {len(partidos)} partidos candidatos:")
        for p in partidos[:50]:  # limitar listado
            print(f"  ID={p.id} torneo={p.torneo} categoria={p.categoria} fecha_hora={p.fecha_hora} estado={p.estado}")
        if len(partidos) > 50:
            print(f"  ... ({len(partidos)-50} más)")

        if args.dry_run:
            print("Dry-run: no se elimina nada.")
            return
        if not args.confirm:
            print("Falta --confirm para proceder al borrado (o usa --dry-run para simular).")
            return
        # Borrado
        ids = [p.id for p in partidos]
        print(f"Eliminando {len(ids)} partidos (IDs: primeros 20: {ids[:20]})...")
        for p in partidos:
            db.session.delete(p)
        db.session.commit()
        print("Borrado completado.")


if __name__ == "__main__":
    main()
