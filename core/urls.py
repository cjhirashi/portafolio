from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('proyectos/<slug:slug>/', views.proyecto_detalle, name='proyecto_detalle'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detalle, name='blog_detalle'),
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    path('contacto/', views.contacto, name='contacto'),
]
