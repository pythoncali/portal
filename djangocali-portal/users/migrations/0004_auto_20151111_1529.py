# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150928_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blog_account',
            field=models.URLField(verbose_name='Direccion del blog', null=True, blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='facebook_account',
            field=models.URLField(verbose_name='Cuenta de Facebook', null=True, blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='google_plus_account',
            field=models.URLField(verbose_name='Cuenta de Google+', null=True, blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='github_account',
            field=models.URLField(verbose_name='Cuenta de GitHub', null=True, blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin_account',
            field=models.URLField(verbose_name='Cuenta de LinkedIn', null=True, blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(verbose_name='Avatar', null=True, blank=True, upload_to='profile_pics/'),
        ),
    ]
