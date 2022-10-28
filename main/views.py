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

    
    white = Color((255, 255, 255))
    black = Color((0, 0, 0))

    zoom = 4.165
    mat = fitz.Matrix(zoom, zoom)
    doc = fitz.open(pdffile)
    page = doc.load_page(31)
    pix = page.get_pixmap(matrix = mat)
    pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = np.array(pil_image)
    img = img[:, :, ::-1].copy()

    resp = img.shape


    return HttpResponse(resp)



class Cell:
    def __init__(self, x, y):
        self.row = x # строка
        self.column = y # столбец
        self.x = -1
        self.y = -1
        self.area = 0
        self.black_area = 0
        self.cover = 0.0 # покрытие черными пикселями

    def calc(self):
        if (self.area > 0):
            if (self.black_area > 0):
                self.cover = self.black_area / self.area

class Color:
  def __init__(self, color):
    self.r, self.g, self.b = color

def colors_match(c1, c2):
    return (c1.r == c2.r and c1.g == c2.g and c1.b == c2.b)

