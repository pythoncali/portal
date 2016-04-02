# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20160402_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='comentarios',
            field=models.ManyToManyField(to='forum.Comentario', blank=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='comentarios',
            field=models.ManyToManyField(to='forum.Comentario', blank=True),
        ),
    ]
