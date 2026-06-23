# Usa una imagen oficial de Python ligera
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y fuerza que el output se muestre en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala las dependencias del sistema necesarias para compilar psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Define el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia e instala los requerimientos de Python
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de tu proyecto al contenedor
COPY . /code/