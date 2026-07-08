from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ContactoForm
from .models import PILARES, Post, Project

HOME_STATS = [
    {'value': 12, 'suffix': '', 'label': 'Certificaciones', 'color': 'primary'},
    {'value': 8, 'suffix': '', 'label': 'Sistemas críticos', 'color': 'secondary'},
    {'value': 20, 'suffix': '+', 'label': 'Años de experiencia', 'color': 'primary'},
    {'value': 99.9, 'suffix': '%', 'label': 'Disponibilidad', 'color': 'secondary'},
]

HOME_CASE_STATS = [
    {'value': '487', 'label': 'Pruebas ejecutadas', 'color': 'primary'},
    {'value': '3', 'label': 'Nivel de certificación', 'color': 'secondary'},
    {'value': '0', 'label': 'Fallos post-certificación', 'color': 'primary'},
]

def home(request):
    context = {
        'stats': HOME_STATS,
        'case_stats': HOME_CASE_STATS,
        'projects': Project.objects.filter(publicado=True).order_by('-es_ancla', '-anio', 'id')[:3],
        'blog_posts': Post.objects.filter(publicado=True).order_by('-fecha_publicacion', 'id')[:3],
    }
    return render(request, 'core/home.html', context)


def proyectos(request):
    q = request.GET.get('q', '').strip()
    filtro = request.GET.get('filtro', 'Todos')
    orden = request.GET.get('orden', 'recientes')

    publicados = Project.objects.filter(publicado=True)

    tags = []
    for project in publicados.order_by('id'):
        if project.categoria not in tags:
            tags.append(project.categoria)
    for project in publicados.order_by('id'):
        if project.industria not in tags:
            tags.append(project.industria)

    filters = [{'label': 'Todos', 'activo': filtro == 'Todos'}]
    filters += [{'label': tag, 'activo': filtro == tag} for tag in tags]

    proyectos_qs = publicados.prefetch_related('metrics')
    if filtro != 'Todos':
        proyectos_qs = proyectos_qs.filter(Q(categoria=filtro) | Q(industria=filtro))
    if q:
        proyectos_qs = proyectos_qs.filter(titulo__icontains=q)
    proyectos_qs = proyectos_qs.order_by('anio', 'id') if orden == 'antiguos' else proyectos_qs.order_by('-anio', 'id')

    context = {
        'filters': filters,
        'proyectos': proyectos_qs,
        'q': q,
        'filtro': filtro,
        'orden': orden,
        'orden_siguiente': 'recientes' if orden == 'antiguos' else 'antiguos',
        'orden_label': 'Más antiguos' if orden == 'antiguos' else 'Más recientes',
    }
    return render(request, 'core/proyectos.html', context)


def proyecto_detalle(request, slug):
    project = get_object_or_404(Project, slug=slug, publicado=True)

    ids = list(Project.objects.filter(publicado=True).order_by('-anio', 'id').values_list('pk', flat=True))
    next_project = project
    if len(ids) > 1:
        idx = ids.index(project.pk)
        next_project = Project.objects.get(pk=ids[(idx + 1) % len(ids)])

    return render(request, 'core/proyecto_detalle.html', {'project': project, 'next_project': next_project})


def blog(request):
    q = request.GET.get('q', '').strip()
    pilar = request.GET.get('pilar', 'Todos')
    orden = request.GET.get('orden', 'recientes')

    filters = [{'label': 'Todos', 'activo': pilar == 'Todos'}]
    filters += [{'label': p, 'activo': pilar == p} for p in PILARES]

    posts_qs = Post.objects.filter(publicado=True)
    if pilar != 'Todos':
        posts_qs = posts_qs.filter(pilar=pilar)
    if q:
        posts_qs = posts_qs.filter(titulo__icontains=q)
    posts_qs = posts_qs.order_by('fecha_publicacion', 'id') if orden == 'antiguos' else posts_qs.order_by('-fecha_publicacion', 'id')

    context = {
        'filters': filters,
        'posts': posts_qs,
        'q': q,
        'pilar': pilar,
        'orden': orden,
        'orden_siguiente': 'recientes' if orden == 'antiguos' else 'antiguos',
        'orden_label': 'Más antiguos' if orden == 'antiguos' else 'Más recientes',
    }
    return render(request, 'core/blog.html', context)


