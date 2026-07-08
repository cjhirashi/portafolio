# Despliegue a producción — cjhirashi.com (VPS Hostinger)

Este documento asume:
- VPS Hostinger con **Ubuntu** (22.04 o 24.04).
- Ya existe un portafolio incompleto corriendo en ese VPS con PostgreSQL — **vamos a reutilizar esa misma base de datos** y reemplazar el sitio.
- Tienes acceso SSH al VPS y el dominio `cjhirashi.com` ya apunta a la IP del VPS.

Sigue los pasos en orden. Cada bloque de comandos se ejecuta por SSH en el VPS, salvo que se indique lo contrario.

---

## 0. Antes de empezar — qué ya se validó localmente

- `python manage.py check` — sin errores.
- `python manage.py collectstatic` — funciona (antes fallaba por falta de `STATIC_ROOT`, ya está corregido).
- El proyecto usa PostgreSQL automáticamente si defines `DB_NAME` en `.env`; si lo dejas vacío, usa SQLite (así sigue funcionando en tu máquina local sin tocar nada).
- `gunicorn` **no se puede probar en Windows** (depende de `fcntl`, solo existe en Linux) — su primera prueba real será en el VPS. Esto es normal y esperado.
- Las banderas de seguridad (`SECURE_SSL_REDIRECT`, etc.) vienen apagadas por defecto para no romper nada antes de tener HTTPS funcionando.

---

## 1. Identificar y detener el sitio viejo

Antes de tocar nada, identifica cómo está corriendo el portafolio incompleto actual:

```bash
sudo systemctl list-units --type=service | grep -i -E "gunicorn|django|portfolio|portafolio"
sudo ls /etc/nginx/sites-enabled/
```

Anota el nombre del servicio systemd y el archivo de nginx que encuentres — los vas a deshabilitar (no borrar todavía, por si necesitas rescatar algo):

```bash
sudo systemctl stop NOMBRE_DEL_SERVICIO_VIEJO
sudo systemctl disable NOMBRE_DEL_SERVICIO_VIEJO
sudo rm /etc/nginx/sites-enabled/NOMBRE_DEL_SITIO_VIEJO
sudo nginx -t
sudo systemctl reload nginx
```

**No borres la base de datos PostgreSQL** — la vamos a reutilizar en el paso 4.

---

## 2. Paquetes del sistema

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx postgresql-client certbot python3-certbot-nginx git
```

---

## 3. Subir el código

Si tu proyecto está en GitHub:

```bash
cd ~
git clone <URL_DE_TU_REPO> portafolio-cjhirashi
cd portafolio-cjhirashi
```

Si prefieres subirlo directamente desde tu PC (sin GitHub), desde tu máquina Windows con este proyecto:

```bash
# Ejecutar en tu PC, no en el VPS
rsync -avz --exclude='.venv' --exclude='__pycache__' --exclude='db.sqlite3' --exclude='_design_handoff' --exclude='*.zip' ./ USUARIO@IP_DEL_VPS:~/portafolio-cjhirashi/
```

---

## 4. Entorno virtual y dependencias

```bash
cd ~/portafolio-cjhirashi
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Configurar `.env` de producción

```bash
cp .env.example .env
nano .env
```

Rellena así (usa las credenciales **reales** de la base de datos PostgreSQL que ya existe en el VPS):

```bash
SECRET_KEY=<genera-una-nueva-abajo>
DEBUG=False
ALLOWED_HOSTS=cjhirashi.com,www.cjhirashi.com
CSRF_TRUSTED_ORIGINS=https://cjhirashi.com,https://www.cjhirashi.com

DB_NAME=<nombre-de-tu-bd-existente>
DB_USER=<usuario-de-tu-bd-existente>
DB_PASSWORD=<password-de-tu-bd-existente>
DB_HOST=localhost
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=<tu-servidor-smtp>
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<tu-usuario-smtp>
EMAIL_HOST_PASSWORD=<tu-password-smtp>
DEFAULT_FROM_EMAIL=no-reply@cjhirashi.com
CONTACT_RECIPIENT_EMAIL=carlos@cjhirashi.com

# Dejar en False por ahora — se activan en el paso 9, después de confirmar HTTPS
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

Para generar un `SECRET_KEY` nuevo y seguro:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Verifica que puedes conectar a la base de datos existente** antes de seguir:

```bash
psql -h localhost -U <DB_USER> -d <DB_NAME> -c "\dt"
```

Si pide password y conecta (aunque la lista de tablas sea la del portafolio viejo), estás listo para el siguiente paso.

---

## 6. Migraciones, superusuario y estáticos

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

`migrate` crea las tablas de este proyecto nuevo dentro de la misma base de datos — no toca ni borra tablas de otros proyectos que pudieran existir ahí.

(Opcional) Si quieres los proyectos/artículos de blog de muestra para no lanzar el sitio vacío mientras cargas tu contenido real:

```bash
python manage.py seed_projects
python manage.py seed_blog
```

---

## 7. Gunicorn como servicio systemd

Copia y adapta la plantilla (reemplaza `REEMPLAZA_USUARIO` por tu usuario real del VPS):

```bash
sed "s/REEMPLAZA_USUARIO/$USER/g" deploy/gunicorn.service | sudo tee /etc/systemd/system/portafolio-cjhirashi.service

