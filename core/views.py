from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from users.models import UserProfile
from .forms import ProfileUpdateForm

import os

from django.db import models
from django.dispatch import receiver


# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def profile(request):
    the_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=the_profile)

    if form.is_valid():
        profile = form.save(commit=False)

        if profile.faceless:
            profile.image = None
        profile.save()

    return render(request, "profile.html", {'form' : form})


# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = UserProfile.objects.get(pk=instance.pk).image
    except UserProfile.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError:
            return False