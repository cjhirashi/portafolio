# Portafolio — Carlos A. Jiménez Hirashi

Sitio de portafolio personal construido en Django. Implementa el diseño de [Claude Design](https://claude.ai/design) para cjhirashi.com: páginas de inicio, proyectos, blog, sobre mí y contacto, con modelos reales, formulario funcional y tema claro/oscuro.

## Stack

- **Backend**: Django 5.2
- **Base de datos**: SQLite en desarrollo, PostgreSQL en producción (se activa sola según `.env`)
- **Frontend**: HTML + CSS + JS vanilla (sin framework de JS ni build step), íconos [Lucide](https://lucide.dev/)
- **Markdown**: los artículos de blog se escriben en Markdown y se renderizan con `python-markdown`
- **Imágenes**: `Pillow` para `ImageField`
- **Producción**: `gunicorn` + `nginx`

## Páginas

| Página | Ruta | Descripción |
|---|---|---|
| Home | `/` | Hero, estadísticas animadas, caso de estudio destacado, proyectos y artículos recientes |
| Proyectos | `/proyectos/` | Listado con búsqueda, filtro por categoría/industria y orden por año |
| Detalle de proyecto | `/proyectos/<slug>/` | Contexto, solución, arquitectura, resultados, galería y stack — las secciones sin contenido se ocultan solas |
| Blog | `/blog/` | Listado con búsqueda, filtro por pilar temático y orden por fecha |
| Detalle de artículo | `/blog/<slug>/` | Contenido en Markdown, tags, tarjeta de autor y siguiente artículo |
| Sobre mí | `/sobre-mi/` | Filosofía, trayectoria, certificaciones y habilidades técnicas |
| Contacto | `/contacto/` | Formulario que envía un correo real (con validación y manejo de errores) |

## Estructura del proyecto

```
config/                  # Configuración de Django (settings, urls, wsgi/asgi)
core/                     # App principal
  models.py               # Project, Post y sus modelos relacionados (métricas, pasos, galería, etc.)
  views.py                # Vistas de todas las páginas
  forms.py                # Formulario de contacto
  admin.py                # Admin con inlines para editar contenido
  management/commands/    # seed_projects, seed_blog — datos de muestra
  templates/core/         # Templates HTML
  static/core/            # CSS y JS por página
deploy/                   # Plantillas de gunicorn.service y nginx.conf para el VPS
requirements.txt
.env.example
manage.py
```

## Puesta en marcha local

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

pip install -r requirements.txt

copy .env.example .env          # Windows
# cp .env.example .env          # Linux/Mac

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sin `DB_NAME` en `.env`, el proyecto usa SQLite automáticamente — no hace falta tener PostgreSQL instalado para desarrollar en local.

### Datos de muestra (opcional)

Para no arrancar con las páginas de Proyectos y Blog vacías:

```bash
python manage.py seed_projects
python manage.py seed_blog
```

Ambos comandos son idempotentes (se pueden correr varias veces sin duplicar datos).

## Variables de entorno

Ver [`.env.example`](.env.example) para la lista completa. Las más relevantes:

| Variable | Uso |
|---|---|
| `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` | Configuración estándar de Django |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Si `DB_NAME` está vacío usa SQLite; si no, PostgreSQL |
| `EMAIL_*`, `CONTACT_RECIPIENT_EMAIL` | Envío del formulario de contacto (backend de consola en desarrollo) |
| `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_*` | Endurecimiento de seguridad — dejar en `False` hasta tener HTTPS funcionando en producción |

## Despliegue

El procedimiento completo de despliegue al VPS (Hostinger, PostgreSQL existente, nginx + gunicorn + certbot) está documentado en `DEPLOY.md`, que **se mantiene solo en local** y no se sube a este repositorio.
