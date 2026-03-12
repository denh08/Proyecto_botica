from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from inventory.models import Producto, Lote
from inventory.forms import ProductoConLoteForm
from .forms import VentaForm, AccountRecoveryForm, RegistroForm
from .services import registrar_venta, StockInsuficienteError
from .models import Venta, UserProfile


def _build_recovery_url(request, uid, token):
    path = reverse('recuperar_confirmar', args=[uid, token])
    base_url = getattr(settings, 'SITE_URL', '').strip().rstrip('/')
    if base_url:
        return f"{base_url}{path}"
    return request.build_absolute_uri(path)


@login_required
def inicio(request):
    return render(request, 'inicio.html')


@login_required
def ventas(request):
    productos = Producto.objects.filter(activo=True)

    productos_info = []
    for producto in productos:
        stock_total = sum(lote.stock for lote in Lote.objects.filter(producto=producto))
        productos_info.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio_venta),
            'stock': stock_total,
        })

    ultimas_ventas = Venta.objects.prefetch_related('detalles__producto').order_by('-id')[:10]

    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data["cliente"]
            metodo_pago = form.cleaned_data["metodo_pago"]
            items_venta = form.obtener_items_venta()

            try:
                venta = registrar_venta(
                    items=items_venta,
                    cliente=cliente,
                    metodo_pago=metodo_pago
                )
                messages.success(
                    request,
                    f"Venta registrada correctamente. N° {venta.id} - Total S/ {venta.total}"
                )
                return redirect("ventas")
            except StockInsuficienteError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Ocurrió un error al registrar la venta: {e}")
    else:
        form = VentaForm()

    return render(request, 'ventas.html', {
        'form': form,
        'productos_info': productos_info,
        'ultimas_ventas': ultimas_ventas,
    })


@login_required
def inventario(request):
    productos = Producto.objects.all()
    lotes = Lote.objects.all()
    return render(request, 'inventario.html', {
        'productos': productos,
        'lotes': lotes,
    })


@login_required
def ingreso_productos(request):
    if request.method == "POST":
        form = ProductoConLoteForm(request.POST)
        if form.is_valid():
            # Crear el producto (precio_compra se establece igual al precio_venta)
            producto = Producto.objects.create(
                codigo_barra=form.cleaned_data['codigo_barra'],
                nombre=form.cleaned_data['nombre'],
                precio_compra=form.cleaned_data['precio_venta'],  # Se establece igual al precio de venta
                precio_venta=form.cleaned_data['precio_venta'],
                stock_minimo=form.cleaned_data['stock_minimo'],
                creado_por=request.user,
            )
            
            # Procesar fecha de vencimiento (formato mes-año a fecha con día 1)
            fecha_str = form.cleaned_data['fecha_vencimiento']
            from datetime import datetime
            try:
                fecha_vencimiento = datetime.strptime(fecha_str, '%Y-%m').date().replace(day=1)
            except ValueError:
                fecha_vencimiento = None
            
            # Crear el lote asociado
            lote = Lote.objects.create(
                producto=producto,
                numero_lote=form.cleaned_data['numero_lote'],
                fecha_vencimiento=fecha_vencimiento,
                stock=form.cleaned_data['stock'],
                creado_por=request.user,
            )
            
            messages.success(
                request,
                f"✅ Medicamento '{producto.nombre}' y lote '{lote.numero_lote}' agregados exitosamente"
            )
            return redirect("ingreso_productos")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductoConLoteForm()
    
    # Obtener lista de medicamentos y lotes recientes
    medicamentos = Producto.objects.filter(activo=True).order_by('-id')[:15]
    lotes_recientes = Lote.objects.select_related('producto').order_by('-id')[:10]
    
    return render(request, 'ingreso_productos.html', {
        'form': form,
        'medicamentos': medicamentos,
        'lotes_recientes': lotes_recientes,
    })


