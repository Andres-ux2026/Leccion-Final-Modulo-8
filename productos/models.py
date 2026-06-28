from django.db import models

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
