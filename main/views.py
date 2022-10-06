from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return HttpResponse("<h4>about</h4>")