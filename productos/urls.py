from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("create/", views.crear_producto, name="crear_producto"),
    path("list/", views.lista_productos, name="lista_productos"),
    path("edit/<int:id>/", views.actualizar_producto, name="actualizar_producto"),
    path("delete/<int:id>/", views.eliminar_producto, name="eliminar_producto"),
]