def recuperar_cuenta(request):
    """Vista para iniciar el proceso de recuperación de cuenta"""
    if request.method == "POST":
        form = AccountRecoveryForm(request.POST)
        if form.is_valid():
            metodo = form.cleaned_data['metodo']
            dato = form.cleaned_data['dato']
            
            # Buscar el usuario
            if metodo == 'email':
                usuario = User.objects.filter(email=dato).first()
            else:  # telefono
                usuario = User.objects.filter(profile__telefono=dato).first()
            
            if usuario:
                # Generar token y uid para reset
                uid = urlsafe_base64_encode(force_bytes(usuario.pk))
                token = default_token_generator.make_token(usuario)
                
                if metodo == 'email':
                    recovery_url = _build_recovery_url(request, uid, token)
                    # Enviar email
                    asunto = "Recuperación de cuenta - Botica Virgen de Huata"
                    mensaje = f"""
Hola {usuario.username},

Recibimos una solicitud para recuperar tu cuenta. Haz clic en el siguiente enlace para establecer una nueva contraseña:

{recovery_url}

Si no solicitaste este cambio, ignora este mensaje.

Saludos,
Botica Virgen de Huata
"""
                    try:
                        send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [usuario.email])
                        messages.success(request, f"Se ha enviado un enlace de recuperación a {usuario.email}. Revisa tu bandeja de entrada.")
                    except Exception as e:
                        messages.error(request, "Ocurrió un error al enviar el email. Intenta más tarde.")
                
                elif metodo == 'telefono':
                    # Mostrar código para teléfono (simulado)
                    messages.success(
                        request, 
                        f"Se ha enviado un código de recuperación al teléfono {usuario.profile.telefono}. " +
                        "Para continuar, haz clic en: " +
                        f"<a href='/recuperar/{uid}/{token}/'>aquí</a>",
                        extra_tags='safe'
                    )
                
                return redirect('recuperar_cuenta')
    else:
        form = AccountRecoveryForm()
    
    return render(request, 'recuperar_cuenta.html', {'form': form})


def recuperar_confirmar(request, uidb64, token):
    """Vista para confirmar el reset de contraseña"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usuario = None
    
    if usuario and default_token_generator.check_token(usuario, token):
        if request.method == 'POST':
            nueva_contrasena = request.POST.get('nueva_contrasena')
            confirmar_contrasena = request.POST.get('confirmar_contrasena')
            
            if nueva_contrasena and nueva_contrasena == confirmar_contrasena:
                usuario.set_password(nueva_contrasena)
                usuario.save()
                messages.success(request, "Tu contraseña ha sido actualizada correctamente. Ahora puedes iniciar sesión.")
                return redirect('login')
            else:
                messages.error(request, "Las contraseñas no coinciden o están vacías.")
        
        return render(request, 'recuperar_confirmar.html')
    else:
        messages.error(request, "El enlace de recuperación es inválido o ha expirado.")
        return redirect('recuperar_cuenta')


def registro(request):
    """Vista para crear una nueva cuenta de usuario"""
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            
            # Crear perfil de usuario con teléfono
            telefono = form.cleaned_data.get('telefono', '')
            UserProfile.objects.create(user=usuario, telefono=telefono if telefono else None)
            
            messages.success(request, f"¡Bienvenido {usuario.username}! Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})


@login_required
def editar_producto(request, producto_id):
    """Vista para editar un producto existente"""
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        messages.error(request, "El producto no existe.")
        return redirect('ingreso_productos')
    
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        precio_venta = request.POST.get('precio_venta', '')
        stock_minimo = request.POST.get('stock_minimo', '')
        codigo_barra = request.POST.get('codigo_barra', '').strip()
        
        # Validaciones
        errores = []
        if not nombre:
            errores.append("El nombre del medicamento es requerido.")
        
        try:
            precio_venta = float(precio_venta)
            if precio_venta <= 0:
                errores.append("El precio de venta debe ser mayor a 0.")
        except (ValueError, TypeError):
            errores.append("El precio de venta debe ser un número válido.")
        
        try:
            stock_minimo = int(stock_minimo)
            if stock_minimo < 0:
                errores.append("El stock mínimo no puede ser negativo.")
        except (ValueError, TypeError):
            errores.append("El stock mínimo debe ser un número entero.")
        
        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            producto.nombre = nombre
            producto.precio_venta = precio_venta
            producto.precio_compra = precio_venta
            producto.stock_minimo = stock_minimo
            producto.codigo_barra = codigo_barra
            producto.save()
            
            messages.success(request, f"✅ El medicamento '{producto.nombre}' ha sido actualizado correctamente.")
            return redirect('ingreso_productos')
    
    return render(request, 'editar_producto.html', {'producto': producto})