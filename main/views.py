from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

import numpy as np
import pytesseract
import fitz
from PIL import Image
import cv2

# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def test(request):
    # return HttpResponse("<h4>about</h4>")
   
    return HttpResponse("<h4>about</h4>")
