from django.http import HttpResponse
from django.shortcuts import render_to_response


def result(request, theme):
    return render_to_response('result.html')


def index(request, theme):
    return HttpResponse('')
