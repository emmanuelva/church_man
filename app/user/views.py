"""
Views for the user API
"""
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views import View
from django.utils.translation import gettext as _
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.forms import LoginForm, SignUpForm
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


# API views
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# Web app views
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html', {
            'form': SignUpForm,
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password_conf = form.cleaned_data.get('password1')

            errors = []

            if password_conf != password:
                errors.append(_('SignUpIncorrectPasswordError'))
            if get_user_model().objects.filter(email=email).exists():
                errors.append(_('SignUpExistingEmailError'))

            have_errors = len(errors) > 0

            if not have_errors:
                try:
                    get_user_model().objects.create_user(email=email, password=password)
                except Exception as ex:
                    errors.extend([x[0] for x in ex.args])

            if have_errors:
                return render(request, 'signup.html', {
                    'have_errors': have_errors,
                    'errors': errors,
                    'form': UserCreationForm,
                })

            return render(request, 'signup_success.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {
            'form': LoginForm,
        })

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            return render(request, 'login.html', {
                'form': LoginForm,
                'errors': [_('LoginInvalidError')],
            })
        login(request, user)
        return redirect('home')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
