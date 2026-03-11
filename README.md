# 💊 Botica Virgen de Huata

**Sistema web de gestión de ventas e inventario para farmacias**

Sistema desarrollado con Django para facilitar la administración de medicamentos, lotes, ventas y control de usuarios.

## ✨ Características

✅ **Gestión de Productos/Medicamentos**
- Agregar, editar y ver medicamentos
- Control de stock mínimo
- Código de barras integrado

✅ **Control de Lotes**
- Registro de lotes con números y fechas de vencimiento
- Gestión de stock por lote
- Ordenamiento automático por vencimiento

✅ **Módulo de Ventas**
- Registrar ventas con múltiples medicamentos
- Métodos de pago: Efectivo, Yape, Plin, Tarjeta
- Cálculo automático de totales
- Historial de últimas ventas

✅ **Inventario en Tiempo Real**
- Vista completa de productos y lotes
- Control de stock disponible
- Alertas de vencimiento

✅ **Autenticación y Seguridad**
- Sistema de login/logout
- Registro de nuevas cuentas
- Recuperación de cuenta por email/teléfono
- Cambio de contraseña
- Perfiles de usuario

✅ **Panel Administrativo**
- Django Admin integrado
- Gestión completa de datos

## 🚀 Instalación Local

### Requisitos
- Python 3.10+
- pip
- Git
- SQLite (incluido con Python)

### Instalación paso a paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/Proyecto_Botica.git
cd Proyecto_Botica

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear usuario administrador
python manage.py createsuperuser

# 7. Ejecutar servidor de desarrollo
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000`

---

## 📖 Uso

### Primer acceso
1. Entra en http://127.0.0.1:8000/admin con tu cuenta admin
2. Ve a http://127.0.0.1:8000/login para el panel principal

### Módulos principales

**Menú Principal**
- 💳 Ventas - Registrar nuevas ventas
- 📦 Inventario - Ver productos y lotes
- 💊 Ingreso de Productos - Agregar medicamentos

**Gestión de Medicamentos**
- Nombre del medicamento
- Precio de venta
- Stock mínimo
- Lotes asociados

**Gestión de Lotes**
- Número de lote
- Fecha de vencimiento (mes/año)
- Stock disponible
- Asociado a medicamento

---

## 📦 Estructura del Proyecto

```
Proyecto_Botica/
├── botica/                 # Configuración principal
│   ├── settings.py        # Configuración Django
│   ├── urls.py            # Rutas principales
│   ├── wsgi.py            # WSGI para servidor
│   └── templates/         # Plantillas HTML
├── inventory/             # App de inventario
│   ├── models.py          # Modelos: Producto, Lote
│   ├── forms.py           # Formularios
│   └── views.py           # Vistas
├── sales/                 # App de ventas
│   ├── models.py          # Modelos: Venta, DetalleVenta
│   ├── forms.py           # Formularios
│   ├── views.py           # Vistas
│   └── services.py        # Lógica de ventas
├── manage.py              # CLI de Django
├── db.sqlite3             # Base de datos
├── requirements.txt       # Dependencias
├── DEPLOYMENT.md          # Guía de despliegue
└── README.md              # Este archivo
```

---

## 🌐 Despliegue en Producción

Consulta [DEPLOYMENT.md](./DEPLOYMENT.md) para instrucciones completas de:
- Despliegue en DigitalOcean
- Configuración de Gunicorn y Nginx
- SSL con Let's Encrypt
- Dominios gratuitos
- Monitoreo y mantenimiento

---

## 📱 Tecnologías usadas

- **Backend**: Django 6.0.3
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor web**: Nginx
- **Servidor WSGI**: Gunicorn
- **Autenticación**: Django Auth

---

## 🔑 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## 📝 Migraciones

Para crear nuevas migraciones después de cambiar modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Testing (Opcional)

```bash
python manage.py test
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📞 Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio.

---

## 🎯 Roadmap futuro

- [ ] Reportes de ventas avanzados
- [ ] Exportar datos a Excel/PDF
- [ ] Código QR para medicamentos
- [ ] App móvil (React Native)
- [ ] Dashboard con gráficos
- [ ] Integración con proveedores
- [ ] Notificaciones de stock bajo
- [ ] Multi-sucursal

---

**Hecho con ❤️ para Botica Virgen de Huata**
