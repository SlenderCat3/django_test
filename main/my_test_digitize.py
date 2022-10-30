from dis import show_code
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import views

import time

def show_img(img, scale):
        cv2.namedWindow("window", cv2.WINDOW_NORMAL)
        w = round(img.shape[0] * scale)
        h = round(img.shape[1] * scale)
        # cv2.resizeWindow("window", h, w)
        cv2.imshow("window", cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA))
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        return


img = cv2.imread("main/images/output_32.png") 

originalImage = img.copy()
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)


mask_img = cv2.imread("main/images/mask.png")
mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2RGB)

start = time.time()
result, simple_res, char_res, masked_image = views.digitize_image(img, mask_img)
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


# show_img(masked_image, 0.5)

plt.imshow(masked_image)
plt.show()