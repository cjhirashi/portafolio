import markdown as markdown_lib
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

PILARES = ['Arquitectura', 'Data Science e IA', 'Pensamiento Sistémico']
PILAR_CHOICES = [(p, p) for p in PILARES]


class Project(models.Model):
    titulo = models.CharField(
        max_length=200,
        help_text='Nombre del proyecto. Aparece como título en la tarjeta del listado y en la página de detalle.',
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        help_text='Se genera solo a partir del título si lo dejas vacío. Define la URL: /proyectos/este-texto/',
    )
    categoria = models.CharField(
        max_length=60,
        help_text='Etiqueta corta, ej: Data, ML Ops, Systems. También funciona como filtro en el listado de Proyectos.',
    )
    industria = models.CharField(
        max_length=60,
        help_text='Etiqueta corta, ej: Fintech, Salud, Retail. También funciona como filtro en el listado.',
    )
    anio = models.PositiveIntegerField(help_text='Año del proyecto. Define el orden del listado (más reciente primero).')

    resultado = models.CharField(
        max_length=300,
        help_text='Resumen corto (1-2 líneas) para la tarjeta del listado y para "Proyectos destacados" del Home.',
    )
    resumen = models.TextField(
        help_text='Resumen largo mostrado como párrafo principal en la parte superior de la página de detalle.',
    )

    es_ancla = models.BooleanField(
        'Proyecto ancla',
        default=False,
        help_text='Actívalo solo en UN proyecto a la vez: ese es el que se muestra en la sección "Caso ancla" del Home '
                   '(usa su título, año, problema, arquitectura, resultado, métricas e imagen hero).',
    )
    destacado_home = models.BooleanField(
        'Destacado en Home',
        default=False,
        help_text='Se muestra en la sección "Proyectos destacados" del Home (máx. 3; si marcas más, se ordenan por año).',
    )

    imagen_card = models.ImageField(
        upload_to='proyectos/cards/',
        blank=True,
        null=True,
        help_text='Imagen de la tarjeta en el listado de Proyectos y en "Proyectos destacados" del Home. '
                   'Si se deja vacía, se muestra un recuadro gris de reemplazo.',
    )
    imagen_hero = models.ImageField(
        upload_to='proyectos/hero/',
        blank=True,
        null=True,
        help_text='Imagen grande en la parte superior del detalle. También aparece en "Caso ancla" del Home si este es el proyecto ancla.',
    )
    imagen_arquitectura = models.ImageField(
        upload_to='proyectos/arquitectura/',
        blank=True,
        null=True,
        help_text='Imagen o diagrama para la sección "Arquitectura" del detalle. Opcional.',
    )

    problema = models.TextField(
        blank=True,
        help_text='Sección "El problema" del detalle. Si se deja vacío, esa sección se oculta '
                   '(y también la de "Problema" en el Home si este es el proyecto ancla).',
    )
    solucion = models.TextField(
        blank=True,
        help_text='Sección "La solución" del detalle (junto con los pasos del enfoque, abajo). Si se deja vacío, se oculta.',
    )
    arquitectura_texto = models.TextField(
        'Arquitectura (texto)',
        blank=True,
        help_text='Sección "Arquitectura" del detalle. Si se deja vacío, esa sección se oculta '
                   '(y también la de "Arquitectura" en el Home si este es el proyecto ancla).',
    )

    stack = models.CharField(
        max_length=500,
        blank=True,
        help_text='Tecnologías separadas por coma, ej: Python, Kubernetes, MLflow. Aparecen como etiquetas en "Stack" del detalle.',
    )

    web_url = models.URLField(
        'URL de demo',
        blank=True,
        help_text='Si se llena: botón "Ver demo" en el detalle + ícono de globo en la tarjeta del listado.',
    )
    github_url = models.URLField(
        'URL de GitHub',
        blank=True,
        help_text='Si se llena: botón "Código" en el detalle + ícono de GitHub en la tarjeta del listado.',
    )
    notebook_url = models.URLField(
        'URL de notebook',
        blank=True,
        help_text='Si se llena: botón "Notebook" en el detalle + ícono de notebook en la tarjeta del listado.',
    )

    publicado = models.BooleanField(default=True, help_text='Desmárcalo para ocultar el proyecto de todo el sitio sin borrarlo.')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-anio', 'id']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:proyecto_detalle', args=[self.slug])

    @property
    def stack_list(self):
        return [s.strip() for s in self.stack.split(',') if s.strip()]

    @property
    def has_web(self):
        return bool(self.web_url)

    @property
    def has_github(self):
        return bool(self.github_url)

    @property
    def has_notebook(self):
        return bool(self.notebook_url)


