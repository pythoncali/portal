# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_auto_20160313_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respuesta',
            name='slug',
        ),
        migrations.AddField(
            model_name='votos',
            name='votante',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
