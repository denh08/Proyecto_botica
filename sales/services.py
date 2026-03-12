from decimal import Decimal
from django.db import transaction
from inventory.models import Producto, Lote
from .models import Venta, DetalleVenta


class StockInsuficienteError(Exception):
    pass


def _registrar_detalles_venta(venta, producto, cantidad):
    lotes = Lote.objects.select_for_update().filter(
        producto=producto,
        stock__gt=0
    ).order_by("fecha_vencimiento")

    cantidad_restante = cantidad
    total_producto = Decimal("0.00")

    for lote in lotes:
        if cantidad_restante <= 0:
            break

        tomar = min(lote.stock, cantidad_restante)
        subtotal = Decimal(tomar) * producto.precio_venta

        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            lote=lote,
            cantidad=tomar,
            precio_unitario=producto.precio_venta,
            subtotal=subtotal
        )

        lote.stock -= tomar
        lote.save()

        total_producto += subtotal
        cantidad_restante -= tomar

    if cantidad_restante > 0:
        raise StockInsuficienteError(
            f"No hay stock suficiente para {producto.nombre}. Faltan {cantidad_restante} unidades."
        )

    return total_producto


@transaction.atomic
def registrar_venta(items, cliente="", metodo_pago="EFECTIVO", registrado_por=None):
    total_venta = Decimal("0.00")

    venta = Venta.objects.create(
        cliente=cliente,
        metodo_pago=metodo_pago,
        total=0,
        registrado_por=registrado_por,
    )

    for item in items:
        producto = item["producto"]
        if isinstance(producto, Producto):
            producto_obj = producto
        else:
            producto_obj = Producto.objects.get(id=producto)

        total_venta += _registrar_detalles_venta(venta, producto_obj, item["cantidad"])

    venta.total = total_venta
    venta.save()

    return venta