# 🚀 Guía de Despliegue - Botica Virgen de Huata

## Requisitos previos
- Cuenta en DigitalOcean, AWS, o similar
- Dominio (por ahora usaremos subdominio gratuito)
- Acceso SSH al servidor

## 📋 Opción 1: Despliegue en DigitalOcean (Recomendado)

### Paso 1: Crear un Droplet
1. Accede a [DigitalOcean](https://www.digitalocean.com)
2. Haz clic en **Create** → **Droplet**
3. Selecciona:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($4/mes - suficiente para empezar)
   - **Region**: Cercana a tus usuarios
   - **Authentication**: SSH key

### Paso 2: Conectar al servidor
```bash
ssh root@tu_ip_del_droplet
```

### Paso 3: Instalar dependencias
```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Python y herramientas
apt install -y python3 python3-pip python3-venv git nginx

# Instalar Supervisor (para mantener Gunicorn corriendo)
apt install -y supervisor
```

### Paso 4: Clonar el proyecto
```bash
cd /home
mkdir botica
cd botica
git clone https://github.com/tu-usuario/Proyecto_Botica.git proyecto_botica
cd proyecto_botica

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Crear archivo .env
```bash
nano .env
```

Copia esto y modifica según sea necesario:
```
DEBUG=False
SECRET_KEY=usa-este-comando-para-generar: python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,tu-ip
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Paso 6: Preparar aplicación
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Crear usuario admin
```

### Paso 7: Configurar Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Probar Gunicorn
gunicorn --workers 3 --bind 0.0.0.0:8000 botica.wsgi:application
```

### Paso 8: Crear servicio systemd
```bash
sudo nano /etc/systemd/system/botica.service
```

Copia el contenido de `botica.service` (ajusta el usuario si es necesario).

```bash
# Habilitar el servicio
sudo systemctl daemon-reload
sudo systemctl start botica
sudo systemctl enable botica
sudo systemctl status botica
```

### Paso 9: Configurar Nginx
```bash
sudo nano /etc/nginx/sites-available/botica
```

Copia el contenido de `nginx_botica.conf` (sin la sección SSL por ahora).

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/botica /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 10: Configurar HTTPS con Let's Encrypt (⭐ Importante)
```bash
# Instalar Certbot
apt install -y certbot python3-certbot-nginx

# Obtener certificado SSL
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovación automática
systemctl enable certbot.timer
```

### Paso 11: Configurar dominio gratuito
Si no tienes dominio, usa **noip.com** o **FreeDNS**:
1. Registra account en [No-IP](https://www.noip.com)
2. Crea hostname: `botica-hospital.ddns.net`
3. Apunta a tu IP del droplet
4. Actualiza `ALLOWED_HOSTS` en `.env`

---

## 📋 Opción 2: Despliegue en Vercel/Heroku (Más fácil, menos control)

### Heroku (Gratuito con limitaciones)
```bash
# Instalar Heroku CLI
npm install -g heroku

# Conectar con Heroku
heroku login
heroku create tu-app-botica

# Establecer variables de entorno
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=tu-clave-secreta

# Desplegar
git push heroku main
```

---

## 🔄 Actualizar la aplicación

```bash
cd /home/botica/proyecto_botica
source venv/bin/activate

# Tirar cambios del repositorio
git pull origin main

# Instalar nuevas dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Reiniciar servicio
sudo systemctl restart botica
```

O simplemente ejecuta el script:
```bash
bash deploy.sh
```

---

## 🐛 Solución de problemas

### Gunicorn no inicia
```bash
sudo systemctl status botica
sudo journalctl -u botica -n 50
```

### Nginx no funciona
```bash
sudo nginx -t  # Verifica sintaxis
sudo systemctl restart nginx
sudo tail -f /var/log/nginx/error.log
```

### Permisos denegados
```bash
sudo chown -R www-data:www-data /home/botica/proyecto_botica
```

---

## 📊 Monitoreo

### Ver logs en tiempo real
```bash
sudo journalctl -u botica -f
```

### Reiniciar la aplicación
```bash
sudo systemctl restart botica
```

### Verificar estado
```bash
sudo systemctl status botica
curl http://tu-dominio.com
```

---

## ✅ Checklist final

- [ ] Servidor creado en DigitalOcean/AWS
- [ ] SSH configurado
- [ ] Código clonado
- [ ] Entorno virtual creado
- [ ] `.env` configurado correctamente
- [ ] Migraciones ejecutadas
- [ ] Gunicorn funcionando
- [ ] Nginx configurado
- [ ] SSL configurado (Let's Encrypt)
- [ ] Dominio apuntando al servidor
- [ ] Panel admin accesible
- [ ] Usuarios pueden registrarse y usar la app

---

## 🎯 Costos estimados

- **DigitalOcean Droplet**: $4-6/mes
- **Dominio**: Gratuito (No-IP) o $10-15/año (dominio propio)
- **Total**: ~$4-6/mes para hostear muchos usuarios

¡Tu aplicación estará en línea! 🚀
