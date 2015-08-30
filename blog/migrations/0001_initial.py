# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(unique=True, max_length=50)),
                ('imagen_destacada', models.ImageField(blank=True, null=True, upload_to='articles_pics/%Y-%m-%d/')),
                ('contenido', models.TextField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='titulo', unique=True, editable=False)),
                ('estado', models.CharField(choices=[('b', 'borrador'), ('p', 'publicado')], default='b', max_length=1)),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Articulo',
                'verbose_name_plural': 'Articulos',
                'ordering': ('-creado_en',),
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(unique=True, max_length=20)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='nombre', unique=True, editable=False)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ('nombre',),
            },
        ),
        migrations.AddField(
            model_name='articulo',
            name='categoria',
            field=models.ForeignKey(to='blog.Categoria'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='tags',
            field=taggit.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
