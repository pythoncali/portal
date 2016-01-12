# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151111_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='short_bio',
            field=models.CharField(blank=True, null=True, max_length=60, verbose_name='Frase descriptiva'),
        ),
    ]
