# Generated by Django 2.1.2 on 2018-11-08 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0002_students_tfgs'),
        ('tfms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='tfms',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tfms.Tfms'),
        ),
    ]
