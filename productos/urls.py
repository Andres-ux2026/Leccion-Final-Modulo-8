from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("create/", views.crear_producto, name="crear_producto"),
    path("list/", views.lista_productos, name="lista_productos"),
    path("edit/<int:id>/", views.actualizar_producto, name="actualizar_producto"),
    path("delete/<int:id>/", views.eliminar_producto, name="eliminar_producto"),
    path("cart/", views.ver_carrito, name="ver_carrito"),
    path("cart/add/<int:id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("cart/update/<int:id>/", views.actualizar_carrito, name="actualizar_carrito"),
    path("cart/remove/<int:id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path("cart/checkout/", views.confirmar_compra, name="confirmar_compra"),
    path("order/<int:orden_id>/", views.orden_confirmada, name="orden_confirmada"),
]
