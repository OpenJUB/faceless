from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from django.contrib import admin

import json


def upload_to(instance, filename):
    return 'yearbook/{0}.jpg'.format(instance.user.username, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    image = models.ImageField(upload_to=upload_to, null=True,
                              blank=True)
    faceless = models.BooleanField(default=False)
    details = models.TextField()

    def __str__(self):
        return u'[Profile] %s' % (self.user.username)

    def clean(self):
        # make sure that the details are a valid json object
        try:
            json.loads(self.details)
        except:
            raise ValidationError({
                'details': ValidationError(
                    'Details needs to be a valid JSON object', code='invalid')
            })


admin.site.register(UserProfile)
