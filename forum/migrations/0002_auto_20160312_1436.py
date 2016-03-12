# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('voto', models.SmallIntegerField()),
                ('votante', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Voto',
                'verbose_name_plural': 'Votos',
            },
        ),
        migrations.AlterModelOptions(
            name='respuesta',
            options={'ordering': ('-aceptada', 'creado_en'), 'verbose_name': 'Respuesta', 'verbose_name_plural': 'Respuestas'},
        ),
        migrations.AddField(
            model_name='pregunta',
            name='tiene_respuesta',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', to='taggit.Tag', through='taggit.TaggedItem', blank=True, verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='descripcion', unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', to='taggit.Tag', through='taggit.TaggedItem', blank=True, verbose_name='Tags'),
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='votos',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='votos',
            field=models.ManyToManyField(to='forum.Votos', blank=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='votos',
            field=models.ManyToManyField(to='forum.Votos', blank=True),
        ),
    ]
