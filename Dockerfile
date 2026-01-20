# Usar una imagen ligera de Python
FROM python:3.10-slim

# Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y material
COPY src/ /app/src/
COPY examples/ /app/examples/
COPY student_material/ /app/student_material/
COPY setup.py .
COPY README.md .

# Instalar el paquete en modo editable
RUN pip install -e .

# Por defecto, entramos en una shell para que el alumno pueda ejecutar los labs
CMD ["/bin/bash"]
