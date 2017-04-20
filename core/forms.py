from django import forms

class ProfileUpdateForm(forms.Form):
    faceless = forms.BooleanField(required=False,
                                  label='Show me as faceless in yearbook',
                                  help_text='(checkbox will remove current '
                                            'image)')
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput,
                             label='New Profile picture',
                             help_text="(leave blank for unchanged)")
