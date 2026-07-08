from django.contrib import admin

from .models import (
    AboutContent,
    Certification,
    HomeContent,
    HomeStat,
    Post,
    Project,
    ProjectGalleryImage,
    ProjectMetric,
    ProjectResultado,
    ProjectStep,
    SkillGroup,
    TimelineEntry,
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
    list_display = ['titulo', 'categoria', 'industria', 'anio', 'es_ancla', 'destacado_home', 'publicado']
    list_display_links = ['titulo']
    list_editable = ['destacado_home']
    list_filter = ['categoria', 'industria', 'publicado', 'es_ancla', 'destacado_home']
    search_fields = ['titulo', 'resumen']
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ProjectMetricInline, ProjectStepInline, ProjectResultadoInline, ProjectGalleryImageInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'pilar', 'fecha_publicacion', 'destacado_home', 'publicado']
    list_display_links = ['titulo']
    list_editable = ['destacado_home']
    list_filter = ['pilar', 'publicado', 'destacado_home']
    search_fields = ['titulo', 'extracto', 'contenido']
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'


class SingletonAdmin(admin.ModelAdmin):
    """Un solo registro editable: sin lista, sin permiso de agregar si ya existe."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            from django.shortcuts import redirect
            return redirect('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), obj.pk)
        return super().changelist_view(request, extra_context)


class HomeStatInline(admin.TabularInline):
    model = HomeStat
    extra = 1


@admin.register(HomeContent)
class HomeContentAdmin(SingletonAdmin):
    inlines = [HomeStatInline]


class TimelineEntryInline(admin.TabularInline):
    model = TimelineEntry
    extra = 1


class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1


class SkillGroupInline(admin.TabularInline):
    model = SkillGroup
    extra = 1


@admin.register(AboutContent)
class AboutContentAdmin(SingletonAdmin):
    inlines = [TimelineEntryInline, CertificationInline, SkillGroupInline]
