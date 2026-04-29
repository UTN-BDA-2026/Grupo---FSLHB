# Grupo---FSLHB
Integrantes 
Caceres Franco
Cardoso Leandro
Carrieri Bruno
Garcia Santiago
Peñalbe Hernan 
=======
# Proyecto Hockey

Este proyecto es una página web dedicada al hockey, donde los usuarios pueden acceder a:

- Noticias actualizadas sobre el mundo del hockey
- Posiciones y tablas de clasificación
- Calendario de partidos y eventos
- Información completa de equipos y jugadoras
- Sistema de gestión de partidos simple y robusto para todas las categorías

El objetivo es centralizar toda la información relevante y facilitar la gestión de partidos y torneos para clubes, jugadoras y aficionados.

## Tecnologías y herramientas utilizadas

- **Lenguaje principal:** Python 3.11
- **Framework web:** Flask
- **Servidor de aplicaciones:** Gunicorn
- **Base de datos:** MariaDB 10.11
- **ORM:** SQLAlchemy + Flask-SQLAlchemy
- **Migraciones:** Flask-Migrate
- **Autenticación:** Flask-Login, Flask-WTF (CSRF)
- **CORS:** Flask-Cors
- **CDN de imágenes:** Cloudinary
- **Exportación de archivos:** openpyxl (Excel), reportlab y PyPDF2 (PDF)
- **Contenedores:** Docker y Docker Compose
- **Proxy inverso y HTTPS:** Traefik

---

## Cómo probar el proyecto en otra computadora

1. **Requisitos previos:**
	- Tener instalado [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/).
	- (Opcional) Tener git para clonar el repositorio.

2. **Clonar el repositorio:**
	```sh
	git clone https://github.com/UTN-BDA-2026/Grupo---FSLHB.git
	cd Hockey
	```

3. **Configurar variables de entorno y entorno Python (opcional para desarrollo sin Docker):**
	- Crear un entorno virtual de Python y activarlo:
		```sh
		python -m venv venv
		.\venv\Scripts\Activate.ps1  # En Windows
		# source venv/bin/activate    # En Linux/Mac
		```
	- Instalar dependencias:
		```sh
		pip install -r requirements.txt
		```

4. **Construir la imagen y levantar los contenedores:**
	- Desde la raíz del proyecto, ejecutar:
		```sh
		docker compose up --build
		```
	- Esto descargará las imágenes necesarias, construirá la imagen de la app y levantará los servicios Traefik, MariaDB (base de datos) y la aplicación.
	- Nota: el `docker-compose.yml` incluye Postgres como base de origen para migración/compatibilidad (la app corre contra MariaDB).

5. **Acceder a la web:**
	- Una vez levantado, accede a [http://localhost:5000](http://localhost:5000) en tu navegador para probar la aplicación localmente.

## Importante: ¿Qué pasa al levantar el proyecto?

Al clonar este repositorio y ejecutar `docker compose up --build`, la aplicación **ya queda configurada para usar MariaDB** como base de datos principal (contenedor `mariadb`).

- El contenedor `db` (Postgres) también se levanta, pero **solo como fuente de datos para migrar** (la app no lo usa directamente).
- **MariaDB arranca vacío la primera vez**. Para que la app funcione con datos reales, es necesario correr los scripts de migración (crear el esquema y migrar los datos desde Postgres a MariaDB).
- Si no se corre la migración, la app en MariaDB estará vacía (sin tablas ni datos).

**En resumen:**
- Al levantar los contenedores, la app apunta a MariaDB, pero hay que migrar los datos desde Postgres manualmente con los comandos del README.
- Postgres queda solo como “fuente” para migrar, no como base activa de la app.

---

## Cómo migrar de Postgres a MariaDB (paso a paso)

Este proyecto incluye scripts y configuración para migrar todos los datos desde una base Postgres (contenedor `db`) a MariaDB (contenedor `mariadb`) usando Docker Compose. Así cualquier integrante puede repetir la migración o restaurar el entorno.

**Pasos:**

1. **Levantar los servicios necesarios:**
	```sh
	docker compose up -d --build
	```
	Esto inicia los contenedores de la app, MariaDB (`mariadb`), Postgres (`db`) y Traefik.

2. **Crear el esquema en MariaDB:**
	```sh
	docker compose exec app bash -c 'export PROD_DATABASE_URI="mysql+pymysql://hockeyuser:hockeypass@mariadb:3306/hockey" ; python scripts/create_schema_mariadb.py'
	```
	Esto crea todas las tablas en MariaDB según los modelos ORM.

3. **Migrar los datos desde Postgres a MariaDB:**
	```sh
	docker compose exec app bash -c 'export SOURCE_DATABASE_URL="postgresql+psycopg2://hockeyuser:hockeypass@db:5432/hockey" ; export TARGET_DATABASE_URL="mysql+pymysql://hockeyuser:hockeypass@mariadb:3306/hockey" ; python scripts/migrate_postgres_to_mariadb.py --wipe-target'
	```
	Esto copia todos los datos de Postgres a MariaDB (borrando antes el destino).

4. **Verificar que la migración fue exitosa:**
	```sh
	docker compose exec app bash -c 'export SOURCE_DATABASE_URL="postgresql+psycopg2://hockeyuser:hockeypass@db:5432/hockey" ; export TARGET_DATABASE_URL="mysql+pymysql://hockeyuser:hockeypass@mariadb:3306/hockey" ; python scripts/verify_migration_counts.py'
	```
	Si todo está bien, mostrará: `OK: All common tables match row counts.`

5. **Listo!**
	La app ya estará usando MariaDB con todos los datos migrados. Podés acceder a [http://localhost:5000](http://localhost:5000) y probar los endpoints normalmente.

**Notas:**
- Si ya existe información en MariaDB, el paso 3 (`--wipe-target`) la borrará y reemplazará por la de Postgres.
- Si hay cambios en los modelos, repetir los pasos 2 y 3 para actualizar el esquema y los datos.
- Si hay otro Traefik ocupando los puertos 80/443, detenerlo o cambiar los puertos en `docker-compose.yml`.

- `app/` Código fuente principal (modelos, rutas, servicios, recursos, etc.)
- `migrations/` Migraciones de base de datos (alembic)
- `scripts/` Scripts de utilidad para administración
- `app/traefik/` Configuración de Traefik (proxy inverso y certificados)
- `Dockerfile` y `docker-compose.yml` para despliegue y desarrollo

---

## Licencia

Este proyecto es software propietario. Todos los derechos reservados. Queda prohibida la copia, distribución o modificación sin el permiso expreso del autor. Consulta el archivo LICENSE para más información.

---
Desarrollado por Hernán Peñalbé, 2025.