def blog_detalle(request, slug):
    post = get_object_or_404(Post, slug=slug, publicado=True)

    ids = list(Post.objects.filter(publicado=True).order_by('-fecha_publicacion', 'id').values_list('pk', flat=True))
    next_post = post
    if len(ids) > 1:
        idx = ids.index(post.pk)
        next_post = Post.objects.get(pk=ids[(idx + 1) % len(ids)])

    return render(request, 'core/blog_detalle.html', {'post': post, 'next_post': next_post})


SOBRE_MI_TIMELINE = [
    {
        'periodo': '2004 — 2013',
        'rol': 'Ingeniero de Sistemas de Control',
        'contexto': 'Automatización industrial (HVAC)',
        'logro': 'Comisionamiento de sistemas de control ambiental en más de 20 proyectos industriales, sin fallos post-arranque.',
    },
    {
        'periodo': '2013 — 2018',
        'rol': 'Arquitecto de Sistemas Críticos',
        'contexto': 'Infraestructura de bioseguridad',
        'logro': 'Rediseño sistémico de controles ambientales y de contención para el Bioterio del Instituto Nacional de Salud — certificó nivel 3 con 100% de pruebas pasadas.',
    },
    {
        'periodo': '2018 — 2021',
        'rol': 'Transición a Data Science e IA',
        'contexto': 'Formación y primeros pilotos',
        'logro': 'Aplicó el mismo método de tolerancia cero al diseño de pipelines de datos y modelos predictivos en producción.',
    },
    {
        'periodo': '2021 — presente',
        'rol': 'Arquitecto Senior de Sistemas de Datos',
        'contexto': 'Data Science, ML Ops y automatización',
        'logro': 'Orquestación de modelos en tiempo real, pipelines de ingesta crítica y monitoreo autónomo para salud, fintech y logística.',
    },
]

SOBRE_MI_CERTS = [
    {'icon': 'shield-check', 'titulo': 'Certificación de Bioseguridad Nivel 3', 'entidad': 'Instituto Nacional de Salud', 'anio': '2015', 'color': 'primary'},
    {'icon': 'network', 'titulo': 'Arquitectura Empresarial (TOGAF)', 'entidad': 'The Open Group', 'anio': '2019', 'color': 'secondary'},
    {'icon': 'cloud', 'titulo': 'Arquitecto de Soluciones en la Nube', 'entidad': 'AWS', 'anio': '2021', 'color': 'primary'},
    {'icon': 'brain-circuit', 'titulo': 'Machine Learning en Producción', 'entidad': 'DeepLearning.AI', 'anio': '2022', 'color': 'secondary'},
]

SOBRE_MI_SKILL_GROUPS = [
    {'categoria': 'Data & IA', 'items': ['Python', 'PyTorch', 'MLOps', 'Airflow', 'Feature Stores', 'LLMs']},
    {'categoria': 'Sistemas críticos & arquitectura', 'items': ['Control de procesos', 'Observabilidad', 'Diseño para fallo cero', 'SLA/SLO', 'Arquitectura de eventos']},
    {'categoria': 'Infraestructura', 'items': ['AWS', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'CI/CD']},
]


def sobre_mi(request):
    context = {
        'timeline': SOBRE_MI_TIMELINE,
        'certs': SOBRE_MI_CERTS,
        'skill_groups': SOBRE_MI_SKILL_GROUPS,
    }
    return render(request, 'core/sobre_mi.html', context)


def contacto(request):
    enviado = request.GET.get('enviado') == '1'
    form = ContactoForm()

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            try:
                EmailMessage(
                    subject=f'Contacto desde el portafolio — {nombre}',
                    body=f'{mensaje}\n\n— {nombre} ({email})',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECIPIENT_EMAIL],
                    reply_to=[email],
                ).send(fail_silently=False)
            except SMTPException:
                messages.error(
                    request,
                    'No se pudo enviar tu mensaje. Intenta de nuevo en unos minutos.',
                )
            else:
                return redirect(f"{reverse('core:contacto')}?enviado=1")

    return render(request, 'core/contacto.html', {'form': form, 'enviado': enviado})
