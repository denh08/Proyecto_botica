from django.db import models


class Producto(models.Model):
    codigo_barra = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=200)

    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    stock_minimo = models.IntegerField(default=0)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    numero_lote = models.CharField(max_length=50)

    fecha_vencimiento = models.DateField()

    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre} - Lote {self.numero_lote}"