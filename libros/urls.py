from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('lista/', views.lista_libros, name='lista_libros'),
    path('crear/', views.crear_libro, name='crear_libro'),
    path('editar/<int:id>/', views.actualizar_libros, name='actualizar_libros'),
    path('eliminar/<int:id>/', views.Eliminar_libros, name='eliminar_libros'),
]