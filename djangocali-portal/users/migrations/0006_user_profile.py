# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_short_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.CharField(verbose_name='En que te desenvuelves', null=True, max_length=20, blank=True),
        ),
    ]
