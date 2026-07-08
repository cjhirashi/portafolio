from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_timelineentry_empresa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timelineentry',
            old_name='contexto',
            new_name='responsabilidades',
        ),
        migrations.AlterField(
            model_name='timelineentry',
            name='responsabilidades',
            field=models.TextField(help_text='Qué hacías en ese puesto: funciones y responsabilidades principales.'),
        ),
        migrations.AlterField(
            model_name='timelineentry',
            name='logro',
            field=models.TextField(help_text='Logros, resultados o momentos clave de esa etapa.'),
        ),
    ]
