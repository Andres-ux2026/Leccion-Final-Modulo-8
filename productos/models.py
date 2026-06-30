from django.db import models
from django.conf import settings


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="productos"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    imagen_url = models.URLField(blank=True)

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="ordenes"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = "orden"
        verbose_name_plural = "ordenes"

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"


class ItemOrden(models.Model):
    orden = models.ForeignKey(
        Orden, on_delete=models.CASCADE, related_name="items"
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, null=True
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre if self.producto else 'Eliminado'}"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
