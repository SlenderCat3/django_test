from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import time

# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def test(request):
    # return HttpResponse("<h4>about</h4>")
    resp = ""

    img = cv2.imread("main/images/output_32.png")

    originalImage = img.copy()
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_RGB2GRAY)
    (thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)


    mask_img = cv2.imread("main/images/mask.png")
    mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2RGB)
    
    start_time = time.time()
    result, _, _ = digitize_image(img, mask_img)
    end_time = time.time()

    resp += result
    resp += f"Elapsed time: {end_time-start_time} seconds <br>"

    return HttpResponse(resp)




class Cell:
    def __init__(self, x, y):
        self.row = x        # строка
        self.column = y     # столбец
        self.x = -1         # координаты левого верхнего угла ячейки, x
        self.y = -1         # координаты левого верхнего угла ячейки, y
        self.area = 0       # Общая площадь пикселей
        self.black_area = 0 # Площадь черных пикселей
        self.cover = 0.0    # покрытие черными пикселями

        # Существует ли закрашенный пиксель на данном ребре
        self.upper_corner = False
        self.left_corner  = False
        self.right_corner = False
        self.lower_corner = False

        self.value = "."


    # Вычисление покрытия черными пикселями
    def calc_area(self):
        if (self.area > 0):
            if (self.black_area > 0):
                self.cover = self.black_area / self.area
    
    def calc_value(self):
        
        if (self.cover == 0):
            return
        
        if (self.cover == 1):
            self.value = "#"
        
        elif (self.upper_corner and self.lower_corner and (not self.left_corner) and (not self.right_corner)):
            self.value = "|"
        
        elif (self.right_corner and self.left_corner and (not self.upper_corner) and (not self.lower_corner)):
            self.value = "—"
        
        else:
            self.value = "*"


class Color:
  def __init__(self, color):
    [self.r, self.g, self.b] = color

def colors_match(c1, c2):
    return (c1.r == c2.r and c1.g == c2.g and c1.b == c2.b)


def digitize_image(img, mask_img):
    start_table = "<table style=\"table-layout: fixed; border:1px solid black; border-collapse: collapse\">"
    str_return = ""
    str_simple_return = ""
    str_char_return = ""

    white = Color((255, 255, 255))
    black = Color((0, 0, 0))

    height, width = img.shape
    mask_height, mask_width, _ = mask_img.shape

    X_line = 1900
    y_jump = 200

    prev_start = 0

    def cells_to_str(cells):
        res = ""
        char_res = ""

        for y in range(5):
            res += "<tr style=\"height:20px\">"
            for x in range(48):
                val = int(round(cells[y, x].cover, 1) * 10)
                col = "#FFFFFF"
                if (val == 10):
                    col = "#888888"
                elif (val > 0):
                    col = "#DCDCDC"

                res += f"<td style = \"border:1px solid black; border-collapse: collapse; text-align: center; width: 20px;\" bgcolor=\"{col}\">{cells[y, x].value}</td>"
                char_res += cells[y, x].value
            res += "</tr>"
            char_res += "\n"
        
        return res, char_res

    def mask_image(x1, y1):

        # Создание массива ячеек
        ar = []
        for y in range(5):
            temp = []
            for x in range(48):
                temp.append(Cell(y, x))
            ar.append(temp)
        cells = np.array(ar)

        # (x1, y1) и (x2, y2) - границы рассматриваемого изображения
        x2 = x1 + 1658
        y2 = y1 + 174

        # Ширина левой границы маски
        blue_left_corner_width = 14

        # Цикл по всем пикселям интересующей площади с шагом 2
        for h in range (y1, y2 + 1, 2):

            # относительная координата Y
            mh = h - y1 + 4

            for w in range(x1 + blue_left_corner_width, x2 + 1, 2):

                # относительная координата X
                mw = w - x1 + 4

                # Получение цвета маски: RGB
                mask_color = Color(mask_img[mh, mw])

                if (colors_match(mask_color, white)):
                    break

                # Получение значения изображения: 0 или 1
                img_color = img[h, w]

                # Если маска синего цвета

                if (mask_color.b != 255):

                    # Получение координат ячейки из цвета маски
                    row = mask_color.r // 50
                    column = mask_color.g // 5

                    # Добавление к площади ячейки 1
                    cells[row, column].area += 1    

                    # Если начальный координаты ячейки отсутствуют, задаем их
                    if (cells[row, column].x == -1):
                        cells[row, column].x, cells[row, column].y = w, h

                    # Добавление к закрашенной площади ячейки 1
                    if (img_color == 0):
                        cells[row, column].black_area += 1

                        check_step = 3

                        mask_upper = Color(mask_img[mh - check_step, mw]).b == 255
                        mask_right = Color(mask_img[mh, mw + check_step]).b == 255
                        mask_left  = Color(mask_img[mh, mw - check_step]).b == 255
                        mask_lower = Color(mask_img[mh + check_step, mw]).b == 255

                        if (mask_upper):
                            cells[row, column].upper_corner = True
                        
                        if (mask_right):
                            cells[row, column].left_corner  = True
                        
                        if (mask_left):
                            cells[row, column].right_corner = True
                        
                        if (mask_lower):
                            cells[row, column].lower_corner = True


        # Подсчет закрашенныйх клеток для всего аскаплота
        cellsK = 0
        for y in range(5):
            for x in range(48):
                cells[y, x].calc_area()
                cells[y, x].calc_value()
                if (round(cells[y, x].cover, 3) >= 0.8):
                    cellsK += 1

        return cells, cellsK



    for y in range(200, height - 200):
        if (prev_start == 0 or (y-prev_start) > y_jump):
            cur = img[y, X_line]
            down = img[y+1, X_line]

            if (cur == 255 and down == 0):
                prev_start = y

                for x in range(350, 700):
                    cur = img[y + 20, x]
                    right = img[y + 20, x+1]

                    if (cur == 255 and right == 0):

                        crop_img_text = img[y-75:y, x:x+420]
                        # text = pytesseract.image_to_string(crop_img_text).strip()

                        cells, cellsK = mask_image(x, y)

                        str_return += start_table
                        res, char_res = cells_to_str(cells)
                        str_return += res
                        str_return +="</table><br>"

                        str_simple_return += str(cellsK) + ", "

                        str_char_return += char_res
                        str_char_return += "\n"

                        break
    
    str_return += "<img src = \"main/images/output_32.png\">"
    return str_return, str_simple_return, str_char_return