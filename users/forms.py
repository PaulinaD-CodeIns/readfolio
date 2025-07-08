from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Forename")
    last_name = forms.CharField(max_length=30, label="Surname")

    field_order = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
