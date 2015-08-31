# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(max_length=3000)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, populate_from='titulo', editable=False)),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag')),
            ],
            options={
                'ordering': ('-creado_en',),
                'verbose_name': 'Pregunta',
                'verbose_name_plural': 'Preguntas',
            },
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('descripcion', models.TextField(max_length=2000)),
                ('votos', models.IntegerField(default=0)),
                ('aceptada', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, populate_from='titulo', editable=False)),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('pregunta', models.ForeignKey(to='forum.Pregunta')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag')),
            ],
            options={
                'ordering': ('-aceptada', '-votos', 'creado_en'),
                'verbose_name': 'Respuesta',
                'verbose_name_plural': 'Respuestas',
            },
        ),
    ]
