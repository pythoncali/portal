# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votos',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('voto', models.SmallIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Votos',
                'verbose_name': 'Voto',
            },
        ),
        migrations.AlterModelOptions(
            name='respuesta',
            options={'verbose_name_plural': 'Respuestas', 'ordering': ('-aceptada', 'creado_en'), 'verbose_name': 'Respuesta'},
        ),
        migrations.AddField(
            model_name='pregunta',
            name='tiene_respuesta',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag', blank=True, through='taggit.TaggedItem'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='descripcion', editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag', blank=True, through='taggit.TaggedItem'),
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='votos',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='votos',
            field=models.ManyToManyField(blank=True, to='forum.Votos'),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='votos',
            field=models.ManyToManyField(blank=True, to='forum.Votos'),
        ),
    ]
