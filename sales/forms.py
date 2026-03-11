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
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        label="Producto"
    )
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")
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

        self.fields["producto"].widget.attrs.update({
            "class": "form-control"
        })
        self.fields["cantidad"].widget.attrs.update({
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