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
- **Base de datos:** PostgreSQL 15
- **ORM:** SQLAlchemy + Flask-SQLAlchemy
- **Migraciones:** Flask-Migrate
- **Serialización:** Marshmallow
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
	- Esto descargará las imágenes necesarias, construirá la imagen de la app y levantará los servicios Traefik, base de datos y aplicación.

5. **Acceder a la web:**
	- Una vez levantado, accede a [http://localhost:5000](http://localhost:5000) en tu navegador para probar la aplicación localmente.

## Estructura básica del proyecto

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