from django import forms

from users.models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('faceless', 'image')
        labels = {
            'faceless': 'I do not want my picture to appear in the yearbook.'
        }