from decimal import Decimal
from django.db import transaction
from inventory.models import Producto, Lote
from .models import Venta, DetalleVenta


class StockInsuficienteError(Exception):
    pass


@transaction.atomic
def registrar_venta(producto_id, cantidad, cliente="", metodo_pago="EFECTIVO"):
    producto = Producto.objects.get(id=producto_id)

    lotes = Lote.objects.select_for_update().filter(
        producto=producto,
        stock__gt=0
    ).order_by("fecha_vencimiento")

    cantidad_restante = cantidad
    total_venta = Decimal("0.00")

    venta = Venta.objects.create(
        cliente=cliente,
        metodo_pago=metodo_pago,
        total=0
    )

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

        total_venta += subtotal
        cantidad_restante -= tomar

    if cantidad_restante > 0:
        raise StockInsuficienteError(
            f"No hay stock suficiente para {producto.nombre}. Faltan {cantidad_restante} unidades."
        )

    venta.total = total_venta
    venta.save()

    return venta