# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150905_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, null=True, verbose_name='Descripción corta', max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='github_account',
            field=models.URLField(blank=True, null=True, verbose_name='Cuenta de Twitter', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_account',
            field=models.URLField(blank=True, null=True, verbose_name='Cuenta de Twitter', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/%Y-%m-%d/', verbose_name='Avatar'),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter_account',
            field=models.URLField(blank=True, null=True, verbose_name='Cuenta de Twitter', max_length=255),
        ),
    ]
