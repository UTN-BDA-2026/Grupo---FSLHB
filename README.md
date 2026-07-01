# Grupo---FSLHB
Integrantes 
Caceres Franco
Cardozo Leandro
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
- **Base de datos:** MongoDB 7
- **Driver ODM:** PyMongo + Flask-PyMongo
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
		docker compose --project-directory . -f docker/docker-compose.yml up -d --build
		```
	- Esto descargará las imágenes necesarias, construirá la imagen de la app y levantará los servicios Traefik, MongoDB (base de datos) y la aplicación.

5. **Inicializar índices de MongoDB (opcional, recomendado):**
	```sh
	docker compose --project-directory . -f docker/docker-compose.yml exec app python scripts/setup_mongodb_indexes.py
	```
	Esto crea índices en las colecciones para optimizar las búsquedas más frecuentes.


6. **(Opcional pero recomendado) Ejecutar migración de datos inicial:**
	- Si querés poblar la base de datos con datos existentes (por ejemplo, desde un backup de Postgres), ejecutá el siguiente comando para migrar los datos a MongoDB:
	- **Importante:** el contenedor `db` (Postgres) arranca vacío; antes de migrar tenés que **restaurar el dump** dentro de Postgres (si no, la migración va a reportar `Tablas public: 0` y migrar todo en 0).
		```sh
		python scripts/restore_db.py .\backup_local.dump
		```
	- Luego sí, ejecutá la migración a MongoDB:
	```sh
	docker compose --project-directory . -f docker/docker-compose.yml exec app python scripts/migrate_postgres_to_mongodb.py
	```
	- Esto migrará los datos desde el backup de Postgres (verifica que el script y los archivos necesarios estén presentes en la carpeta `scripts/`).
	- Si no ejecutás este paso, la base de datos quedará vacía y deberás cargar los datos manualmente.

7. **Acceder a la web (HTTPS con Traefik):**
	- Una vez levantado (y migrados los datos), accedé a:
		- **HTTPS:** https://localhost:8444
		- (No se publica HTTP: el acceso es solo por HTTPS)
	- Traefik está configurado **por archivo** (no usa `labels` ni `docker.sock`):
		- Config dinámica: `app/traefik/config/config.yml`
		- Config estática: `app/traefik/config/traefik.yml`
	- Si al entrar por HTTPS te aparece el aviso "Su conexión no es privada", necesitás generar e instalar un certificado local confiable (mkcert):
		1. Instalar mkcert (Windows, con winget):
			```sh
			winget install -e --id FiloSottile.mkcert
			```
			> Si `mkcert` no se reconoce, cerrá y abrí la terminal.
		2. Instalar la CA local:
			```sh
			mkcert -install
			```
			> Si este paso falla por permisos, abrí PowerShell como **Administrador** y repetilo. Si ya estaba instalada, puede no hacer cambios.
		3. Generar el certificado para este proyecto (se guarda en `app/traefik/certs/`):
			```sh
			mkcert -cert-file app/traefik/certs/cert.pem -key-file app/traefik/certs/key.pem localhost 127.0.0.1 ::1 universidad.localhost "*.universidad.localhost" traefik.universidad.localhost
			```
		4. Reiniciar Traefik para que tome el nuevo certificado:
			```sh
			docker compose --project-directory . -f docker/docker-compose.yml up -d --force-recreate traefik
			```
	- Nota: la app no expone `http://localhost:5000` al host; se accede solo vía Traefik.

## Respaldos (Backups) de las Bases de Datos

Para facilitar la generación de copias de seguridad tanto de MariaDB como de MongoDB, el proyecto cuenta con un script automatizado para entornos de Windows.

8. **Generar un nuevo backup manual:**
    - Verificá que los contenedores estén encendidos y que el motor de base de datos esté funcionando.
    - Ejecutá el script de PowerShell desde la raíz del proyecto:
    ```ps1
    .\generar_backups.ps1
    ```
    - Si querés validar la restauración del backup al mismo tiempo, usá:
    ```ps1
    .\generar_backups.ps1 -ValidateRestore
    ```
    - Los archivos quedarán guardados en la carpeta `backups/`.

9. **Restaurar un backup (en caso de error o migración de PC):**
    - Reemplazá `[ARCHIVO]` por el nombre exacto del backup que querés restaurar, por ejemplo `mariadb_20260514_193000.sql` o `mongodb_20260514_193000.archive`.
    - Asegurate de que los contenedores estén levantados.

    - **Para restaurar MariaDB:**
    ```sh
    docker compose --project-directory . -f docker/docker-compose.yml cp .\backups\[ARCHIVO].sql mariadb:/tmp/restore.sql
    docker compose --project-directory . -f docker/docker-compose.yml exec mariadb sh -c "mariadb -u hockeyuser -phockeypass hockey < /tmp/restore.sql"
    ```

    - **Para restaurar MongoDB:**
    ```sh
    docker compose --project-directory . -f docker/docker-compose.yml cp .\backups\[ARCHIVO].archive mongodb:/tmp/restore.archive
    docker compose --project-directory . -f docker/docker-compose.yml exec mongodb sh -c "mongorestore --username admin --password adminpass --authenticationDatabase admin --archive=/tmp/restore.archive --drop"
    ```

    - **Importante:** para restaurar el sistema completo, necesitás usar el backup de MariaDB y el backup de MongoDB correspondientes al mismo momento.



## Importante: ¿Qué pasa al levantar el proyecto?

Al clonar este repositorio y ejecutar `docker compose up --build`, la aplicación **ya queda configurada para usar MongoDB** como base de datos principal (contenedor `mongodb`).

- MongoDB arranca vacío la primera vez.
- Las colecciones se crean **automáticamente** cuando la aplicación realiza la primera inserción de documentos.
- No requiere migraciones previas ni scripts de inicialización de esquema.
- Los datos se almacenan en volúmenes de Docker (`mongodata`) para persistencia.

**En resumen:**
- Al levantar los contenedores, la app apunta a MongoDB.
- Las colecciones se crean automáticamente sin intervención manual.
- Opcionalmente, ejecuta `setup_mongodb_indexes.py` para crear índices de optimización.

---

## Estructura del Proyecto

- `app/` Código fuente principal (modelos, rutas, servicios, recursos, repositorios, etc.)
- `scripts/` Scripts de utilidad para administración (crear usuarios, modificar contraseñas, inicializar índices MongoDB)
- `app/traefik/` Configuración de Traefik (proxy inverso y certificados)
- `Dockerfile` y `docker-compose.yml` para despliegue y desarrollo con MongoDB

---

## Licencia

Este proyecto es software propietario. Todos los derechos reservados. Queda prohibida la copia, distribución o modificación sin el permiso expreso del autor. Consulta el archivo LICENSE para más información.

---
Desarrollado por Bruno Carrieri y otros, 2025.