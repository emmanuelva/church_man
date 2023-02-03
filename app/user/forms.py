from django import forms
from django.utils.translation import gettext as _


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(label=_('PasswordField'), widget=forms.PasswordInput, max_length=150)


class SignUpForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label=_('PasswordField'), widget=forms.PasswordInput, max_length=150)
    password2 = forms.CharField(
        label=_('PasswordConfirmField'),
        widget=forms.PasswordInput,
        max_length=150,
        min_length=8,
    )
