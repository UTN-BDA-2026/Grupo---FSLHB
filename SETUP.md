# 🏒 Guía de Configuración e Inicialización - Hockey Acción

Esta guía te ayudará a configurar y poner en marcha el proyecto completo con MongoDB.

---

## 📋 Tabla de contenidos

1. [Requisitos previos](#requisitos-previos)
2. [Configuración inicial](#configuración-inicial)
3. [Inicialización del proyecto](#inicialización-del-proyecto)
4. [Scripts disponibles](#scripts-disponibles)
5. [Solución de problemas](#solución-de-problemas)

---

## Requisitos previos

- **Docker** y **Docker Compose** instalados
- **Git** (para clonar el proyecto)
- **Python 3.11+** (para desarrollo local, opcional)

### Verificar instalación

```powershell
# Windows PowerShell
docker --version
docker compose --version
git --version
```

---

## Configuración inicial

### 1. Clonar el repositorio

```powershell
git clone https://github.com/UTN-BDA-2026/Grupo---FSLHB.git
cd Grupo---FSLHB
```

### 2. Configurar variables de entorno

El proyecto incluye un archivo `.env` con valores por defecto. Para personalizar:

```powershell
# (Opcional) Copiar archivo de ejemplo
Copy-Item .env.example .env

# Editar .env con tus valores
notepad .env
```

**Variables críticas en `.env`:**

```env
FLASK_ENV=development
MONGO_URI=mongodb://admin:adminpass@localhost:27017/hockey?authSource=admin
SECRET_KEY=tu_clave_secreta_super_segura_aqui
```

---

## Inicialización del proyecto

### Opción 1: Inicialización Rápida (Recomendado)

```powershell
# 1. Levantar los contenedores
docker compose up --build

# 2. En otro terminal: Verificar setup
docker compose exec app python scripts/verify_setup.py

# 3. Inicializar indices y crear usuario admin
docker compose exec app python scripts/init_project.py --all

# 4. Acceder a la app
# http://localhost:5000
```

### Opción 2: Inicialización por Pasos

```powershell
# 1. Levantar Docker
docker compose up -d

# Esperar a que MongoDB esté listo (10-15 segundos)
docker compose logs mongodb | findstr "waited for connections"

# 2. Crear índices
docker compose exec app python scripts/setup_mongodb_indexes.py

# 3. Crear usuario admin interactivamente
docker compose exec app python scripts/crear_usuario_generico.py --username admin --password TuContraseña123

# 4. Acceder a http://localhost:5000
```

### Opción 3: Inicialización Manual (Desarrollo local)

```powershell
# 1. Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Asegurar que MongoDB está corriendo (Docker o local)
docker run -d -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=adminpass \
  mongo:7

# 4. Crear índices
python scripts/setup_mongodb_indexes.py

# 5. Crear usuario
python scripts/crear_usuario_generico.py --username admin --password TuContraseña123

# 6. Ejecutar app
python run.py
```

---

## Scripts disponibles

### 🔧 `scripts/verify_setup.py`
Verifica que todo está configurado correctamente antes de arrancar.

```powershell
# Verificación completa
docker compose exec app python scripts/verify_setup.py

# Exit codes:
# 0 = Todo OK
# 1 = Error crítico
# 2 = Advertencias (no crítico)
```

### 🗄️ `scripts/setup_mongodb_indexes.py`
Crea y gestiona índices de MongoDB para optimizar búsquedas.

```powershell
# Crear índices
docker compose exec app python scripts/setup_mongodb_indexes.py

# Resetear todos los índices
docker compose exec app python scripts/setup_mongodb_indexes.py --reset

# Verificar índices existentes
docker compose exec app python scripts/setup_mongodb_indexes.py --verify
```

**Índices creados:**
- `usuarios`: username (único)
- `clubes`: nombre (único)
- `equipos`: nombre (único), club_id
- `partidos`: fecha (descendente), torneo_id, equipo_local_id, equipo_visitante_id
- `incidencias`: partido_id, jugadora_id, tipo_incidencia
- `noticias`: fecha (descendente)
- `torneo`: nombre (único)
- `jugadora`: nombre, club_id

### 👤 `scripts/init_project.py`
Inicialización completa del proyecto (conexión, índices, usuario admin).

```powershell
# Modo interactivo (pregunta para cada paso)
docker compose exec app python scripts/init_project.py

# Crear todo automáticamente
docker compose exec app python scripts/init_project.py --all

# Sin crear índices
docker compose exec app python scripts/init_project.py --skip-indexes

# Solo crear usuario admin
docker compose exec app python scripts/init_project.py --create-admin
```

### 👤 `scripts/crear_usuario_generico.py`
Crea usuarios con permisos específicos.

```powershell
# Usuario admin
docker compose exec app python scripts/crear_usuario_generico.py \
  --username admin \
  --password TuContraseña123 \
  --operador \
  --puede-cargar-incidencias \
  --puede-precargar-equipos

# Usuario de club
docker compose exec app python scripts/crear_usuario_generico.py \
  --username SanJorge.sr \
  --password Contraseña456 \
  --club "San Jorge"
```

### 🔐 `scripts/modificar_contrasena.py`
Cambia la contraseña de un usuario.

```powershell
# Editar archivo antes de ejecutar
# Luego:
docker compose exec app python scripts/modificar_contrasena.py
```

---

## Solución de problemas

### Problema: "Cannot connect to MongoDB"

**Causa:** MongoDB no está levantado o no está accesible.

**Solución:**

```powershell
# Verificar que Docker Compose está ejecutando
docker compose ps

# Revisar logs de MongoDB
docker compose logs mongodb

# Reiniciar MongoDB
docker compose restart mongodb
```

### Problema: "Port 27017 already in use"

**Causa:** MongoDB ya está corriendo en ese puerto.

**Solución:**

```powershell
# Opción 1: Detener el proceso anterior
docker compose down

# Opción 2: Cambiar puerto en docker-compose.yml
# Cambiar: "27017:27017" a "27018:27017"
# Y actualizar MONGO_URI en .env
```

### Problema: "CSRF token missing"

**Causa:** CSRF está habilitado pero token no se genera.

**Solución:**

```powershell
# Verificar en .env
ENABLE_CSRF=false  # O asegurar que Flask-WTF está bien configurado
```

### Problema: "Usuario no autenticado"

**Causa:** Usuario no existe o contraseña es incorrecta.

**Solución:**

```powershell
# Crear nuevo usuario
docker compose exec app python scripts/crear_usuario_generico.py \
  --username admin \
  --password NuevaContraseña123 \
  --operador
```

### Problema: Índices no se crean

**Causa:** MongoDB no es accesible o permiso insuficiente.

**Solución:**

```powershell
# Verificar conexión
docker compose exec app python scripts/verify_setup.py

# Resetear y recrear
docker compose exec app python scripts/setup_mongodb_indexes.py --reset

# Crear nuevamente
docker compose exec app python scripts/setup_mongodb_indexes.py
```

---

## 🚀 Comandos útiles

```powershell
# INICIALIZACIÓN
docker compose up --build                    # Levantar todo
docker compose exec app python scripts/init_project.py --all  # Inicializar completo

# MONITOREO
docker compose logs -f app                   # Ver logs de la app
docker compose logs -f mongodb               # Ver logs de MongoDB
docker compose ps                            # Ver estado de servicios

# MANTENIMIENTO
docker compose down                          # Detener todos los servicios
docker compose down -v                       # Detener y limpiar volúmenes
docker compose restart                       # Reiniciar servicios
docker compose exec mongodb mongosh          # Conectar a MongoDB shell

# DEBUGGING
docker compose exec app python -i            # Python interactive en contenedor
docker compose exec app bash                 # Bash shell en contenedor
```

---

## 📚 Estructura de carpetas

```
Grupo---FSLHB/
├── app/                          # Código de la aplicación
│   ├── models/                   # Modelos de datos (MongoDB documents)
│   ├── repositories/             # Acceso a datos (PyMongo)
│   ├── services/                 # Lógica de negocio
│   ├── resources/                # Endpoints de la API
│   └── extensions.py             # Inicialización de extensiones
├── scripts/
│   ├── setup_mongodb_indexes.py  # Crear/verificar índices
│   ├── init_project.py           # Inicialización completa
│   ├── verify_setup.py           # Verificar configuración
│   ├── crear_usuario_generico.py # Crear usuarios
│   └── modificar_contrasena.py   # Cambiar contraseñas
├── docker-compose.yml            # Configuración Docker
├── Dockerfile                    # Imagen de la aplicación
├── requirements.txt              # Dependencias Python
├── .env                          # Variables de entorno (local)
├── .env.example                  # Plantilla de variables
└── README.md                     # Documentación general
```

---

## 📞 Soporte

Si tienes problemas:

1. Ejecuta `verify_setup.py` para diagnosticar
2. Revisa los logs: `docker compose logs app`
3. Revisa `.env` y asegurar MONGO_URI es correcta
4. Reinicia todo: `docker compose down && docker compose up --build`

---

**¡Proyecto listo para usar!** 🎉