sudo systemctl daemon-reload
sudo systemctl enable portafolio-cjhirashi
sudo systemctl start portafolio-cjhirashi
sudo systemctl status portafolio-cjhirashi --no-pager
```

Prueba que gunicorn responde localmente en el VPS:

```bash
curl -I http://127.0.0.1:8000/
```

Si da error, revisa logs con `sudo journalctl -u portafolio-cjhirashi -n 50 --no-pager`.

---

## 8. nginx

```bash
sed "s/REEMPLAZA_USUARIO/$USER/g" deploy/nginx.conf | sudo tee /etc/nginx/sites-available/portafolio-cjhirashi

sudo ln -sf /etc/nginx/sites-available/portafolio-cjhirashi /etc/nginx/sites-enabled/portafolio-cjhirashi
sudo nginx -t
sudo systemctl reload nginx
```

Prueba por HTTP (todavía sin HTTPS):

```bash
curl -I http://cjhirashi.com/
```

Deberías ver `200 OK`. Si quieres confirmar visualmente, abre `http://cjhirashi.com/` en el navegador.

---

## 9. HTTPS con certbot

```bash
sudo certbot --nginx -d cjhirashi.com -d www.cjhirashi.com
```

Certbot va a modificar `/etc/nginx/sites-available/portafolio-cjhirashi` automáticamente para agregar el bloque HTTPS y el redirect. Cuando termine:

```bash
curl -I https://cjhirashi.com/
```

**Solo después de confirmar que `https://cjhirashi.com/` carga bien**, activa las banderas de seguridad:

```bash
nano .env
```

Cambia:
```bash
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=3600
```

(Empieza con `SECURE_HSTS_SECONDS=3600` — una hora — y solo súbelo a algo como `31536000` semanas después, cuando estés seguro de que todo funciona bien por HTTPS. HSTS es difícil de revertir rápido.)

Reinicia gunicorn para que tome el `.env` actualizado:

```bash
sudo systemctl restart portafolio-cjhirashi
```

---

## 10. Checklist final de verificación

- [ ] `https://cjhirashi.com/` carga (Home)
- [ ] `https://cjhirashi.com/proyectos/` carga, filtros y búsqueda funcionan
- [ ] `https://cjhirashi.com/blog/` carga, filtros y búsqueda funcionan
- [ ] `https://cjhirashi.com/sobre-mi/` carga
- [ ] `https://cjhirashi.com/contacto/` — envía un mensaje de prueba y confirma que llega el correo real
- [ ] El menú hamburguesa funciona en móvil (achica la ventana del navegador o pruébalo desde tu celular)
- [ ] `https://cjhirashi.com/admin/` — puedes entrar con el superusuario creado en el paso 6
- [ ] Los CSS/imágenes cargan bien (si se ven sin estilos, revisa que `collectstatic` corrió y que la ruta `alias` en nginx apunta al `staticfiles/` correcto)
- [ ] `http://cjhirashi.com/` (sin la S) redirige automáticamente a `https://`

Comandos útiles si algo falla:

```bash
sudo systemctl status portafolio-cjhirashi --no-pager   # estado de gunicorn
sudo journalctl -u portafolio-cjhirashi -n 100 --no-pager  # logs de gunicorn
sudo nginx -t                                             # valida la config de nginx
sudo tail -n 50 /var/log/nginx/error.log                  # errores de nginx
```

---

## 11. Actualizar el sitio después (cambios futuros)

```bash
cd ~/portafolio-cjhirashi
git pull   # o rsync desde tu PC otra vez
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart portafolio-cjhirashi
```

---

## Rollback (volver al portafolio viejo)

Si algo sale mal y necesitas volver rápido al sitio anterior mientras arreglas esto:

```bash
sudo systemctl stop portafolio-cjhirashi
sudo rm /etc/nginx/sites-enabled/portafolio-cjhirashi
sudo systemctl enable --now NOMBRE_DEL_SERVICIO_VIEJO   # el que anotaste en el paso 1
sudo ln -sf /etc/nginx/sites-available/NOMBRE_DEL_SITIO_VIEJO /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

La base de datos no se ve afectada por este rollback porque nunca se tocaron ni borraron tablas de otros proyectos.