class ProjectMetric(models.Model):
    project = models.ForeignKey(Project, related_name='metrics', on_delete=models.CASCADE)
    valor = models.CharField(
        max_length=40,
        help_text='Número o texto corto, ej: 99.9%, 2M+, Nivel 3.',
    )
    etiqueta = models.CharField(
        max_length=80,
        help_text='Descripción debajo del valor, ej: Uptime, Registros/día. Se muestra en la tarjeta del listado, '
                   'el panel de métricas del detalle, y en "Caso ancla" del Home si este es el proyecto ancla.',
    )
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden de aparición (menor primero).')

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f'{self.valor} — {self.etiqueta}'


class ProjectStep(models.Model):
    project = models.ForeignKey(Project, related_name='pasos', on_delete=models.CASCADE)
    texto = models.TextField(
        help_text='Un paso del "Enfoque", dentro de la sección "La solución" del detalle. '
                   'Se numera automáticamente (1, 2, 3…) según el orden.',
    )
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden de aparición (menor primero).')

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.texto[:60]


class ProjectResultado(models.Model):
    project = models.ForeignKey(Project, related_name='resultados', on_delete=models.CASCADE)
    valor = models.CharField(
        max_length=40,
        help_text='Número o texto corto, ej: −82%, 3.2M, $0.',
    )
    etiqueta = models.CharField(
        max_length=160,
        help_text='Descripción del resultado, ej: Tiempo de despliegue de un nuevo modelo. '
                   'Se muestra en la sección "Resultados e impacto" del detalle.',
    )
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden de aparición (menor primero).')

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f'{self.valor} — {self.etiqueta}'


class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(Project, related_name='galeria', on_delete=models.CASCADE)
    imagen = models.ImageField(
        upload_to='proyectos/galeria/',
        blank=True,
        null=True,
        help_text='Imagen para la sección "Galería" del detalle.',
    )
    placeholder = models.CharField(
        max_length=120,
        blank=True,
        help_text='Descripción de la imagen. Se usa como texto alternativo, y como recuadro de reemplazo si no subes imagen.',
    )
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden de aparición (menor primero).')

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.placeholder or f'Imagen {self.pk}'


class Post(models.Model):
    titulo = models.CharField(
        max_length=220,
        help_text='Título del artículo. Aparece en la tarjeta del listado y como encabezado del detalle.',
    )
    slug = models.SlugField(
        max_length=240,
        unique=True,
        blank=True,
        help_text='Se genera solo a partir del título si lo dejas vacío. Define la URL: /blog/este-texto/',
    )
    pilar = models.CharField(
        max_length=40,
        choices=PILAR_CHOICES,
        help_text='Categoría temática del artículo. Funciona como filtro en el listado del Blog y define el color de la etiqueta.',
    )

    extracto = models.TextField(help_text='Resumen corto (1-2 líneas) mostrado en la tarjeta del listado y en "Del blog" del Home.')
    contenido = models.TextField(
        help_text='Cuerpo completo del artículo en formato Markdown: usa "## Subtítulo" para encabezados, '
                   '"**texto**" para negrita, "> texto" para citas destacadas, y "- item" para listas.',
    )

    imagen_portada = models.ImageField(
        upload_to='blog/portadas/',
        blank=True,
        null=True,
        help_text='Imagen de portada: aparece en la tarjeta del listado, en "Del blog" del Home, y arriba del detalle. '
                   'Si se deja vacía, se muestra un recuadro gris de reemplazo.',
    )
    tags = models.CharField(
        max_length=300,
        blank=True,
        help_text='Temas separados por coma, ej: Arquitectura, Sistemas críticos. Se muestran al final del artículo.',
    )

    fecha_publicacion = models.DateField(help_text='Define el orden del listado (más reciente primero) y se muestra en la tarjeta y el detalle.')
    lectura_min = models.PositiveIntegerField('Minutos de lectura', default=5, help_text='Se muestra junto a la fecha, ej: "8 min".')

    publicado = models.BooleanField(default=True, help_text='Desmárcalo para ocultar el artículo de todo el sitio sin borrarlo.')
    destacado_home = models.BooleanField(
        'Destacado en Home',
        default=False,
        help_text='Se muestra en la sección "Del blog" del Home (máx. 3; si marcas más, se ordenan por fecha).',
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_publicacion', 'id']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)[:240]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:blog_detalle', args=[self.slug])

    @property
    def tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    @property
    def contenido_html(self):
        return mark_safe(markdown_lib.markdown(self.contenido, extensions=['extra']))


