from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def view(request):
    return HttpResponse("Hello, world!")