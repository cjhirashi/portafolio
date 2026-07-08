from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Project, ProjectGalleryImage, ProjectMetric, ProjectResultado, ProjectStep

PROJECTS = [
    {
        'titulo': 'Bioterio INS — Certificación nivel 3',
        'categoria': 'Systems', 'industria': 'Salud', 'anio': 2015,
        'resultado': 'Rediseño sistémico de controles ambientales y de contención. Calificó para nivel 3 con 100% de pruebas pasadas.',
        'es_ancla': True,
        'problema': 'Certificación nivel 2 exigida tras el fracaso de una consultora multinacional dos años antes.',
        'arquitectura_texto': 'Rediseño sistémico de controles ambientales y de contención, tolerancia cero al error.',
        'metrics': [('487', 'Pruebas'), ('Nivel 3', 'Certificación'), ('0', 'Fallos')],
        'links': {},
    },
    {
        'titulo': 'Pipeline ETL crítico',
        'categoria': 'Data', 'industria': 'Healthcare', 'anio': 2021,
        'resultado': 'Automatización de ingesta de datos clínicos con tolerancia cero al error.',
        'metrics': [('99.9%', 'Uptime'), ('2M+', 'Registros/día')],
        'links': {'github_url': 'https://github.com/', 'notebook_url': 'https://colab.research.google.com/'},
    },
    {
        'titulo': 'Orquestación de modelos: predicción de fraude en tiempo real',
        'categoria': 'ML Ops', 'industria': 'Fintech', 'anio': 2023,
        'resultado': 'Predicción de fraude en tiempo real con SLA garantizado.',
        'metrics': [('120ms', 'Latencia p99'), ('99.95%', 'SLA cumplido'), ('40+', 'Modelos en producción')],
        'links': {'web_url': 'https://example.com/', 'github_url': 'https://github.com/'},
        'resumen': 'Un sistema de MLOps que despliega, versiona y monitorea modelos de detección de fraude en producción, garantizando latencia y disponibilidad bajo SLA estricto.',
        'problema': 'El equipo de riesgo operaba con modelos de fraude actualizados manualmente, sin control de versiones ni monitoreo de degradación. Cada despliegue tomaba días y un error en producción podía pasar desapercibido durante horas, exponiendo a la fintech a pérdidas directas y regulatorias.',
        'solucion': 'Diseñé una plataforma de orquestación que estandariza el ciclo de vida completo de los modelos: entrenamiento, validación, despliegue canario y rollback automático, con observabilidad de drift y latencia en cada etapa.',
        'arquitectura_texto': 'La plataforma corre sobre un clúster de inferencia con balanceo de carga, un registro de modelos versionado y un bus de eventos que conecta el scoring en tiempo real con el sistema de alertas y el dashboard de riesgo.',
        'stack': 'Python, Kubernetes, MLflow, Kafka, Redis, FastAPI, Prometheus, Terraform',
        'pasos': [
            'Pipeline de CI/CD para modelos con validación automática contra un conjunto de datos de referencia antes de cada despliegue.',
            'Despliegue canario con enrutamiento gradual de tráfico y rollback automático si la latencia o el error rate superan el umbral del SLA.',
            'Monitoreo continuo de drift de datos y degradación de precisión, con alertas al equipo de riesgo antes de que impacte al negocio.',
        ],
        'resultados': [
            ('−82%', 'Tiempo de despliegue de un nuevo modelo'),
            ('3.2M', 'Transacciones evaluadas por día'),
            ('$0', 'Incidentes de fraude no detectados desde el lanzamiento'),
        ],
        'galeria': ['Dashboard de monitoreo', 'Panel de despliegue canario', 'Alertas de drift'],
    },
    {
        'titulo': 'Monitoreo autónomo',
        'categoria': 'Systems', 'industria': 'Logística', 'anio': 2024,
        'resultado': 'Sistema de alertas que opera sin intervención humana.',
        'metrics': [],
        'links': {'web_url': 'https://example.com/'},
    },
    {
        'titulo': 'Forecasting de demanda multi-tienda',
        'categoria': 'Data', 'industria': 'Retail', 'anio': 2022,
        'resultado': 'Modelo de predicción de demanda con reentrenamiento automático, reduciendo quiebres de inventario.',
        'metrics': [('-31%', 'Quiebres de stock'), ('150+', 'Tiendas')],
        'links': {'github_url': 'https://github.com/', 'notebook_url': 'https://colab.research.google.com/'},
    },
    {
        'titulo': 'Integración HVAC a gran escala',
        'categoria': 'Systems', 'industria': 'Industrial', 'anio': 2011,
        'resultado': 'Comisionamiento de sistemas de control ambiental en más de 20 proyectos sin fallos post-arranque.',
        'metrics': [('20+', 'Proyectos'), ('100%', 'Sin fallos')],
        'links': {},
    },
]


class Command(BaseCommand):
    help = 'Carga los proyectos de muestra del handoff de diseño (idempotente).'

    def handle(self, *args, **options):
        for data in PROJECTS:
            slug = slugify(data['titulo'])[:220]
            project, created = Project.objects.update_or_create(
                slug=slug,
                defaults={
                    'titulo': data['titulo'],
                    'categoria': data['categoria'],
                    'industria': data['industria'],
                    'anio': data['anio'],
                    'resultado': data['resultado'],
                    'resumen': data.get('resumen', data['resultado']),
                    'es_ancla': data.get('es_ancla', False),
                    'problema': data.get('problema', ''),
                    'solucion': data.get('solucion', ''),
                    'arquitectura_texto': data.get('arquitectura_texto', ''),
                    'stack': data.get('stack', ''),
                    'web_url': data['links'].get('web_url', ''),
                    'github_url': data['links'].get('github_url', ''),
                    'notebook_url': data['links'].get('notebook_url', ''),
                },
            )

            project.metrics.all().delete()
            for orden, (valor, etiqueta) in enumerate(data.get('metrics', [])):
                ProjectMetric.objects.create(project=project, valor=valor, etiqueta=etiqueta, orden=orden)

            project.pasos.all().delete()
            for orden, texto in enumerate(data.get('pasos', [])):
                ProjectStep.objects.create(project=project, texto=texto, orden=orden)

            project.resultados.all().delete()
            for orden, (valor, etiqueta) in enumerate(data.get('resultados', [])):
                ProjectResultado.objects.create(project=project, valor=valor, etiqueta=etiqueta, orden=orden)

            project.galeria.all().delete()
            for orden, placeholder in enumerate(data.get('galeria', [])):
                ProjectGalleryImage.objects.create(project=project, placeholder=placeholder, orden=orden)

            self.stdout.write(self.style.SUCCESS(f'{"Creado" if created else "Actualizado"}: {project.titulo}'))
