# Lección Final Módulo 8 - E-commerce con Django

Sistema de e-commerce completo desarrollado en **Django 6.0** con PostgreSQL y autenticación por roles. Incluye catálogo de productos, carrito de compras, flujo de pedidos y panel de administración.

**[Repositorio público](https://github.com/anomalyco/Leccion-Final-Modulo-8)**

---

## Requisitos e Instalación

### Requisitos previos
- Python 3.12+
- Docker y Docker Compose (para PostgreSQL)

### 1. Clonar el repositorio
```bash
git clone https://github.com/anomalyco/Leccion-Final-Modulo-8.git
cd Leccion-Final-Modulo-8
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Levantar base de datos (PostgreSQL con Docker)
```bash
docker compose up -d db
```

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Iniciar servidor
```bash
python manage.py runserver
```

> Los productos de demostración se crean automáticamente al cargar la página principal si la base de datos está vacía.

---

## Rutas Principales

### Públicas (sin autenticación)

| Ruta | Descripción |
|---|---|
| `GET /products/` | Catálogo de productos |
| `GET /accounts/login/` | Inicio de sesión |

### Cliente (autenticado)

| Ruta | Descripción |
|---|---|
| `GET /products/cart/` | Carrito de compras |
| `GET /products/cart/add/<id>/` | Agregar producto al carrito |
| `POST /products/cart/update/<id>/` | Actualizar cantidad |
| `GET /products/cart/remove/<id>/` | Eliminar producto del carrito |
| `GET/POST /products/cart/checkout/` | Confirmar compra |
| `GET /products/order/<id>/` | Detalle de orden |

### Administrador

| Ruta | Descripción |
|---|---|
| `GET /products/list/` | Tabla administrativa de productos |
| `GET/POST /products/create/` | Crear producto |
| `GET/POST /products/edit/<id>/` | Editar producto |
| `GET/POST /products/delete/<id>/` | Eliminar producto |
| `GET /admin/` | Panel Django admin |

---

## Credenciales de Prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| **Administrador** | `admin` | `holamundo` |
| **Cliente** | `cliente` | `holamundo123` |

- **Admin**: Accede a `/products/list/` para gestión CRUD y a `/admin/` para el panel Django.
- **Cliente**: Navega el catálogo, agrega productos al carrito y realiza compras.

---

## Despliegue en Render (Free Tier)

### Requisitos
- Repositorio en GitHub (ya vinculado)
- Cuenta gratuita en [render.com](https://render.com)

### Pasos

1. **Conecta tu repositorio**: En Render, crea un **Web Service** vinculado a tu fork/clone de este repo.

2. **Crea una base de datos PostgreSQL**: Ve a **Dashboard > Databases > New PostgreSQL**, elige el plan **Free**.

3. **Configura el Web Service**:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn conf.wsgi:application --workers 2 --worker-class sync --timeout 120`
   - **Plan**: Free

4. **Variables de entorno** (Render las auto-asigna desde `render.yaml` o créalas manualmente):
   - `DATABASE_URL`: conectar desde la base de datos creada
   - `DJANGO_SECRET_KEY`: generar un valor seguro
   - `DJANGO_DEBUG`: `False`
   - `DJANGO_ALLOWED_HOSTS`: `.onrender.com,localhost`
   - `PYTHON_VERSION`: `3.12.8`

5. **Desplegar**: Render ejecutará `build.sh` (instala dependencias, collectstatic, migraciones).

6. **Crear usuarios de prueba** (después del despliegue):
   ```bash
   # Conectarse a Render Shell o usar django manage.py shell
   python manage.py createsuperuser --username=admin --email=admin@example.com
   python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('cliente', 'cliente@example.com', 'holamundo123')"
   ```

> **Nota**: El plan free de Render "duerme" el servicio tras 15 min de inactividad. La primera solicitud puede demorar hasta 90 segundos mientras "despierta". La base de datos PostgreSQL free tiene 1 GB de almacenamiento.

---

## Funcionalidades Implementadas (MVP Final)

### Autenticación y acceso
- **Cliente**: Inicia sesión, navega el catálogo y opera el carrito de compras.
- **Administrador**: Inicia sesión, accede al panel de administración de Django y al CRUD de productos.

### Catálogo y persistencia
- Catálogo de productos mostrado desde la base de datos (ORM de Django).
- Productos persistidos y editables (creación/edición/eliminación) solo por administradores.
- Seed automático: si la base de datos está vacía, se crean 20 productos de demostración.

### Carrito y compra (flujo completo)
- **Carrito funcional** para clientes autenticados:
  - Agregar productos
  - Quitar productos
  - Actualizar cantidades
  - Mostrar subtotales y total correcto
- **Confirmación de compra**:
  - Registro de orden (pedido) con sus ítems
  - Asociación de la orden al usuario autenticado
  - Reducción de stock al confirmar la compra

### Vistas y navegación
- Frontend consistente con Bootstrap 5.
- Navegación clara entre: catálogo, carrito, login/logout y administración de productos.
- Navbar responsive con contador de items en el carrito.

### Validaciones y mensajes
- Validaciones en formularios (precio > 0, campos requeridos).
- Validaciones en carrito (stock suficiente, cantidades > 0).
- Mensajes claros de éxito/error con auto-dismiss (3 segundos).

---

## Motor de Base de Datos

**PostgreSQL 15** corriendo en un contenedor Docker. Configuración en `docker-compose.yml`:

| Parámetro | Valor |
|---|---|
| Motor | `django.db.backends.postgresql` |
| Base de datos | `mi_django_db` |
| Usuario | `mi_usuario` |
| Contraseña | `mi_contraseña_secreta` |
| Puerto | `5432` |

---

## Descripción del Modelo de Datos

### `Producto` — `productos/models.py`

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id` | `BigAutoField` | PK, auto | Identificador único |
| `categoria` | `ForeignKey(Categoria)` | null=True, on_delete=SET_NULL | Relación muchos-a-uno con Categoria |
| `nombre` | `CharField` | max_length=100, obligatorio | Nombre del producto |
| `descripcion` | `TextField` | blank=True | Descripción del producto |
| `precio` | `DecimalField` | max_digits=10, decimal_places=2, > 0 | Precio en pesos chilenos |
| `stock` | `IntegerField` | default=0 | Unidades disponibles |
| `imagen` | `ImageField` | upload_to="productos/", blank=True, null=True | Imagen subida desde el PC |
| `imagen_url` | `URLField` | blank=True | Imagen desde URL externa (demo) |

### `Categoria` — `productos/models.py`

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id` | `BigAutoField` | PK, auto | Identificador único |
| `nombre` | `CharField` | max_length=50, obligatorio | Nombre de la categoría |

### `Orden` — `productos/models.py` (nuevo en Módulo 8)

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id` | `BigAutoField` | PK, auto | Identificador único |
| `usuario` | `ForeignKey(User)` | on_delete=CASCADE | Usuario que realizó la compra |
| `fecha` | `DateTimeField` | auto_now_add=True | Fecha y hora de la compra |
| `total` | `DecimalField` | max_digits=12, decimal_places=2 | Total de la orden |

### `ItemOrden` — `productos/models.py` (nuevo en Módulo 8)

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id` | `BigAutoField` | PK, auto | Identificador único |
| `orden` | `ForeignKey(Orden)` | on_delete=CASCADE, related_name="items" | Orden asociada |
| `producto` | `ForeignKey(Producto)` | on_delete=SET_NULL, null=True | Producto comprado |
| `cantidad` | `IntegerField` | — | Cantidad comprada |
| `precio_unitario` | `DecimalField` | max_digits=10, decimal_places=2 | Precio al momento de la compra |

**Relaciones:**
- `Categoria` → `Producto` (1:N)
- `User` → `Orden` (1:N)
- `Orden` → `ItemOrden` (1:N)
- `Producto` → `ItemOrden` (1:N)

**Validaciones:**
- `precio` debe ser mayor a 0 (validación en `ProductoForm.clean_precio`)
- `nombre` es obligatorio
- Stock suficiente al agregar al carrito y al confirmar compra
- Cantidad > 0 en el carrito

---

## Ejecutar Tests
```bash
python manage.py test productos -v 2
```

El proyecto incluye **48 tests** que cubren:
- Modelos (Categoria, Producto, Orden, ItemOrden)
- Vistas públicas (catálogo, login)
- Autenticación y roles (admin, cliente, anónimo)
- CRUD de productos (crear, editar, eliminar)
- Carrito de compras (agregar, actualizar, eliminar, stock)
- Flujo de orden (confirmar compra, detalle, permisos)
- Formularios (validación de precio)
- Templates y contexto (navbar, botones, contador)
- Context processor (carrito_count)

---

## Estructura del Proyecto

```
├── conf/                   # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── productos/              # Aplicación principal
│   ├── models.py           # Modelos: Producto, Categoria, Orden, ItemOrden
│   ├── views.py            # Vistas: CRUD, carrito, ordenes
│   ├── forms.py            # Formulario con validaciones
│   ├── urls.py             # Rutas de la aplicación
│   ├── admin.py            # Registro en admin Django
│   ├── context_processors.py # Context processor para carrito_count
│   ├── templatetags/
│   │   └── producto_extras.py  # Filtro clp (formato precios)
│   └── templates/
│       ├── base.html
│       ├── inicio.html
│       ├── lista_productos.html
│       ├── crear_producto.html
│       ├── actualizar_producto.html
│       ├── confirmar_eliminacion.html
│       ├── carrito.html          # (nuevo) Carrito de compras
│       ├── orden_confirmada.html # (nuevo) Confirmación de orden
│       └── registration/
│           └── login.html
├── media/                  # Archivos subidos (imágenes)
├── capturas/               # Capturas de pantalla
├── estilo/                 # Archivos de diseño (PDF, HTML, CSS)
├── docker-compose.yml      # PostgreSQL + pgAdmin
├── Dockerfile
├── manage.py
└── requirements.txt
```
