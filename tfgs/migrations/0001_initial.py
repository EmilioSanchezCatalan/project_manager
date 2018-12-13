# Generated by Django 2.1.2 on 2018-12-10 17:14

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('announcements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tfgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'General'), (1, 'Específico')], verbose_name='Tipo de proyecto')),
                ('mode', models.PositiveSmallIntegerField(choices=[(2, 'Trabajo teórico/experimental'), (0, 'Proyecto de Ingeniería'), (1, 'Estudio técnico')], verbose_name='Modalidad')),
                ('is_team', models.BooleanField(verbose_name='¿Es un trabajo en equipo?')),
                ('team_memory', models.FileField(blank=True, null=True, upload_to='is_team', verbose_name='Memoria justificativa')),
                ('objectives', ckeditor.fields.RichTextField(verbose_name='Objetivos')),
                ('methodology', ckeditor.fields.RichTextField(verbose_name='Metodología')),
                ('docs_and_forms', ckeditor.fields.RichTextField(verbose_name='Documentos y formatos de entrega')),
                ('departament_validation', models.BooleanField(null=True, verbose_name='Validación del departamento')),
                ('center_validation', models.BooleanField(null=True, verbose_name='Validación del centro')),
                ('draft', models.BooleanField(verbose_name='Borrador')),
                ('date_assignment', models.DateTimeField(null=True, verbose_name='Fecha de asignación')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('announcements', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='announcements.AnnouncementsTfg', verbose_name='Convocatoria')),
                ('carrers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tfgs', to='core.Carrers', verbose_name='Titulación')),
                ('itineraries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Itineraries', verbose_name='Itinerario')),
                ('mentions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Mentions', verbose_name='Mencion')),
                ('skills', models.ManyToManyField(to='core.Skills', verbose_name='Competencias que desarrolla')),
                ('tutor1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor1', to=settings.AUTH_USER_MODEL, verbose_name='Tutor principal')),
                ('tutor2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Tutor2', verbose_name='Tutor de apoyo')),
            ],
            options={
                'verbose_name': 'Trabajo final de grado',
                'verbose_name_plural': 'Trabajos finales de grado',
                'ordering': ['-createdAt'],
            },
        ),
    ]
