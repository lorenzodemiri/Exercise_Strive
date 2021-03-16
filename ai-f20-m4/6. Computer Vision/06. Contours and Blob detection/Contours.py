import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
os.environ['DISPLAY'] = ':0'

def detect(countorn):
    shape = "not_found"
    
    peri = cv2.arcLength(countorn, True)
    approx = cv2.approxPolyDP(countorn, 0.04 * peri, True)
    if len(approx) == 3:
        shape = "Triangle"
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        if ar >= 0.95 and ar <= 1.05:
            shape = "Square"
        else:
            shape = "Rectangle"
    elif len(approx) == 5:
            shape = "Pentagon"
    else:
        shape = "Circle"
        
    return shape


def get_contourn(img, 
                 thresh_val = 100, 
                 apply_canny = False, 
                 canny_start = 50, 
                 apply_gaussBlur = False, 
                 gauss_kernel = (7,7),
                 apply_dilation = False,
                 kernel_dilation = (3,3)
                ):
    var_THRESH = cv2.THRESH_BINARY_INV
    
    if apply_gaussBlur is True: img = cv2.GaussianBlur(img, gauss_kernel, 0)
    
    if apply_canny is True: 
        img = cv2.Canny(img, canny_start, 255)
        var_THRESH = cv2.THRESH_BINARY
    
    if apply_dilation is True:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,kernel_dilation)
        img  = cv2.dilate(img, kernel, iterations = 1)
    
    ret, th = cv2.threshold(img, thresh_val, 255, var_THRESH)    
    img_contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("Detected {} shapes".format(len(img_contours[0])))
    img_contours = imutils.grab_contours(img_contours)
    return img_contours


shape_img = cv2.imread('6. Computer Vision/06. Contours and Blob detection/img/test.jpg', cv2.IMREAD_COLOR)
rgb_img = cv2.cvtColor(shape_img,cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)


countorn_vect = get_contourn(img_gray,
                 thresh_val = 60, 
                 apply_canny = True,
                 canny_start = 100, 
                 apply_gaussBlur = True,
                 gauss_kernel = (3,3),
                 apply_dilation = False,
                 kernel_dilation = (3,3))



for countorn in countorn_vect:
    M = cv2.moments(countorn)
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    shape = detect(countorn)

    cv2.drawContours(shape_img, [countorn], -1, (255, 0, 0), 2)
    cv2.putText(shape_img, shape,(cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    cv2.imshow("Image", shape_img)
    cv2.waitKey(0)

cv2.destroyAllWindows()