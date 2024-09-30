from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    respond = '<h1>Home Blog Here</h1>'
    return HttpResponse(respond)