from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import fitz

# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def test(request):
    # return HttpResponse("<h4>about</h4>")
    resp = ""
    pdffile = "PGIdata_2015-4.pdf"

    resp = pdffile


    return HttpResponse(resp)
