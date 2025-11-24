# Imagen base oficial de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copia el proyecto
COPY . /app

# Paquetes del sistema necesarios (WeasyPrint, fuentes y utilidades)
RUN apt-get update \
	 && apt-get install -y --no-install-recommends \
		 libcairo2 \
		 libpango-1.0-0 \
		 libpangoft2-1.0-0 \
		 libgdk-pixbuf-2.0-0 \
		 libffi-dev \
		 fonts-dejavu \
		 tzdata \
	 && rm -rf /var/lib/apt/lists/*

# Instala dependencias
RUN python -m pip install --upgrade pip \
	&& python -m pip install --no-cache-dir -r requirements.txt

# Expone el puerto Flask
EXPOSE 5000

# Comando para iniciar la app (ajusta si usás run.py)
CMD ["python", "run.py"]
