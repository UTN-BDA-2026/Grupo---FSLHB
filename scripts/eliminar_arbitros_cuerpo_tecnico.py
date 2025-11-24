from app import app, db
from app.models.cuerpo_tecnico import CuerpoTecnico


def eliminar_arbitros():
    """
    Elimina todos los registros de CuerpoTecnico con rol='ARB' (Árbitro).
    Muestra el total afectado.
    """
    with app.app_context():
        rows = CuerpoTecnico.query.filter_by(rol='ARB').all()
        total = len(rows)
        if total == 0:
            print('No hay árbitros para eliminar (rol=ARB).')
            return
        for r in rows:
            db.session.delete(r)
        db.session.commit()
        print(f'Eliminados {total} registros de árbitros (rol=ARB) de CuerpoTecnico.')


if __name__ == '__main__':
    eliminar_arbitros()
