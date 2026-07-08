from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Post

POST_TOLERANCIA_CERO_MD = """La mayoría de los sistemas se diseñan para recuperarse de fallos. Un sistema con tolerancia cero al error se diseña para que ciertas clases de fallo nunca puedan ocurrir en primer lugar. La diferencia no es de grado, es de método.

## El error como variable de diseño, no como excepción

Cuando el error se trata como una eventualidad a manejar después del hecho, el sistema hereda toda la fragilidad de lo no anticipado. El pensamiento sistémico invierte esa lógica: cada interacción entre componentes se modela antes de escribir una línea de código, buscando específicamente los puntos donde decenas de variables interdependientes podrían converger en un fallo.

## Certificación como prueba, no como formalidad

En el caso del Bioterio del Instituto Nacional de Salud, la certificación de bioseguridad no fue el objetivo final sino el mecanismo de verificación de que el diseño era correcto. El sistema no solo aprobó el **100% de las pruebas** de nivel 2 — calificó para nivel 3, un estándar que no se le exigía. Esa holgura es la métrica real de un diseño sin puntos ciegos.

## De la corrección reactiva a la prevención estructural

Un arquitecto que corrige después del incidente optimiza el tiempo de respuesta. Un arquitecto que diseña con tolerancia cero optimiza para que el incidente sea estructuralmente imposible dentro del dominio operativo del sistema. Esto exige modelar explícitamente los límites del sistema, no solo su comportamiento esperado.

> Entro cuando el error no es una opción — el diseño correcto elimina la posibilidad, no reduce la probabilidad.

Este mismo método — anticipar interacciones antes de que fallen — es el que aplico hoy al llevar modelos de Data Science e IA a producción bajo la misma disciplina de sistema crítico."""

POSTS = [
    {
        'titulo': 'Tolerancia cero: diseñando para que el error no exista',
        'pilar': 'Arquitectura',
        'extracto': 'Un método explícito para eliminar clases enteras de fallos antes de que el sistema entre en producción, no después.',
        'contenido': POST_TOLERANCIA_CERO_MD,
        'tags': 'Arquitectura, Sistemas críticos, Tolerancia cero, Certificación',
        'fecha_publicacion': '2026-05-14',
        'lectura_min': 8,
    },
    {
        'titulo': 'Llevar un modelo a producción con disciplina de sistema crítico',
        'pilar': 'Data Science e IA',
        'extracto': 'Por qué el 90% de los modelos que "funcionan en el notebook" fallan en producción, y cómo evitarlo con ingeniería rigurosa.',
        'fecha_publicacion': '2026-04-02',
        'lectura_min': 11,
    },
    {
        'titulo': 'Cómo modelar mentalmente un sistema de 40 variables interdependientes',
        'pilar': 'Pensamiento Sistémico',
        'extracto': 'El método que uso para anticipar interacciones antes de que ocurran, en vez de depurarlas después del incidente.',
        'fecha_publicacion': '2026-02-20',
        'lectura_min': 9,
    },
    {
        'titulo': 'Rollback automático: el patrón que evita que un despliegue se convierta en incidente',
        'pilar': 'Arquitectura',
        'extracto': 'Arquitectura de despliegue canario con reversión automática basada en umbrales de SLA, aplicada a sistemas de misión crítica.',
        'fecha_publicacion': '2025-12-11',
        'lectura_min': 7,
    },
    {
        'titulo': 'Drift de datos: la falla silenciosa que nadie monitorea',
        'pilar': 'Data Science e IA',
        'extracto': 'Cómo detectar degradación de modelos antes de que impacte al negocio, con observabilidad continua de principio a fin.',
        'fecha_publicacion': '2025-10-30',
        'lectura_min': 10,
    },
    {
        'titulo': 'Anticipar en vez de corregir: el costo real de reaccionar tarde',
        'pilar': 'Pensamiento Sistémico',
        'extracto': 'La diferencia entre un arquitecto que apaga incendios y uno que diseña sistemas donde el incendio no puede iniciar.',
        'fecha_publicacion': '2025-09-05',
        'lectura_min': 6,
    },
]


class Command(BaseCommand):
    help = 'Carga los artículos de blog de muestra del handoff de diseño (idempotente).'

    def handle(self, *args, **options):
        for data in POSTS:
            slug = slugify(data['titulo'])[:240]
            post, created = Post.objects.update_or_create(
                slug=slug,
                defaults={
                    'titulo': data['titulo'],
                    'pilar': data['pilar'],
                    'extracto': data['extracto'],
                    'contenido': data.get('contenido', data['extracto']),
                    'tags': data.get('tags', ''),
                    'fecha_publicacion': data['fecha_publicacion'],
                    'lectura_min': data['lectura_min'],
                },
            )
            self.stdout.write(self.style.SUCCESS(f'{"Creado" if created else "Actualizado"}: {post.titulo}'))
