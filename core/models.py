import markdown as markdown_lib
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

PILARES = ['Arquitectura', 'Data Science e IA', 'Pensamiento Sistémico']
PILAR_CHOICES = [(p, p) for p in PILARES]


class Project(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categoria = models.CharField(max_length=60)
    industria = models.CharField(max_length=60)
    anio = models.PositiveIntegerField()

    resultado = models.CharField(
        max_length=300,
        help_text='Resumen corto mostrado en las tarjetas de listado.',
    )
    resumen = models.TextField(help_text='Resumen largo mostrado en el detalle.')

    es_ancla = models.BooleanField('Proyecto ancla', default=False)

    imagen_card = models.ImageField(upload_to='proyectos/cards/', blank=True, null=True)
    imagen_hero = models.ImageField(upload_to='proyectos/hero/', blank=True, null=True)
    imagen_arquitectura = models.ImageField(upload_to='proyectos/arquitectura/', blank=True, null=True)

    problema = models.TextField(blank=True)
    solucion = models.TextField(blank=True)
    arquitectura_texto = models.TextField(blank=True)

    stack = models.CharField(max_length=500, blank=True, help_text='Tecnologías separadas por coma.')

    web_url = models.URLField('URL de demo', blank=True)
    github_url = models.URLField('URL de GitHub', blank=True)
    notebook_url = models.URLField('URL de notebook', blank=True)

    publicado = models.BooleanField(default=True)
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
    valor = models.CharField(max_length=40)
    etiqueta = models.CharField(max_length=80)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f'{self.valor} — {self.etiqueta}'


class ProjectStep(models.Model):
    project = models.ForeignKey(Project, related_name='pasos', on_delete=models.CASCADE)
    texto = models.TextField()
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.texto[:60]


class ProjectResultado(models.Model):
    project = models.ForeignKey(Project, related_name='resultados', on_delete=models.CASCADE)
    valor = models.CharField(max_length=40)
    etiqueta = models.CharField(max_length=160)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f'{self.valor} — {self.etiqueta}'


class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(Project, related_name='galeria', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='proyectos/galeria/', blank=True, null=True)
    placeholder = models.CharField(max_length=120, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.placeholder or f'Imagen {self.pk}'


class Post(models.Model):
    titulo = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    pilar = models.CharField(max_length=40, choices=PILAR_CHOICES)

    extracto = models.TextField(help_text='Resumen corto mostrado en las tarjetas de listado.')
    contenido = models.TextField(help_text='Cuerpo del artículo en formato Markdown.')

    imagen_portada = models.ImageField(upload_to='blog/portadas/', blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, help_text='Temas separados por coma.')

    fecha_publicacion = models.DateField()
    lectura_min = models.PositiveIntegerField('Minutos de lectura', default=5)

    publicado = models.BooleanField(default=True)
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


COLOR_CHOICES = [('primary', 'Primary'), ('secondary', 'Secondary')]


class HomeContent(models.Model):
    badge_texto = models.CharField(max_length=100, default='Tolerancia cero al error')
    titulo = models.CharField('Título del hero', max_length=300)
    lead = models.TextField('Texto del hero')
    cta_primario_texto = models.CharField(max_length=50, default='Ver caso INS')
    cta_secundario_texto = models.CharField(max_length=50, default='Ver proyectos')

    caso_titulo = models.CharField('Título del caso de estudio', max_length=200, default='Caso ancla — Bioterio INS')
    caso_anio = models.CharField(max_length=10, default='2015')
    caso_problema = models.TextField('Problema')
    caso_arquitectura = models.TextField('Arquitectura')
    caso_resultado = models.TextField(
        'Resultado',
        help_text='Se permite HTML simple, ej. <b>negrita</b>.',
    )

    class Meta:
        verbose_name = 'Contenido de Home'
        verbose_name_plural = 'Contenido de Home'

    def __str__(self):
        return 'Contenido de Home'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @property
    def caso_resultado_html(self):
        return mark_safe(self.caso_resultado)


class HomeStat(models.Model):
    home = models.ForeignKey(HomeContent, related_name='stats', on_delete=models.CASCADE)
    valor = models.FloatField(help_text='Ej: 12, 20, 99.9')
    sufijo = models.CharField(max_length=5, blank=True, help_text='Ej: +, %')
    etiqueta = models.CharField(max_length=100)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='primary')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Estadística'
        verbose_name_plural = 'Estadísticas del hero'

    def __str__(self):
        return f'{self.valor}{self.sufijo} — {self.etiqueta}'


class HomeCaseStat(models.Model):
    home = models.ForeignKey(HomeContent, related_name='case_stats', on_delete=models.CASCADE)
    valor = models.CharField(max_length=20)
    etiqueta = models.CharField(max_length=100)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='primary')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Estadística del caso'
        verbose_name_plural = 'Estadísticas del caso de estudio'

    def __str__(self):
        return f'{self.valor} — {self.etiqueta}'


class AboutContent(models.Model):
    badge_texto = models.CharField(max_length=100, default='Tolerancia cero al error')
    nombre = models.CharField(max_length=150, default='Carlos A. Jiménez Hirashi')
    bio = models.TextField('Biografía corta (hero)')
    cta_primario_texto = models.CharField(max_length=50, default='Hablemos')
    cta_secundario_texto = models.CharField(max_length=50, default='Ver proyectos')

    filosofia_titulo = models.CharField(max_length=200, default='Diseñar para que el error no exista')
    filosofia_cita = models.TextField('Cita (blockquote)')
    filosofia_texto = models.TextField('Texto de filosofía')

    trayectoria_titulo = models.CharField(max_length=200, default='20+ años, dos disciplinas, un mismo estándar')

    cta_final_titulo = models.CharField(max_length=200, default='¿Un sistema que no puede fallar?')
    cta_final_texto = models.TextField(default='Hablemos de tu proyecto de datos, IA o automatización crítica.')
    cta_final_boton_texto = models.CharField(max_length=50, default='Ir a contacto')

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
    periodo = models.CharField(max_length=50)
    rol = models.CharField(max_length=150)
    contexto = models.CharField(max_length=150)
    logro = models.TextField()
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Entrada de trayectoria'
        verbose_name_plural = 'Trayectoria (timeline)'

    def __str__(self):
        return f'{self.periodo} — {self.rol}'


class Certification(models.Model):
    about = models.ForeignKey(AboutContent, related_name='certs', on_delete=models.CASCADE)
    icono = models.CharField(max_length=50, help_text='Nombre de ícono Lucide, ej: shield-check')
    titulo = models.CharField(max_length=200)
    entidad = models.CharField(max_length=150)
    anio = models.CharField(max_length=10)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='primary')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Certificación'
        verbose_name_plural = 'Certificaciones'

    def __str__(self):
        return self.titulo


class SkillGroup(models.Model):
    about = models.ForeignKey(AboutContent, related_name='skill_groups', on_delete=models.CASCADE)
    categoria = models.CharField(max_length=150)
    items = models.CharField(max_length=500, help_text='Habilidades separadas por coma.')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Grupo de habilidades'
        verbose_name_plural = 'Habilidades técnicas'

    def __str__(self):
        return self.categoria

    @property
    def items_list(self):
        return [s.strip() for s in self.items.split(',') if s.strip()]
