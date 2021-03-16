import cv2
import imutils
import numpy as np
import os
os.environ['DISPLAY'] = ':0'

def print_image(image):
    print('here')
    cv2.imshow('thresh', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image = cv2.imread('6. Computer Vision/07. Template matching, corners and Haar cascades/img/sudoku.jpg', 0)
#gray = cv2.cvtColor(image, cv2.COLOR_BAYER_BG2GRAY)
thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 57, 5)
#print(thresh.shape)
contourns, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contourn in contourns:
    area = cv2.contourArea(contourn)
    if area < 500:
        cv2.drawContours(thresh, [contourn], -1, (0,0,0), -1)

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4) 

print_image(thresh)