COLOR_CHOICES = [('primary', 'Primary (azul)'), ('secondary', 'Secondary (morado)')]


class HomeContent(models.Model):
    badge_texto = models.CharField(
        max_length=100,
        default='Tolerancia cero al error',
        help_text='Texto de la pastilla pequeña arriba del título del hero.',
    )
    titulo = models.CharField('Título del hero', max_length=300, help_text='Título grande (H1) en la parte superior del Home.')
    lead = models.TextField('Texto del hero', help_text='Párrafo debajo del título del hero.')
    cta_primario_texto = models.CharField(
        max_length=50,
        default='Ver caso INS',
        help_text='Texto del botón principal del hero. Ese mismo botón se repite abajo, en la sección "Caso ancla".',
    )
    cta_secundario_texto = models.CharField(
        max_length=50,
        default='Ver proyectos',
        help_text='Texto del botón secundario del hero (lleva siempre al listado de Proyectos).',
    )

    class Meta:
        verbose_name = 'Contenido de Home'
        verbose_name_plural = 'Contenido de Home'

    def __str__(self):
        return 'Contenido de Home'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class HomeStat(models.Model):
    home = models.ForeignKey(HomeContent, related_name='stats', on_delete=models.CASCADE)
    valor = models.FloatField(help_text='Número que se anima al cargar la página. Ej: 12, 20, 99.9.')
    sufijo = models.CharField(max_length=5, blank=True, help_text='Va pegado al número, ej: +, %. Déjalo vacío si no aplica.')
    etiqueta = models.CharField(max_length=100, help_text='Texto debajo del número, ej: Certificaciones, Sistemas críticos.')
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='primary',
        help_text='Color del número. Alterna primary/secondary entre estadísticas para dar contraste visual.',
    )
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden de aparición, de izquierda a derecha (menor primero).')

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Estadística'
        verbose_name_plural = 'Estadísticas del hero'

    def __str__(self):
        return f'{self.valor}{self.sufijo} — {self.etiqueta}'


