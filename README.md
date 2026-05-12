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
		docker compose up --build
		```
	- Esto descargará las imágenes necesarias, construirá la imagen de la app y levantará los servicios Traefik, MongoDB (base de datos) y la aplicación.

5. **Inicializar índices de MongoDB (opcional, recomendado):**
	```sh
	docker compose exec app python scripts/setup_mongodb_indexes.py
	```
	Esto crea índices en las colecciones para optimizar las búsquedas más frecuentes.

6. **Acceder a la web:**
	- Una vez levantado, accede a [http://localhost:5000](http://localhost:5000) en tu navegador para probar la aplicación localmente.

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
Desarrollado por Hernán Peñalbé, 2025.