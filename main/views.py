from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import dig_img

# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def test(request):
    # return HttpResponse("<h4>about</h4>")
    resp = ""

    img = cv2.imread("output_32.png")

    originalImage = img.copy()
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_RGB2GRAY)
    (thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)


    mask_img = cv2.imread("mask.png")
    mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2RGB)

    result = dig_img.digitize_image(img, mask_img)

    resp += result

    return HttpResponse(resp)