from django.shortcuts import render  # noqa


def home(response):
    return render(response, 'home.html', {})
