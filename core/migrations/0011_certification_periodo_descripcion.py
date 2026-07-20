from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_timelineentry_caso_exito_logro_optional'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certification',
            old_name='anio',
            new_name='periodo',
        ),
        migrations.AlterField(
            model_name='certification',
            name='periodo',
            field=models.CharField(
                max_length=30,
                help_text='Año o rango, ej: 2021 o 2019 — presente.',
            ),
        ),
        migrations.AddField(
            model_name='certification',
            name='descripcion',
            field=models.TextField(
                blank=True,
                help_text='Descripción breve de la certificación o lo que acredita. Opcional — si está vacío no se muestra en la tarjeta.',
            ),
        ),
    ]
