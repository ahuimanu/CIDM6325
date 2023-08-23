from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    item = ''.join(request.GET.values())
    # item = request.GET["dude"]
    return HttpResponse(f"DUDE, You're Gettin' a DELL - {item}")