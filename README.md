# Leccion-6-modulo-7

# 📚 Sistema de Gestión de libros - Django 6.0

Este proyecto es una aplicación web desarrollada en **Django 6.0** que implementa un sistema CRUD completo para la gestión de un catálogo de libros. Cuenta con una interfaz estilizada utilizando **Bootstrap 5**, alertas dinámicas que desaparecen automáticamente y contenedores Docker para un despliegue rápido y consistente.

---

## 🚀 Cómo Levantar el Proyecto

Puedes levantar el proyecto de dos maneras: utilizando **Docker** (recomendado para desarrollo consistente) o mediante un **Entorno Virtual local**.

### Opción 1: Levantamiento con Docker (Recomendado)

El proyecto incluye un `Dockerfile` basado en `python:3.12-slim` optimizado con las dependencias del sistema necesarias (`libpq-dev`, `gcc`).

1. **Construir la imagen de Docker:**
   ```bash
  docker compose up --build

2.  Crear e iniciar el entorno virtual:

  python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

3. instalar dependencias:
    pip install -r requirements.txt

4. Ejecutar migraciones de la Base de Datos:   
    python manage.py migrate

5. Iniciar el servidor de desarrollo:
    python manage.py runserver    


🗺️ Mapa de Rutas del Proyecto
Rutas del ecosistema de la aplicación configuradas en urls.py:

[GET]  /libros/            -> name='inicio'            -> Menú Principal de la Biblioteca
[GET]  /libros/lista/      -> name='lista_libros'      -> Catálogo General (Read)
[POST] /libros/crear/      -> name='crear_libro'       -> Agregar Nuevo Libro (Create)
[POST] /libros/editar/ID/  -> name='actualizar_libros' -> Modificar Datos por ID (Update)
[POST] /libros/eliminar/ID -> name='eliminar_libros'   -> Borrar Registro por ID (Delete)