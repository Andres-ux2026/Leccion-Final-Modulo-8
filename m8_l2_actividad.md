# Módulo 8 — Actividad N° 2: Buenas Prácticas para el Diseño de un Producto Tecnológico

**Estudiante:** Andrés  
**Curso:** Desarrollo de Aplicaciones Full Stack Python Trainee  
**Módulo:** Portafolio Profesional  
**Producto:** E-commerce Django — Lección Final Módulo 8

---

## 1. Errores detectados y corregidos

Durante la revisión del producto encontré varios problemas que fui corrigiendo uno por uno:

### 1.1 CSRF en crear producto
- **Error:** Al enviar el formulario para crear un producto, Django devolvía error 403 Forbidden.
- **Causa:** Las vistas `crear_producto`, `actualizar_producto` y `eliminar_producto` no tenían los decoradores `@login_required` y `@user_passes_test(is_admin)`, entonces cualquier persona (incluso sin autenticarse) podía intentar enviar el formulario y Django lo rechazaba por CSRF.
- **Solución:** Agregué ambos decoradores a las tres vistas.
- **Archivo:** `productos/views.py` líneas 62-63, 83-84, 98-99.

### 1.2 Usuarios staff bloqueados del carrito
- **Error:** Los administradores podían agregar productos al carrito normalmente, pero no debían porque ellos solo administran, no compran.
- **Causa:** No había ninguna validación en `agregar_al_carrito`.
- **Solución:** Agregué un `if request.user.is_staff` al inicio de la vista que muestra un mensaje de error y redirige.
- **Archivo:** `productos/views.py` línea 145.

### 1.3 Error 404 al acceder al carrito sin estar autenticado
- **Error:** Si un usuario no autenticado entraba a `/carrito/`, Django lanzaba error 404 porque la vista `ver_carrito` intentaba leer la sesión pero no estaba preparada para ese caso.
- **Causa:** La vista no verificaba si el usuario tenía sesión activa antes de consultar el carrito en la BD.
- **Solución:** Agregué el decorador `@login_required` a `ver_carrito`, `agregar_al_carrito`, `actualizar_carrito`, `eliminar_del_carrito`, `confirmar_compra` y `orden_confirmada` para redirigir automáticamente al login si no hay sesión.
- **Archivo:** `productos/views.py` líneas 133, 143, 171, 208, 219, 258.

### 1.4 Menú hamburguesa no funcionaba en móvil
- **Error:** En smartphone, al tocar el botón hamburguesa no se abría el panel con los enlaces del nav.
- **Causa:** El JavaScript (`main.js`) agregaba la clase `navPanel-visible` al elemento `<html>` (`document.documentElement`), pero los estilos CSS la esperaban en `<body>`.
- **Solución:** Cambié `doc.classList.toggle()` por `document.body.classList.toggle()`. También eliminé la transformación `translateX(-4em)` del `#page-wrapper` que movía toda la página al abrir el menú.
- **Archivo:** `productos/static/productos/js/main.js` línea 59.

### 1.5 Badges de categoría desalineados en las cards
- **Error:** En la cuadrícula de productos, el badge rojo de la categoría aparecía a diferente altura según el título: si el título era corto (1 línea), el badge quedaba más arriba; si era largo (2 líneas), quedaba más abajo.
- **Causa:** El contenedor `.card-header-area` tenía `height: 6em` fijo, pero el `<h3>` tenía `margin-bottom: 0.35em` y no ocupaba todo el espacio vertical disponible, así que la posición del badge dependía del alto real del título.
- **Solución:** Cambié el `<h3>` a `flex-grow: 1` y `margin: 0`. Esto hace que el título ocupe todo el espacio disponible y empuje el badge siempre al fondo del área de 6em, sin importar el largo del texto.
- **Archivo:** `productos/static/productos/css/main.css`.

### 1.6 Redirección de `/` rota
- **Error:** La raíz del sitio no mostraba nada, daba error 404.
- **Causa:** No había una vista configurada para la URL `/`.
- **Solución:** Usé `RedirectView.as_view(pattern_name='inicio')` en `conf/urls.py` para redirigir automáticamente al catálogo.
- **Archivo:** `conf/urls.py`.

### 1.7 Migraciones faltantes y usuarios de prueba
- **Error:** En Render (free tier) no hay consola para ejecutar `createsuperuser`, así que no se podía iniciar sesión.
- **Solución:** Creé una data migration (`0007_crear_usuarios_prueba.py`) que crea automáticamente un admin y un cliente al ejecutar `migrate`.
- **Archivo:** `productos/migrations/0007_crear_usuarios_prueba.py`.

---

## 2. Mejoras implementadas

### 2.1 Diseño responsivo (mobile first)
- Agregué menú hamburguesa que se muestra solo en pantallas ≤ 736px.
- El nav superior se oculta en móvil y aparece el botón hamburguesa.
- La cuadrícula de productos cambia de 3 columnas a 2 y luego a 1 según el ancho de pantalla (breakpoints en 1280px, 1080px, 736px, 480px).
- Las tablas de carrito y órdenes tienen scroll horizontal en móvil.
- **Archivo:** `productos/static/productos/css/main.css`.

### 2.2 Hero mejorado
- Cambié el texto del hero principal a un estilo más llamativo: negrita, con `text-shadow` y `max-width` para que se vea profesional.
- **Archivo:** `productos/templates/inicio.html`.

### 2.3 Badge de categoría rojo
- Cambié el color del badge de categoría a rojo (`#f35858`) con texto blanco para que resalte mejor sobre la card.
- **Archivo:** `productos/static/productos/css/main.css`.

