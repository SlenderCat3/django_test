from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import views

import time

img = cv2.imread("images/output_32.png") 

originalImage = img.copy()
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)


mask_img = cv2.imread("images/mask.png")
mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2RGB)

start = time.time()
result, simple_res, char_res = views.digitize_image(img, mask_img)
end = time.time()

print(simple_res)

print(f"Elapsed: {end-start} seconds")

# cut = len(result)//2
# print(result[:cut], end = "")
# print(result[cut:])

print(char_res)


# 20 simple
# 5 with 2 pixels step
# 4 with skip blue lines

# 16.5 with 1 step