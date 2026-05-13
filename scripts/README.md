# 🛠️ Scripts de Mantenimiento - Hockey Acción

Descripción y uso de todos los scripts de administración del proyecto.

---

## 📋 Resumen rápido

| Script | Descripción | Crítico |
|--------|-------------|---------|
| `verify_setup.py` | Verifica configuración antes de arrancar | ✅ |
| `setup_mongodb_indexes.py` | Crea/verifica índices de MongoDB | ✅ |
| `init_project.py` | Inicialización completa (conexión, índices, usuario) | ✅ |
| `crear_usuario_generico.py` | Crea usuarios con permisos específicos | ⚠️ |
| `modificar_contrasena.py` | Cambia contraseña de usuario | ⚠️ |

---

## 🔍 `verify_setup.py`

**Propósito:** Verificar que el proyecto está configurado correctamente antes de arrancar.

### Uso

```bash
# Verificación completa
python scripts/verify_setup.py

# O en Docker
docker compose exec app python scripts/verify_setup.py
```

### Qué verifica

- ✅ Archivo `.env` existe
- ✅ Variables de entorno críticas (`FLASK_ENV`, `MONGO_URI`, `SECRET_KEY`)
- ✅ Conexión a MongoDB
- ✅ Colecciones necesarias existen
- ✅ Índices creados correctamente

### Exit codes

- `0` = Todo OK, proyecto listo
- `1` = Error crítico, no puedes arrancar
- `2` = Advertencias (puedes arrancar pero falta algo)

### Ejemplos de salida

```
✅ Archivo .env encontrado
✅ Todas las variables críticas definidas
✅ MongoDB accesible
✅ Colecciones existentes: usuarios, clubes, equipos, partidos
⚠️  Colecciones faltantes: noticias
⚠️  Algunos índices no están creados
```

---

## 🗄️ `setup_mongodb_indexes.py`

**Propósito:** Crear y gestionar índices de MongoDB para optimizar rendimiento.

### Uso

```bash
# Crear/verificar índices (recomendado primera vez)
python scripts/setup_mongodb_indexes.py

# Verificar índices existentes sin modificar
python scripts/setup_mongodb_indexes.py --verify

# Resetear todos los índices (excepto _id) y recrear
python scripts/setup_mongodb_indexes.py --reset

# En Docker
docker compose exec app python scripts/setup_mongodb_indexes.py
```

### Índices creados

**Índices únicos (evitan duplicados):**
- `usuarios.username` - No permiten dos usuarios con mismo nombre
- `clubes.nombre` - No permiten dos clubes con mismo nombre
- `equipos.nombre` - No permiten dos equipos con mismo nombre
- `torneo.nombre` - No permiten dos torneos con mismo nombre

**Índices de búsqueda:**
- `partidos.fecha` - Ordena por fecha (más reciente primero)
- `partidos.torneo_id` - Búsqueda rápida por torneo
- `partidos.equipo_local_id` - Búsqueda por equipo local
- `partidos.equipo_visitante_id` - Búsqueda por equipo visitante
- `incidencias.partido_id` - Búsqueda rápida por partido
- `incidencias.jugadora_id` - Búsqueda por jugadora
- `incidencias.tipo_incidencia` - Búsqueda por tipo
- `noticias.fecha` - Ordena por fecha (más reciente primero)
- `jugadora.nombre` - Búsqueda por nombre
- `equipos.club_id` - Búsqueda por club

### Mejora de rendimiento

Estos índices optimizan consultas como:

```python
# Búsqueda rápida gracias a índice username
usuario = db.usuarios.find_one({'username': 'admin'})

# Listado ordenado por fecha (rápido)
partidos = db.partidos.find().sort('fecha', -1).limit(10)

# Búsqueda por relación (rápido)
incidencias = db.incidencias.find({'partido_id': ObjectId('...')})
```

---

## 🚀 `init_project.py`

**Propósito:** Inicialización completa del proyecto en una sola ejecución.

### Uso

```bash
# Modo interactivo (pregunta para cada paso)
python scripts/init_project.py

# Ejecutar todo automáticamente
python scripts/init_project.py --all

# Sin crear índices (si ya existen)
python scripts/init_project.py --skip-indexes

# Solo crear usuario admin
python scripts/init_project.py --create-admin

# En Docker
docker compose exec app python scripts/init_project.py --all
```

### Qué realiza

1. ✅ Verifica conexión a MongoDB
2. ✅ Crea índices en colecciones críticas
3. ✅ Crea usuario admin (interactivo o automático)
4. ✅ (Opcional) Crea club de ejemplo
5. ✅ Muestra reporte final con documentos por colección

### Exemplo de ejecución automática

```bash
docker compose exec app python scripts/init_project.py --all
```

Salida:

```
======================================================================
🏒 INICIALIZACIÓN - HOCKEY ACCIÓN
======================================================================

✅ Conexión a MongoDB exitosa

======================================================================
🏒 INICIALIZANDO ÍNDICES
======================================================================

📋 Colección: usuarios
  ✓ Username único
  ✓ Búsqueda de admins
  ✓ Búsqueda de operadores

...

✅ Usuario admin 'admin' creado exitosamente
   ID: 507f1f77bcf86cd799439011

✅ Club 'Club Ejemplo' creado exitosamente
   ID: 507f1f77bcf86cd799439012

======================================================================
RESUMEN DE INICIALIZACIÓN
======================================================================

📊 Estado de colecciones:
  ✅ usuarios: 1 documentos
  ✅ clubes: 1 documentos
  ⚠️  equipos: 0 documentos
  ⚠️  partidos: 0 documentos
  ⚠️  noticias: 0 documentos

⏰ Inicialización completada: 2026-05-12 14:35:22

✅ Inicialización completada exitosamente
```

---

## 👤 `crear_usuario_generico.py`

**Propósito:** Crear usuarios con permisos específicos.

### Uso

```bash
# Usuario operador (admin sin club)
python scripts/crear_usuario_generico.py \
  --username admin \
  --password MiContraseña123 \
  --operador \
  --puede-cargar-incidencias \
  --puede-precargar-equipos

# Usuario de club
python scripts/crear_usuario_generico.py \
  --username SanJorge.sr \
  --password Contraseña456 \
  --club "San Jorge"

# Usuario solo lectura
python scripts/crear_usuario_generico.py \
  --username visualizador \
  --password MiContraseña789

# En Docker
docker compose exec app python scripts/crear_usuario_generico.py \
  --username admin --password Contraseña123 --operador
```

### Opciones

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--username` | Nombre de usuario | `admin` |
| `--password` | Contraseña en texto plano | `MiContraseña123` |
| `--club` | Club a asociar (opcional) | `"San Jorge"` |
| `--operador` | Permiso de operador general | (flag) |
| `--puede-cargar-incidencias` | Permiso de cargar incidencias | (flag) |
| `--puede-precargar-equipos` | Permiso de precargar equipos | (flag) |

### Ejemplos

```bash
# Admin con todos los permisos
python scripts/crear_usuario_generico.py --username admin --password Admin123 --operador --puede-cargar-incidencias --puede-precargar-equipos

# Usuario de club (sin permisos especiales)
python scripts/crear_usuario_generico.py --username Club.sr --password Club123 --club "Mi Club"

# Operador de mesa de control
python scripts/crear_usuario_generico.py --username mesa1 --password Mesa123 --operador --puede-cargar-incidencias
```

---

## 🔐 `modificar_contrasena.py`

**Propósito:** Cambiar la contraseña de un usuario existente.

### Uso

```bash
# 1. Editar el archivo (cambiar variables en if __name__ == '__main__')
notepad scripts/modificar_contrasena.py

# 2. Ejecutar
python scripts/modificar_contrasena.py

# O en Docker
docker compose exec app python scripts/modificar_contrasena.py
```

### Edición del archivo

```python
if __name__ == '__main__':
    usuario = 'SanJorge.sr'              # Usuario a modificar
    nueva_contrasena = 'NuevaPass456'     # Nueva contraseña
    modificar_contrasena(usuario, nueva_contrasena)
```

---

## 🔧 Scripts legacy (ya no se usan)

Estos scripts están marcados como legacy y NO DEBEN USARSE (están aquí solo por historial):

- `create_schema_mariadb.py` - Legacy (MariaDB)
- `crear_tabla_incidencias.py` - Legacy (SQLAlchemy)
- `migrate_postgres_to_mariadb.py` - Legacy (migración SQL)
- `verify_migration_counts.py` - Legacy (verificación SQL)

---

## 📝 Flujo de inicialización recomendado

### Primera vez (nuevo ambiente)

```bash
# 1. Levantar Docker Compose
docker compose up --build

# 2. Esperar a que MongoDB esté listo (mirar logs)
docker compose logs mongodb | grep "Waiting for connections"

# 3. Verificar setup
docker compose exec app python scripts/verify_setup.py

# 4. Inicializar todo
docker compose exec app python scripts/init_project.py --all

# 5. Acceder a http://localhost:5000
```

### Agregar nuevo usuario después

```bash
docker compose exec app python scripts/crear_usuario_generico.py \
  --username usuario.nuevo \
  --password ContrasenaSegura123 \
  --club "Mi Club"
```

### Resetear contraseña olvidada

```bash
# 1. Editar scripts/modificar_contrasena.py

# 2. Ejecutar
docker compose exec app python scripts/modificar_contrasena.py
```

---

## ⚠️ Notas importantes

- **Contraseñas:** Usar contraseñas fuertes en producción
- **Índices:** Solo ejecutar `--reset` si es NECESARIO (interrupción breve de servicio)
- **Usuarios:** No es posible editar usuarios, solo crearlos. Para cambiar: crear nuevo + borrar manual
- **Backups:** Hacer backup de MongoDB antes de operaciones críticas

---

## 🔗 Relacionados

- [SETUP.md](SETUP.md) - Guía de configuración completa
- [README.md](../README.md) - Documentación general del proyecto
- `.env.example` - Plantilla de variables de entorno
