import os

from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from django.contrib import admin

import json


def upload_to(instance, filename):
    return 'yearbook/{0}{1}'.format(instance.user.username, os.path.splitext(filename)[1])


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    image = models.ImageField(upload_to=upload_to, null=True,
                              blank=True)
    faceless = models.BooleanField(default=False)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return u'[Profile] %s' % self.user.username


admin.site.register(UserProfile)
