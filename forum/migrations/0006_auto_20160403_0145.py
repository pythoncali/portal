# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0005_auto_20160402_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioPregunta',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('comentario', models.TextField(blank=True, max_length=3000)),
                ('comentador', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Comentarios',
                'ordering': ('-creado_en',),
                'verbose_name': 'Comentario',
            },
        ),
        migrations.CreateModel(
            name='ComentarioRespuesta',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('comentario', models.TextField(blank=True, max_length=3000)),
                ('comentador', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Comentarios',
                'ordering': ('-creado_en',),
                'verbose_name': 'Comentario',
            },
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='comentador',
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='comentarios',
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='comentarios',
        ),
        migrations.DeleteModel(
            name='Comentario',
        ),
        migrations.AddField(
            model_name='comentariorespuesta',
            name='respuesta',
            field=models.ForeignKey(to='forum.Respuesta'),
        ),
        migrations.AddField(
            model_name='comentariopregunta',
            name='pregunta',
            field=models.ForeignKey(to='forum.Pregunta'),
        ),
    ]
