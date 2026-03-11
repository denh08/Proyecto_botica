from django import forms
from .models import Producto, Lote


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_barra', 'nombre', 'precio_compra', 'precio_venta', 'stock_minimo']
        labels = {
            'codigo_barra': 'Código de barra',
            'nombre': 'Nombre del medicamento',
            'precio_compra': 'Precio de compra (S/)',
            'precio_venta': 'Precio de venta (S/)',
            'stock_minimo': 'Stock mínimo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar estilos a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })


class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['numero_lote', 'fecha_vencimiento', 'stock']
        labels = {
            'numero_lote': 'Número de lote',
            'fecha_vencimiento': 'Fecha de vencimiento',
            'stock': 'Stock disponible',
        }
        widgets = {
            'numero_lote': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345A'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible',
                'min': '0'
            }),
        }


class ProductoConLoteForm(forms.Form):
    """Formulario combinado para crear Producto y Lote simultáneamente"""
    
    # Campos del Producto
    codigo_barra = forms.CharField(
        max_length=50,
        required=False,
        label="Código de barra",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código de barra (opcional)'
        })
    )
    nombre = forms.CharField(
        max_length=200,
        label="Nombre del medicamento",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del medicamento'
        })
    )
    precio_venta = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Precio de venta (S/)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    stock_minimo = forms.IntegerField(
        initial=10,
        label="Stock mínimo",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '10',
            'min': '0'
        })
    )
    
    # Campos del Lote
    numero_lote = forms.CharField(
        max_length=50,
        label="Número de lote",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 12345A'
        })
    )
    fecha_vencimiento = forms.CharField(
        label="Fecha de vencimiento (MM/YYYY)",
        max_length=7,
        widget=forms.TextInput(attrs={
            'type': 'month',
            'class': 'form-control',
            'placeholder': 'MM/YYYY'
        }),
        help_text="Ingresa el mes y año de vencimiento"
    )
    stock = forms.IntegerField(
        min_value=0,
        label="Stock disponible (para este lote)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad disponible',
            'min': '0'
        })
    )
