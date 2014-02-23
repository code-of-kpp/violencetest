from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from .models import ViolentPhoto, Theme


def result(request, theme):
    theme = get_object_or_404(Theme, short_name=theme)

    vp = ViolentPhoto.objects.filter(theme=theme).all()

    return render_to_response('result.html', {'photos': vp})


def index(request, theme):
    return HttpResponse('')
