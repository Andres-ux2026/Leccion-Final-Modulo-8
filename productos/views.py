from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Producto, Categoria
from .forms import ProductoForm


def is_admin(user):
    return user.is_staff or user.is_superuser


def _seed_productos():
    from decimal import Decimal

    cats = {
        "Electrónica": Categoria.objects.get_or_create(nombre="Electrónica")[0],
        "Audio": Categoria.objects.get_or_create(nombre="Audio")[0],
        "Deportes": Categoria.objects.get_or_create(nombre="Deportes")[0],
        "Computación": Categoria.objects.get_or_create(nombre="Computación")[0],
        "Ropa": Categoria.objects.get_or_create(nombre="Ropa")[0],
        "Hogar": Categoria.objects.get_or_create(nombre="Hogar")[0],
        "Herramientas": Categoria.objects.get_or_create(nombre="Herramientas")[0],
    }

    data = [
        {"nombre": "Auriculares Bluetooth Sony WH-1000XM5", "descripcion": "Auriculares inalámbricos con cancelación de ruido activa, 30 horas de batería y carga rápida.", "precio": 189990, "stock": 15, "imagen_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "categoria": cats["Audio"]},
        {"nombre": "Smartwatch Samsung Galaxy Watch 6", "descripcion": "Reloj inteligente con monitoreo de salud, GPS integrado, resistencia al agua y pantalla Super AMOLED.", "precio": 249990, "stock": 8, "imagen_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", "categoria": cats["Electrónica"]},
        {"nombre": "Cámara Mirrorless Sony Alpha A7 IV", "descripcion": "Cámara sin espejo de fotograma completo con 33MP, grabación 4K y estabilización de imagen integrada.", "precio": 1899990, "stock": 3, "imagen_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400", "categoria": cats["Electrónica"]},
        {"nombre": "Zapatillas Nike Air Max 270", "descripcion": "Zapatillas deportivas con unidad Air Max en el talón, parte superior de malla transpirable y suela de goma duradera.", "precio": 89990, "stock": 25, "imagen_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "categoria": cats["Deportes"]},
        {"nombre": "Mochila North Face Borealis", "descripcion": "Mochila ergonómica de 28L con compartimento para laptop, correas acolchadas y soporte lumbar.", "precio": 79990, "stock": 12, "imagen_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "categoria": cats["Deportes"]},
        {"nombre": "Silla Gamer Corsair T3 Rush", "descripcion": "Silla ergonómica con soporte lumbar ajustable, reposabrazos 4D y tapizado transpirable de tela.", "precio": 349990, "stock": 6, "imagen_url": "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400", "categoria": cats["Computación"]},
        {"nombre": "Teclado Mecánico Logitech G Pro X", "descripcion": "Teclado mecánico ultraportátil con switches intercambiables, retroiluminación RGB y cable desmontable.", "precio": 129990, "stock": 20, "imagen_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400", "categoria": cats["Computación"]},
        {"nombre": "Monitor LG UltraGear 27\" 1440p", "descripcion": "Monitor gaming IPS de 27 pulgadas, resolución QHD, tasa de refresco 165Hz y 1ms de respuesta.", "precio": 449990, "stock": 7, "imagen_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400", "categoria": cats["Computación"]},
        {"nombre": "Mouse Razer DeathAdder V3", "descripcion": "Mouse gaming ergonómico con sensor óptico de 30K DPI, peso ultraligero de 59g y switches ópticos.", "precio": 79990, "stock": 18, "imagen_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400", "categoria": cats["Computación"]},
        {"nombre": "Audífonos Marshall Major IV", "descripcion": "Audífonos over-ear con diseño clásico, 80 horas de reproducción, carga inalámbrica y plegables.", "precio": 59990, "stock": 10, "imagen_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400", "categoria": cats["Audio"]},
        {"nombre": "Tablet iPad Air M2 11\"", "descripcion": "Tablet con chip M2, pantalla Liquid Retina 11 pulgadas, 128GB y compatibilidad con Apple Pencil.", "precio": 699990, "stock": 5, "imagen_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400", "categoria": cats["Electrónica"]},
        {"nombre": "Polera Algodón Orgánico Unisex", "descripcion": "Polera de algodón orgánico certificado, corte regular, costuras reforzadas y tintes naturales.", "precio": 15990, "stock": 50, "imagen_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400", "categoria": cats["Ropa"]},
        {"nombre": "Chaqueta Impermeable Columbia", "descripcion": "Chaqueta cortavientos con tecnología Omni-Tech, capucha desmontable y múltiples bolsillos con cierre.", "precio": 129990, "stock": 9, "imagen_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400", "categoria": cats["Ropa"]},
        {"nombre": "Set de Sartenes Antiadherentes 3 Piezas", "descripcion": "Sartenes de aluminio forjado con recubrimiento cerámico triple capa, aptas para inducción y horno.", "precio": 45990, "stock": 14, "imagen_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400", "categoria": cats["Hogar"]},
        {"nombre": "Cafetera Italiana Bialetti 6 Tazas", "descripcion": "Cafetera de acero inoxidable, diseño clásico, apta para todo tipo de cocinas.", "precio": 24990, "stock": 30, "imagen_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400", "categoria": cats["Hogar"]},
        {"nombre": "Mochila de Hidratación Camelbak 2L", "descripcion": "Mochila ligera con reservorio de agua de 2 litros, diseño transpirable y compartimento para herramientas.", "precio": 54990, "stock": 11, "imagen_url": "https://images.unsplash.com/photo-1622260614153-03223fb72052?w=400", "categoria": cats["Deportes"]},
        {"nombre": "Parlante Portátil JBL Charge 5", "descripcion": "Parlante Bluetooth resistente al agua IP67, 20 horas de reproducción y batería con carga USB.", "precio": 89990, "stock": 22, "imagen_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "categoria": cats["Audio"]},
        {"nombre": "Lámpara LED Escritorio con Brazo Articulado", "descripcion": "Lámpara LED regulable con brazo articulado, luz neutra y cálida ajustable, base con carga inalámbrica.", "precio": 34990, "stock": 16, "imagen_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400", "categoria": cats["Hogar"]},
        {"nombre": "Set de Herramientas 32 Piezas Stanley", "descripcion": "Kit con martillo, destornilladores, llaves Allen, alicates y caja organizadora.", "precio": 39990, "stock": 13, "imagen_url": "https://images.unsplash.com/photo-1581783898377-1c85bf937427?w=400", "categoria": cats["Herramientas"]},
        {"nombre": "Mesa Plegable Camping 4 Personas", "descripcion": "Mesa portátil de aluminio con bolsas laterales, soporte para 20kg y funda de transporte incluida.", "precio": 49990, "stock": 0, "imagen_url": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400", "categoria": cats["Deportes"]},
    ]
    for item in data:
        item["precio"] = Decimal(str(item["precio"]))
        Producto.objects.create(**item)


def inicio(request):
    productos = Producto.objects.all()
    if not productos:
        _seed_productos()
        productos = Producto.objects.all()
    return render(request, "inicio.html", {"productos": productos})


@login_required
@user_passes_test(is_admin)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "lista_productos.html", {"productos": productos})


@login_required
@user_passes_test(is_admin)
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente")
            return redirect("inicio")
    else:
        form = ProductoForm()
    return render(request, "crear_producto.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente")
            return redirect("inicio")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "actualizar_producto.html", {"form": form, "producto": producto})


@login_required
@user_passes_test(is_admin)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente")
        return redirect("inicio")
    return render(request, "confirmar_eliminacion.html", {"producto": producto})
