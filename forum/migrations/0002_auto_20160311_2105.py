# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('voto', models.SmallIntegerField()),
                ('votante', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='respuesta',
            options={'verbose_name': 'Respuesta', 'verbose_name_plural': 'Respuestas', 'ordering': ('-aceptada', 'creado_en')},
        ),
        migrations.AddField(
            model_name='pregunta',
            name='tiene_respuesta',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='votos',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='votos',
            field=models.ManyToManyField(to='forum.Votos'),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='votos',
            field=models.ManyToManyField(to='forum.Votos'),
        ),
    ]
