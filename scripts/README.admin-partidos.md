# Admin: Carga de Partidos

Solo el programador puede crear partidos. Hay dos formas:

## 1) Script CSV (recomendado)

Archivo: `scripts/admin_cargar_partidos.py`

Formato CSV (cabeceras):

```
torneo,categoria,fecha_numero,bloque,fecha_hora,cancha,equipo_local_nombre,equipo_visitante_nombre
```

- `torneo`: Ej. `Clausura Damas (2025)`
- `categoria`: `damas_a` | `damas_b` | `damas_c` | `caballeros` | `mamis`
- `fecha_numero`: número de fecha (opcional)
- `bloque`: letra/identificador (opcional)
- `fecha_hora`: ISO `YYYY-MM-DDTHH:MM` (opcional)
- `cancha`: texto (opcional)
- `equipo_local_nombre` | `equipo_visitante_nombre`: nombres exactos de equipos existentes

Ejemplo: `scripts/ejemplos/partidos_ejemplo.csv`

### Ejecutar

Desde la raíz del proyecto (con el entorno configurado):

```
python -m scripts.admin_cargar_partidos scripts/ejemplos/partidos_ejemplo.csv
```

> El script usa el contexto Flask definido en `app/__init__.py` y crea los registros en la base.

## 2) Endpoint API (protegido)

`POST /partidos` (solo con header `X-Admin-Key` igual a `ADMIN_API_KEY` en env)

Body JSON mínimo:

```json
{
  "torneo": "Clausura Damas (2025)",
  "categoria": "damas_b",
  "equipo_local_id": 1,
  "equipo_visitante_id": 2,
  "fecha_hora": "2025-10-11T16:30"
}
```

Respuestas de error comunes:
- 401: `No autorizado` (falta o no coincide `X-Admin-Key`)
- 400: `Faltan campos: ...` | `Formato de fecha_hora inválido` | `El equipo local y visitante no pueden ser el mismo`

## Notas
- Asegúrese de que los equipos existan previamente con nombres y categorías correctos.
- Las categorías deben coincidir con las usadas en la web (`damas_a`, `damas_b`, `damas_c`, `caballeros`, `mamis`).
- Después de cargar partidos, aparecen automáticamente en la Precarga y Carga de Incidencias.
