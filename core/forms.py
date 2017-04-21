from django import forms

from users.models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('faceless', 'image')
