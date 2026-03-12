from django.contrib import admin
from .models import Venta, DetalleVenta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
	list_display = ('id', 'fecha', 'cliente', 'metodo_pago', 'total', 'registrado_por')
	search_fields = ('cliente', 'registrado_por__username')


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
	list_display = ('venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
	search_fields = ('producto__nombre', 'venta__cliente')
