# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    picture = models.ImageField("Avatar", upload_to='profile_pics/',
                                null=True, blank=True)
    blog_account = models.URLField("Direccion del blog", max_length=255,
                                   blank=True, null=True)
    facebook_account = models.URLField("Cuenta de Facebook", max_length=255,
                                       blank=True, null=True)
    google_plus_account = models.URLField("Cuenta de Google+", max_length=255,
                                          blank=True, null=True)
    twitter_account = models.URLField("Cuenta de Twitter", max_length=255,
                                      blank=True, null=True)
    github_account = models.URLField("Cuenta de GitHub", max_length=255,
                                     blank=True, null=True)
    linkedin_account = models.URLField("Cuenta de LinkedIn", max_length=255,
                                       blank=True, null=True)
    profile = models.CharField("En que te desenvuelves", max_length=20,
                               blank=True, null=True)
    short_bio = models.CharField("Frase descriptiva", max_length=60, blank=True,
                                 null=True)
    bio = models.CharField("Descripción corta", max_length=200,
                           blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
