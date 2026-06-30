from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Categoria, Producto, Orden, ItemOrden


class ModelTests(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre="Test")
        self.prod = Producto.objects.create(
            categoria=self.cat,
            nombre="Producto Test",
            descripcion="Descripción test",
            precio=Decimal("19990"),
            stock=10,
            imagen_url="https://example.com/img.jpg",
        )
        self.user = User.objects.create_user("testuser", "test@test.com", "pass123")
        self.orden = Orden.objects.create(usuario=self.user, total=Decimal("39980"))
        self.item = ItemOrden.objects.create(
            orden=self.orden,
            producto=self.prod,
            cantidad=2,
            precio_unitario=self.prod.precio,
        )

    def test_categoria_str(self):
        self.assertEqual(str(self.cat), "Test")

    def test_categoria_verbose_name(self):
        self.assertEqual(Categoria._meta.verbose_name, "categoría")

    def test_producto_str(self):
        self.assertEqual(str(self.prod), "Producto Test")

    def test_orden_str(self):
        expected = f"Orden #{self.orden.id} - testuser"
        self.assertEqual(str(self.orden), expected)

    def test_orden_verbose_name(self):
        self.assertEqual(Orden._meta.verbose_name, "orden")

    def test_item_orden_str(self):
        self.assertEqual(str(self.item), "2x Producto Test")

    def test_item_orden_subtotal(self):
        self.assertEqual(self.item.subtotal, Decimal("39980"))

    def test_producto_stock_default(self):
        prod2 = Producto.objects.create(
            nombre="Sin stock", precio=Decimal("1000")
        )
        self.assertEqual(prod2.stock, 0)


class ViewPublicTests(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre="Test")
        self.prod = Producto.objects.create(
            categoria=self.cat,
            nombre="Producto Test",
            precio=Decimal("19990"),
            stock=10,
            imagen_url="https://example.com/img.jpg",
        )

    def test_inicio_status_200(self):
        response = self.client.get(reverse("inicio"))
        self.assertEqual(response.status_code, 200)

    def test_inicio_usa_template_correcto(self):
        response = self.client.get(reverse("inicio"))
        self.assertTemplateUsed(response, "inicio.html")

    def test_inicio_muestra_productos(self):
        response = self.client.get(reverse("inicio"))
        self.assertContains(response, "Producto Test")

    def test_inicio_seed_auto_si_vacio(self):
        Producto.objects.all().delete()
        response = self.client.get(reverse("inicio"))
        self.assertGreater(Producto.objects.count(), 0)

    def test_login_page_status_200(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)


class ViewAuthTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin", "admin@test.com", "admin123"
        )
        self.cliente = User.objects.create_user(
            "cliente", "cliente@test.com", "cliente123"
        )
        self.cat = Categoria.objects.create(nombre="Test")
        self.prod = Producto.objects.create(
            categoria=self.cat,
            nombre="Producto Test",
            precio=Decimal("19990"),
            stock=10,
            imagen_url="https://example.com/img.jpg",
        )

    def test_admin_accede_a_lista_productos(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("lista_productos"))
        self.assertEqual(response.status_code, 200)

    def test_cliente_no_accede_a_lista_productos(self):
        self.client.login(username="cliente", password="cliente123")
        response = self.client.get(reverse("lista_productos"))
        self.assertNotEqual(response.status_code, 200)

    def test_anonimo_no_accede_a_lista_productos(self):
        response = self.client.get(reverse("lista_productos"))
        self.assertNotEqual(response.status_code, 200)

    def test_admin_accede_a_crear_producto(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("crear_producto"))
        self.assertEqual(response.status_code, 200)

    def test_admin_crea_producto(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.post(reverse("crear_producto"), {
            "categoria": self.cat.id,
            "nombre": "Nuevo",
            "precio": "5000",
            "stock": "5",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Producto.objects.filter(nombre="Nuevo").exists())

    def test_admin_edita_producto(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.post(
            reverse("actualizar_producto", args=[self.prod.id]),
            {"nombre": "Editado", "precio": "25000", "stock": "8"},
            follow=True,
        )
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.nombre, "Editado")

    def test_admin_elimina_producto(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.post(
            reverse("eliminar_producto", args=[self.prod.id]), follow=True
        )
        self.assertFalse(Producto.objects.filter(id=self.prod.id).exists())


class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("cliente", "c@t.com", "pass123")
        self.prod = Producto.objects.create(
            nombre="Producto Test",
            precio=Decimal("19990"),
            stock=10,
            imagen_url="https://example.com/img.jpg",
        )

    def test_anonimo_no_ve_carrito(self):
        response = self.client.get(reverse("ver_carrito"))
        self.assertNotEqual(response.status_code, 200)

    def test_ver_carrito_vacio(self):
        self.client.login(username="cliente", password="pass123")
        response = self.client.get(reverse("ver_carrito"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "vacío")

    def test_agregar_al_carrito(self):
        self.client.login(username="cliente", password="pass123")
        response = self.client.get(
            reverse("agregar_al_carrito", args=[self.prod.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        carrito = self.client.session.get("carrito", {})
        self.assertIn(str(self.prod.id), carrito)

    def test_agregar_producto_agotado(self):
        self.client.login(username="cliente", password="pass123")
        self.prod.stock = 0
        self.prod.save()
        response = self.client.get(
            reverse("agregar_al_carrito", args=[self.prod.id]), follow=True
        )
        self.assertContains(response, "agotado")

    def test_actualizar_carrito(self):
        self.client.login(username="cliente", password="pass123")
        self.client.get(reverse("agregar_al_carrito", args=[self.prod.id]))
        response = self.client.post(
            reverse("actualizar_carrito", args=[self.prod.id]),
            {"cantidad": "3"},
            follow=True,
        )
        carrito = self.client.session.get("carrito", {})
        self.assertEqual(carrito[str(self.prod.id)]["cantidad"], 3)

    def test_actualizar_carrito_cantidad_cero_elimina(self):
        self.client.login(username="cliente", password="pass123")
        self.client.get(reverse("agregar_al_carrito", args=[self.prod.id]))
        self.client.post(
            reverse("actualizar_carrito", args=[self.prod.id]),
            {"cantidad": "0"},
            follow=True,
        )
        carrito = self.client.session.get("carrito", {})
        self.assertNotIn(str(self.prod.id), carrito)

    def test_eliminar_del_carrito(self):
        self.client.login(username="cliente", password="pass123")
        self.client.get(reverse("agregar_al_carrito", args=[self.prod.id]))
        response = self.client.get(
            reverse("eliminar_del_carrito", args=[self.prod.id]), follow=True
        )
        carrito = self.client.session.get("carrito", {})
        self.assertNotIn(str(self.prod.id), carrito)

    def test_carrito_muestra_items(self):
        self.client.login(username="cliente", password="pass123")
        self.client.get(reverse("agregar_al_carrito", args=[self.prod.id]))
        response = self.client.get(reverse("ver_carrito"))
        self.assertContains(response, "Producto Test")
        self.assertContains(response, "$19.990")

    def test_carrito_muestra_total(self):
        self.client.login(username="cliente", password="pass123")
        self.client.get(reverse("agregar_al_carrito", args=[self.prod.id]))
        response = self.client.get(reverse("ver_carrito"))
        self.assertContains(response, "$19.990")


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("cliente", "c@t.com", "pass123")
        self.prod = Producto.objects.create(
            nombre="Producto Test",
            precio=Decimal("19990"),
            stock=10,
            imagen_url="https://example.com/img.jpg",
        )
        self.client.login(username="cliente", password="pass123")
        self.client.get(reverse("agregar_al_carrito", args=[self.prod.id]))

    def test_confirmar_compra_get_muestra_resumen(self):
        response = self.client.get(reverse("confirmar_compra"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirmar Compra")

    def test_confirmar_compra_post_crea_orden(self):
        response = self.client.post(reverse("confirmar_compra"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Orden.objects.count(), 1)
        self.assertEqual(ItemOrden.objects.count(), 1)

    def test_orden_asociada_al_usuario(self):
        self.client.post(reverse("confirmar_compra"), follow=True)
        orden = Orden.objects.first()
        self.assertEqual(orden.usuario, self.user)

    def test_orden_items_tienen_datos_correctos(self):
        self.client.post(reverse("confirmar_compra"), follow=True)
        item = ItemOrden.objects.first()
        self.assertEqual(item.producto, self.prod)
        self.assertEqual(item.cantidad, 1)
        self.assertEqual(item.precio_unitario, self.prod.precio)

    def test_orden_reduce_stock(self):
        stock_inicial = self.prod.stock
        self.client.post(reverse("confirmar_compra"), follow=True)
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock, stock_inicial - 1)

    def test_orden_vacia_carrito_despues_compra(self):
        self.client.post(reverse("confirmar_compra"), follow=True)
        carrito = self.client.session.get("carrito", {})
        self.assertEqual(carrito, {})

    def test_confirmar_compra_carrito_vacio(self):
        self.client.post(reverse("confirmar_compra"), follow=True)
        response = self.client.get(reverse("confirmar_compra"), follow=True)
        self.assertContains(response, "vacío")

    def test_orden_confirmada_muestra_detalle(self):
        self.client.post(reverse("confirmar_compra"), follow=True)
        orden = Orden.objects.first()
        response = self.client.get(
            reverse("orden_confirmada", args=[orden.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Producto Test")

    def test_orden_confirmada_solo_para_el_usuario(self):
        otro = User.objects.create_user("otro", "o@t.com", "pass123")
        self.client.post(reverse("confirmar_compra"), follow=True)
        orden = Orden.objects.first()
        self.client.login(username="otro", password="pass123")
        response = self.client.get(
            reverse("orden_confirmada", args=[orden.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_no_stock_en_compra(self):
        self.prod.stock = 0
        self.prod.save()
        self.client.get(reverse("agregar_al_carrito", args=[self.prod.id]))
        response = self.client.post(reverse("confirmar_compra"), follow=True)
        self.assertContains(response, "Stock insuficiente")


class FormTests(TestCase):
    def setUp(self):
        Categoria.objects.create(nombre="Test")
        self.admin = User.objects.create_superuser(
            "admin", "a@t.com", "pass123"
        )

    def test_precio_negativo_rechazado(self):
        self.client.login(username="admin", password="pass123")
        response = self.client.post(reverse("crear_producto"), {
            "nombre": "Test",
            "precio": "-1000",
            "stock": "5",
        })
        self.assertNotEqual(response.status_code, 302)
        form = response.context.get("form")
        if form:
            self.assertIn("precio", form.errors)

    def test_precio_cero_rechazado(self):
        self.client.login(username="admin", password="pass123")
        response = self.client.post(reverse("crear_producto"), {
            "nombre": "Test",
            "precio": "0",
            "stock": "5",
        })
        self.assertNotEqual(response.status_code, 302)
        form = response.context.get("form")
        if form:
            self.assertIn("precio", form.errors)


class TemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("cliente", "c@t.com", "pass123")
        self.prod = Producto.objects.create(
            nombre="Producto Test",
            precio=Decimal("19990"),
            stock=10,
            imagen_url="https://example.com/img.jpg",
        )

    def test_navbar_muestra_carrito_si_autenticado(self):
        self.client.login(username="cliente", password="pass123")
        response = self.client.get(reverse("inicio"))
        self.assertContains(response, "Carrito")

    def test_navbar_muestra_login_si_anonimo(self):
        response = self.client.get(reverse("inicio"))
        self.assertContains(response, "Iniciar Sesión")

    def test_inicio_muestra_boton_agregar_carrito_para_cliente(self):
        self.client.login(username="cliente", password="pass123")
        response = self.client.get(reverse("inicio"))
        self.assertContains(response, "Agregar al Carrito")

    def test_inicio_no_muestra_boton_admin_para_cliente(self):
        self.client.login(username="cliente", password="pass123")
        response = self.client.get(reverse("inicio"))
        self.assertNotContains(response, "Editar")
        self.assertNotContains(response, "Eliminar")


class ContextProcessorTests(TestCase):
    def test_carrito_count_anonimo_es_cero(self):
        response = self.client.get(reverse("inicio"))
        self.assertEqual(response.context.get("carrito_count"), 0)

    def test_carrito_count_autenticado_sin_items_es_cero(self):
        user = User.objects.create_user("c", "c@t.com", "pass")
        self.client.login(username="c", password="pass")
        response = self.client.get(reverse("inicio"))
        self.assertEqual(response.context.get("carrito_count"), 0)

    def test_carrito_count_con_items(self):
        user = User.objects.create_user("c", "c@t.com", "pass")
        self.client.login(username="c", password="pass")
        prod = Producto.objects.create(
            nombre="P", precio=Decimal("1000"), stock=5
        )
        self.client.get(reverse("agregar_al_carrito", args=[prod.id]))
        self.client.get(reverse("agregar_al_carrito", args=[prod.id]))
        response = self.client.get(reverse("inicio"))
        self.assertEqual(response.context.get("carrito_count"), 2)
