from django.contrib import admin

from .models import (
    Post,
    Project,
    ProjectGalleryImage,
    ProjectMetric,
    ProjectResultado,
    ProjectStep,
)


class ProjectMetricInline(admin.TabularInline):
    model = ProjectMetric
    extra = 1


class ProjectStepInline(admin.TabularInline):
    model = ProjectStep
    extra = 1


class ProjectResultadoInline(admin.TabularInline):
    model = ProjectResultado
    extra = 1


class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'industria', 'anio', 'es_ancla', 'publicado']
    list_filter = ['categoria', 'industria', 'publicado', 'es_ancla']
    search_fields = ['titulo', 'resumen']
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ProjectMetricInline, ProjectStepInline, ProjectResultadoInline, ProjectGalleryImageInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'pilar', 'fecha_publicacion', 'publicado']
    list_filter = ['pilar', 'publicado']
    search_fields = ['titulo', 'extracto', 'contenido']
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
