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
