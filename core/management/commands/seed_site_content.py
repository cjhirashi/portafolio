from django.core.management.base import BaseCommand

from core.models import (
    AboutContent,
    Certification,
    HomeCaseStat,
    HomeContent,
    HomeStat,
    SkillGroup,
    TimelineEntry,
)


class Command(BaseCommand):
    help = 'Carga el contenido actual de Home y Sobre Mí como datos editables (idempotente).'

    def handle(self, *args, **options):
        home, _ = HomeContent.objects.update_or_create(
            pk=1,
            defaults={
                'badge_texto': 'Tolerancia cero al error',
                'titulo': 'Diseño sistemas de datos que operan solos, incluso cuando fallar no es una opción.',
                'lead': '20+ años en automatización de sistemas críticos, hoy aplicado a Data Science e IA en producción.',
                'cta_primario_texto': 'Ver caso INS',
                'cta_secundario_texto': 'Ver proyectos',
                'caso_titulo': 'Caso ancla — Bioterio INS',
                'caso_anio': '2015',
                'caso_problema': 'Certificación nivel 2 exigida tras el fracaso de una consultora multinacional dos años antes.',
                'caso_arquitectura': 'Rediseño sistémico de controles ambientales y de contención, tolerancia cero al error.',
                'caso_resultado': 'Calificó para <b>nivel 3</b> — 100% de pruebas pasadas, cero degradación.',
            },
        )
        home.stats.all().delete()
        for orden, (valor, sufijo, etiqueta, color) in enumerate([
            (12, '', 'Certificaciones', 'primary'),
            (8, '', 'Sistemas críticos', 'secondary'),
            (20, '+', 'Años de experiencia', 'primary'),
            (99.9, '%', 'Disponibilidad', 'secondary'),
        ]):
            HomeStat.objects.create(home=home, valor=valor, sufijo=sufijo, etiqueta=etiqueta, color=color, orden=orden)

        home.case_stats.all().delete()
        for orden, (valor, etiqueta, color) in enumerate([
            ('487', 'Pruebas ejecutadas', 'primary'),
            ('3', 'Nivel de certificación', 'secondary'),
            ('0', 'Fallos post-certificación', 'primary'),
        ]):
            HomeCaseStat.objects.create(home=home, valor=valor, etiqueta=etiqueta, color=color, orden=orden)

        self.stdout.write(self.style.SUCCESS('HomeContent listo.'))

        about, _ = AboutContent.objects.update_or_create(
            pk=1,
            defaults={
                'badge_texto': 'Tolerancia cero al error',
                'nombre': 'Carlos A. Jiménez Hirashi',
                'bio': 'Arquitecto Senior de Sistemas de Datos. 20+ años diseñando sistemas críticos que no pueden fallar — hoy aplicado a Data Science e IA en producción.',
                'cta_primario_texto': 'Hablemos',
                'cta_secundario_texto': 'Ver proyectos',
                'filosofia_titulo': 'Diseñar para que el error no exista',
                'filosofia_cita': 'La mayoría de los sistemas se diseñan para recuperarse de un fallo. Yo los diseño para que ese fallo nunca pueda ocurrir en primer lugar.',
                'filosofia_texto': 'Cada interacción entre componentes se modela antes de escribir una línea de código, buscando específicamente los puntos donde variables interdependientes podrían converger en un fallo. Esa disciplina viene de dos décadas comisionando sistemas industriales donde un error no es un bug — es un incidente. Hoy aplico el mismo rigor a modelos de IA y pipelines de datos en producción.',
                'trayectoria_titulo': '20+ años, dos disciplinas, un mismo estándar',
                'cta_final_titulo': '¿Un sistema que no puede fallar?',
                'cta_final_texto': 'Hablemos de tu proyecto de datos, IA o automatización crítica.',
                'cta_final_boton_texto': 'Ir a contacto',
            },
        )

        about.timeline.all().delete()
        for orden, (periodo, rol, contexto, logro) in enumerate([
            ('2004 — 2013', 'Ingeniero de Sistemas de Control', 'Automatización industrial (HVAC)',
             'Comisionamiento de sistemas de control ambiental en más de 20 proyectos industriales, sin fallos post-arranque.'),
            ('2013 — 2018', 'Arquitecto de Sistemas Críticos', 'Infraestructura de bioseguridad',
             'Rediseño sistémico de controles ambientales y de contención para el Bioterio del Instituto Nacional de Salud — certificó nivel 3 con 100% de pruebas pasadas.'),
            ('2018 — 2021', 'Transición a Data Science e IA', 'Formación y primeros pilotos',
             'Aplicó el mismo método de tolerancia cero al diseño de pipelines de datos y modelos predictivos en producción.'),
            ('2021 — presente', 'Arquitecto Senior de Sistemas de Datos', 'Data Science, ML Ops y automatización',
             'Orquestación de modelos en tiempo real, pipelines de ingesta crítica y monitoreo autónomo para salud, fintech y logística.'),
        ]):
            TimelineEntry.objects.create(about=about, periodo=periodo, rol=rol, contexto=contexto, logro=logro, orden=orden)

        about.certs.all().delete()
        for orden, (icono, titulo, entidad, anio, color) in enumerate([
            ('shield-check', 'Certificación de Bioseguridad Nivel 3', 'Instituto Nacional de Salud', '2015', 'primary'),
            ('network', 'Arquitectura Empresarial (TOGAF)', 'The Open Group', '2019', 'secondary'),
            ('cloud', 'Arquitecto de Soluciones en la Nube', 'AWS', '2021', 'primary'),
            ('brain-circuit', 'Machine Learning en Producción', 'DeepLearning.AI', '2022', 'secondary'),
        ]):
            Certification.objects.create(about=about, icono=icono, titulo=titulo, entidad=entidad, anio=anio, color=color, orden=orden)

        about.skill_groups.all().delete()
        for orden, (categoria, items) in enumerate([
            ('Data & IA', 'Python, PyTorch, MLOps, Airflow, Feature Stores, LLMs'),
            ('Sistemas críticos & arquitectura', 'Control de procesos, Observabilidad, Diseño para fallo cero, SLA/SLO, Arquitectura de eventos'),
            ('Infraestructura', 'AWS, GCP, Docker, Kubernetes, Terraform, CI/CD'),
        ]):
            SkillGroup.objects.create(about=about, categoria=categoria, items=items, orden=orden)

        self.stdout.write(self.style.SUCCESS('AboutContent listo.'))
