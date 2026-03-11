#!/bin/bash

# Script de despliegue para Botica Virgen de Huata
# Uso: bash deploy.sh

echo "=========================================="
echo "Despliegue de Botica Virgen de Huata"
echo "=========================================="

# Actualizar código
echo "📦 Actualizando código..."
git pull origin main

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Reiniciar servicio
echo "🔄 Reiniciando servicio Gunicorn..."
sudo systemctl restart botica

echo "✅ ¡Despliegue completado!"
echo "=========================================="