class AboutContent(models.Model):
    badge_texto = models.CharField(
        max_length=100,
        default='Tolerancia cero al error',
        help_text='Texto de la pastilla pequeña junto a la foto, arriba del nombre.',
    )
    nombre = models.CharField(max_length=150, default='Carlos A. Jiménez Hirashi', help_text='Nombre completo, título grande del hero.')
    bio = models.TextField('Biografía corta (hero)', help_text='Párrafo debajo del nombre, en la parte superior de la página.')
    cta_primario_texto = models.CharField(
        max_length=50,
        default='Hablemos',
        help_text='Texto del botón principal del hero (lleva a Contacto).',
    )
    cta_secundario_texto = models.CharField(
        max_length=50,
        default='Ver proyectos',
        help_text='Texto del botón secundario del hero (lleva al listado de Proyectos).',
    )

    filosofia_titulo = models.CharField(
        max_length=200,
        default='Diseñar para que el error no exista',
        help_text='Título de la sección "01 · Filosofía".',
    )
    filosofia_cita = models.TextField('Cita (blockquote)', help_text='Texto grande en cursiva, destacado con una línea vertical.')
    filosofia_texto = models.TextField('Texto de filosofía', help_text='Párrafo largo debajo de la cita.')

    trayectoria_titulo = models.CharField(
        max_length=200,
        default='20+ años, dos disciplinas, un mismo estándar',
        help_text='Título de la sección "02 · Trayectoria" (arriba de la línea de tiempo).',
    )

    cta_final_titulo = models.CharField(
        max_length=200,
        default='¿Un sistema que no puede fallar?',
        help_text='Título de la tarjeta de contacto al final de la página.',
    )
    cta_final_texto = models.TextField(
        default='Hablemos de tu proyecto de datos, IA o automatización crítica.',
        help_text='Texto debajo del título, en la tarjeta de contacto final.',
    )
    cta_final_boton_texto = models.CharField(
        max_length=50,
        default='Ir a contacto',
        help_text='Texto del botón de esa tarjeta final (lleva a Contacto).',
    )

    class Meta:
        verbose_name = 'Contenido de Sobre Mí'
        verbose_name_plural = 'Contenido de Sobre Mí'

    def __str__(self):
        return 'Contenido de Sobre Mí'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class TimelineEntry(models.Model):
    about = models.ForeignKey(AboutContent, related_name='timeline', on_delete=models.CASCADE)
    periodo = models.CharField(max_length=50, help_text='Rango de años, ej: 2004 — 2013, o 2021 — presente.')
    rol = models.CharField(max_length=150, help_text='Puesto o rol durante ese periodo.')
    empresa = models.CharField(max_length=150, blank=True, help_text='Empresa u organización donde ocupaste ese rol.')
    responsabilidades = models.TextField(help_text='Qué hacías en ese puesto: funciones y responsabilidades principales.')
    logro = models.TextField(blank=True, help_text='Logros, resultados o momentos clave de esa etapa. Opcional — si está vacío no se muestra en la página.')
    caso_exito = models.TextField(blank=True, help_text='Caso de éxito concreto de esa etapa. Opcional — si está vacío no se muestra en la página.')
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden en la línea de tiempo (menor primero, de arriba a abajo).')

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Entrada de trayectoria'
        verbose_name_plural = 'Trayectoria (timeline)'

    def __str__(self):
        return f'{self.periodo} — {self.rol}'


class Certification(models.Model):
    about = models.ForeignKey(AboutContent, related_name='certs', on_delete=models.CASCADE)
    icono = models.CharField(
        max_length=50,
        help_text='Nombre exacto de un ícono de Lucide (ver lucide.dev/icons), ej: shield-check, network, cloud, brain-circuit.',
    )
    titulo = models.CharField(max_length=200, help_text='Nombre de la certificación.')
    entidad = models.CharField(max_length=150, help_text='Institución u organización que la emitió.')
    anio = models.CharField(max_length=10, help_text='Año en que se obtuvo, ej: 2021.')
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='primary',
        help_text='Color del ícono y su fondo. Alterna primary/secondary para dar variedad visual.',
    )
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden de aparición (menor primero).')

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Certificación'
        verbose_name_plural = 'Certificaciones'

    def __str__(self):
        return self.titulo


class SkillGroup(models.Model):
    about = models.ForeignKey(AboutContent, related_name='skill_groups', on_delete=models.CASCADE)
    categoria = models.CharField(max_length=150, help_text='Nombre del grupo, ej: Data & IA, Infraestructura.')
    items = models.CharField(
        max_length=500,
        help_text='Habilidades separadas por coma, ej: Python, PyTorch, MLOps. Cada una se muestra como una etiqueta.',
    )
    orden = models.PositiveIntegerField(default=0, help_text='Controla el orden de los grupos (menor primero, de arriba a abajo).')

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Grupo de habilidades'
        verbose_name_plural = 'Habilidades técnicas'

    def __str__(self):
        return self.categoria

    @property
    def items_list(self):
        return [s.strip() for s in self.items.split(',') if s.strip()]
