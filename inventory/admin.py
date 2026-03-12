from django.contrib import admin
from .models import Producto, Lote


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'precio_venta', 'stock_minimo', 'creado_por', 'fecha_creacion')
	search_fields = ('nombre', 'codigo_barra')


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
	list_display = ('id', 'producto', 'numero_lote', 'fecha_vencimiento', 'stock', 'creado_por', 'fecha_creacion')
	search_fields = ('numero_lote', 'producto__nombre')
