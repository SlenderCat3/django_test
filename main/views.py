from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract

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

    result = digitize_image(img, mask_img)

    resp += result

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


def digitize_image(img, mask_img):

    str_return = ""

    white = Color((255, 255, 255))
    black = Color((0, 0, 0))

    height, width = img.shape
    mask_height, mask_width, _ = mask_img.shape

    X_line = 1900
    y_jump = 200

    prev_start = 0

    def mask_image(x1, y1):
        ar = []
        for y in range(5):
            temp = []
            for x in range(48):
                temp.append(Cell(y, x))
            ar.append(temp)

        cells = np.array(ar)

        x2 = x1 + 1658
        y2 = y1 + 174

        for h in range (y1, y2 + 1):
            mh = h - y1 + 4

            for w in range(x1, x2 + 1):
                mw = w - x1 + 4

                mask_color = Color(tuple(mask_img[mh, mw]))
                img_color = img[h, w]

                if (mask_color.b == 255):
                    # obj[w, h] = (255, 255, 255)
                    1
                    # do something

                elif (mask_color.r != 255 and mask_color.g != 255):
                    row = mask_color.r // 50
                    column = mask_color.g // 5
                    cells[row, column].area += 1    

                    if (cells[row, column].x == -1):
                        cells[row, column].x, cells[row, column].y = w, h

                    if (img_color == 0):
                        cells[row, column].black_area += 1

        cellsK = 0
        for y in range(5):
            for x in range(48):
                cells[y, x].calc()
                if (round(cells[y, x].cover, 3) >= 0.8):
                    cellsK += 1

        return cells, cellsK



    for y in range(200, height - 200):
        if (prev_start == 0 or (y-prev_start) > y_jump):
            cur = img[y, X_line]
            down = img[y+1, X_line]

            if (cur == 255 and down == 0):
                prev_start = y
                # print("-"*10)
                str_return += "-"*10 + "\n"
                # print(f"Table start coords: ({y};", end = "")

                for x in range(350, 700):
                    cur = img[y + 20, x]
                    right = img[y + 20, x+1]

                    if (cur == 255 and right == 0):
                        # print(f"{x})")
                        # plt.text(x, y, f"({x};{y})", ha = 'right')

                        crop_img_text = img[y-75:y, x:x+420]
                        text = pytesseract.image_to_string(crop_img_text).strip()
                        # print("Date:",text)
                        str_return += "Date: " + text + "\n"
                        cells, cellsK = mask_image(x, y)
                        # print("Dark squares:", cellsK)
                        str_return += "Dark squares: " + str(cellsK) + "\n"

                        break

    return str_return