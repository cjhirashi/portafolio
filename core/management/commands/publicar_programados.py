from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Post


class Command(BaseCommand):
    help = 'Publica los posts cuya fecha_programada ya llegó.'

    def handle(self, *args, **options):
        ahora = timezone.now()
        pendientes = Post.objects.filter(
            publicado=False,
            fecha_programada__isnull=False,
            fecha_programada__lte=ahora,
        )
        count = pendientes.count()
        pendientes.update(publicado=True)
        self.stdout.write(self.style.SUCCESS(f'{count} post(s) publicado(s).'))
