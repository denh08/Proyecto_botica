from django import forms
from django.contrib.auth.models import User
from inventory.models import Producto


class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres'
        })
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña'
        })
    )
    telefono = forms.CharField(
        label="Número de teléfono",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+51 999 999 999'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu_correo@ejemplo.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        if password and len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener mínimo 8 caracteres.")
        
        return self.cleaned_data


class VentaForm(forms.Form):
    producto_1 = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        label="Producto 1",
        required=False,
        empty_label="Seleccione un producto"
    )
    cantidad_1 = forms.IntegerField(min_value=1, label="Cantidad 1", required=False)
    producto_2 = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        label="Producto 2",
        required=False,
        empty_label="Seleccione un producto"
    )
    cantidad_2 = forms.IntegerField(min_value=1, label="Cantidad 2", required=False)
    producto_3 = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        label="Producto 3",
        required=False,
        empty_label="Seleccione un producto"
    )
    cantidad_3 = forms.IntegerField(min_value=1, label="Cantidad 3", required=False)
    cliente = forms.CharField(max_length=200, required=False, label="Cliente")
    metodo_pago = forms.ChoiceField(
        choices=[
            ("EFECTIVO", "Efectivo"),
            ("YAPE", "Yape"),
            ("PLIN", "Plin"),
            ("TARJETA", "Tarjeta"),
        ],
        label="Método de pago"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for indice in range(1, 4):
            self.fields[f"producto_{indice}"].widget.attrs.update({
                "class": "form-control"
            })
            self.fields[f"cantidad_{indice}"].widget.attrs.update({
                "class": "form-control",
                "placeholder": "Ingrese cantidad"
            })
        self.fields["cliente"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nombre del cliente"
        })
        self.fields["metodo_pago"].widget.attrs.update({
            "class": "form-control"
        })

    def clean(self):
        cleaned_data = super().clean()
        items = []
        productos_ids = []

        for indice in range(1, 4):
            producto = cleaned_data.get(f"producto_{indice}")
            cantidad = cleaned_data.get(f"cantidad_{indice}")

            if producto and not cantidad:
                self.add_error(f"cantidad_{indice}", "Ingresa la cantidad para este producto.")
            elif cantidad and not producto:
                self.add_error(f"producto_{indice}", "Selecciona el producto para esta cantidad.")
            elif producto and cantidad:
                if producto.id in productos_ids:
                    self.add_error(f"producto_{indice}", "No repitas el mismo producto en la misma venta.")
                productos_ids.append(producto.id)
                items.append({
                    "producto": producto,
                    "cantidad": cantidad,
                })

        if not items:
            raise forms.ValidationError("Debes seleccionar al menos un producto para registrar la venta.")

        cleaned_data["items_venta"] = items
        return cleaned_data

    def obtener_items_venta(self):
        return self.cleaned_data.get("items_venta", [])


class AccountRecoveryForm(forms.Form):
    METODO_CHOICES = [
        ('email', 'Por correo electrónico'),
        ('telefono', 'Por número de teléfono'),
    ]
    
    metodo = forms.ChoiceField(
        choices=METODO_CHOICES,
        widget=forms.RadioSelect,
        label="Selecciona el método de recuperación"
    )
    dato = forms.CharField(
        max_length=200,
        label="Correo electrónico o número de teléfono",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com o +51 999 999 999'
        })
    )
    
    def clean_dato(self):
        dato = self.cleaned_data.get('dato')
        metodo = self.cleaned_data.get('metodo')
        
        if metodo == 'email':
            if '@' not in dato:
                raise forms.ValidationError("Ingresa un correo electrónico válido.")
            usuario = User.objects.filter(email=dato).first()
            if not usuario:
                raise forms.ValidationError("No existe una cuenta con este correo electrónico.")
        elif metodo == 'telefono':
            usuario = User.objects.filter(profile__telefono=dato).first()
            if not usuario:
                raise forms.ValidationError("No existe una cuenta con este número de teléfono.")
        
        return dato