### 2.4 Placeholder en imágenes
- Cuando un producto no tiene imagen, se muestra un placeholder visual (círculo gris con ícono) en vez de un espacio vacío o un enlace roto.
- **Archivo:** `productos/templates/inicio.html`.

### 2.5 Mensajes flash con desvanecimiento
- Los mensajes de éxito/error ahora se eliminan del DOM con `parentElement.remove()` después de 3 segundos, en vez de solo ocultarlos con `display: none`. Esto mejora la experiencia de usuario.
- **Archivo:** `productos/templates/base.html`.

### 2.6 Footer limpio
- Eliminé el texto "Design: HTML5 UP" del footer y dejé solo el mensaje de copyright del proyecto.
- **Archivo:** `productos/templates/base.html`.

### 2.7 Nav mejorado
- Eliminé el botón "Mi Tienda" duplicado del header.
- El nav ahora muestra el nombre del usuario autenticado, enlace al carrito y botón de cerrar sesión (solo en desktop). En móvil todo aparece dentro del panel hamburguesa.
- **Archivo:** `productos/templates/base.html`.

### 2.8 Despliegue en Render
- Configuré todo el proyecto para desplegarse en Render free tier:
  - `build.sh`: script de build que instala dependencias, ejecuta collectstatic y migrate.
  - `runtime.txt`: fija Python 3.12.8.
  - `render.yaml`: define la base de datos PostgreSQL y el web service.
  - `requirements.txt`: incluye gunicorn, whitenoise, dj-database-url.
  - `conf/settings.py`: configurado para leer `DATABASE_URL`, whitenoise middleware, `ALLOWED_HOSTS` dinámico, `CSRF_TRUSTED_ORIGINS` incluye `.onrender.com`.

### 2.9 Tests automatizados
- Escribí 48 tests que cubren:
  - Modelos (creación de productos, categorías, órdenes).
  - Vistas (carga de páginas, CRUD de productos).
  - Carrito (agregar, actualizar, eliminar items, validar stock).
  - Autenticación (login requerido, bloqueo a staff, redirección si no autenticado).
  - Órdenes (creación, confirmación, descuento de stock).
- **Archivo:** `productos/tests.py` (401 líneas).

---

## 3. Feedback recibido y aplicado

### 3.1 Feedback del docente: alinear badges de categoría
- **Feedback:** "Las cards del catálogo deben mostrar la categoría alineada a la misma altura exacta."
- **Aplicación:** Cambié el CSS del contenedor `.card-header-area` para que use `flex-grow` en el título y el badge quede siempre al fondo del área fija de 6em. Esto funciona sin importar si el título del producto es corto o largo.
- **Resultado:** Todas las cards ahora tienen el badge rojo en la misma posición vertical, lo que se ve ordenado y profesional.

### 3.2 Feedback del docente: carrito y login visibles en móvil
- **Feedback:** "En smartphone no se ve el carrito ni el botón para iniciar sesión."
- **Aplicación:** Diagnosticamos que el menú hamburguesa no se abría porque JavaScript agregaba la clase al elemento incorrecto (`<html>` en vez de `<body>`). Corregí el selector y aseguré que el panel incluya todos los enlaces: Carrito, Cerrar Sesión, y el nombre del usuario.
- **Resultado:** Ahora en cualquier smartphone se puede abrir el menú, ver el carrito, cerrar sesión y navegar por el sitio.

### 3.3 Feedback entre compañeros: hero poco atractivo
- **Feedback:** "El hero se ve muy simple, sin personalidad."
- **Aplicación:** Modernicé el hero con texto en negrita, sombra (`text-shadow`) y un ancho máximo para que se vea más profesional y llamativo.
- **Resultado:** El hero ahora capta la atención y da una mejor primera impresión del sitio.

### 3.4 Feedback entre compañeros: footer con créditos genéricos
- **Feedback:** "El footer dice 'Design: HTML5 UP', eso no va con un portafolio profesional."
- **Aplicación:** Eliminé ese texto y dejé solo un mensaje de copyright personalizado.
- **Resultado:** El footer ahora luce limpio y profesional.

### 3.5 Feedback del docente: redirección raíz
- **Feedback:** "Al entrar al dominio raíz debería mostrar la tienda, no un error."
- **Aplicación:** Agregué `RedirectView` en las URLs principales para redirigir `/` a `/products/`.
- **Resultado:** Ahora al entrar al sitio se ve inmediatamente el catálogo de productos.

---

## Conclusión

Este proyecto me permitió aplicar todo lo aprendido en los 9 módulos del curso:

| Módulo | Contenido aplicado en el proyecto |
|--------|----------------------------------|
| M1 — Orientación al perfil | Estructura de trabajo, disciplina, autoaprendizaje |
| M2 — Front-end | HTML, CSS, diseño responsivo, Bootstrap, menú hamburguesa |
| M3 — Python básico | Sintaxis, funciones, tipos de datos |
| M4 — Python avanzado | Decoradores, POO, módulos, manejo de excepciones |
| M5 — Bases de datos | Modelo relacional, migraciones, SQLite/PostgreSQL |
| M6 — Django | Vistas, templates, URLs, herencia de plantillas, formularios |
| M7 — Acceso a datos | ORM, modelos relacionales (ForeignKey), CRUD, consultas |
| M8 — Portafolio | Depuración, mejora continua, feedback, versión final |
| M9 — Empleabilidad | README profesional, deploy en Render, repositorio público |

El producto final es una aplicación e-commerce funcional, desplegada en Render, con catálogo, carrito de compras, órdenes, autenticación por roles y diseño responsivo.

**Enlace a la aplicación:** https://leccion-final-modulo-8.onrender.com  
**Repositorio:** https://github.com/Andres-ux2026/Leccion-Final-Modulo-8
