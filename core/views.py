from django.contrib.auth.decorators import login_required
from django_cleanup import cleanup

from django.shortcuts import render

from users.models import UserProfile
from .forms import ProfileUpdateForm


# Create your views here.
def home(request):
    return render(request, "home.html")


def clear_image(user):
    if user.profile.image is not None:
        user.profile.image.delete()
        cleanup.refresh(user.profile)

@login_required
def profile(request):
    the_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            print('form', form.cleaned_data)

            # if the user wishes to be faceless, clear the image
            if form.cleaned_data['faceless']:
                the_profile.faceless = True
                clear_image(request.user)

            # else, check if we uploaded an image
            else:
                the_profile.faceless = False
                image = form.cleaned_data['image']

                # if so, we want to save it
                if image:
                    clear_image(request.user)
                    request.user.profile.image.save(image.name, image)

            the_profile.save()
    else:
        form = ProfileUpdateForm()

    return render(request, "profile.html", {'form' : form})
