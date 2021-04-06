import cv2
import numpy as np
import os
os.environ['DISPLAY'] = ':0'

def preprocess(image):
    img_copy = image.copy()
    img_copy = cv2.GaussianBlur(img_copy, (9,9), 0)

    temp = cv2.adaptiveThreshold(img_copy, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    temp = cv2.bitwise_not(temp, temp)
    return temp

def find_corner(image):
    external_contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    external_contours = external_contours[0] if len(external_contours) == 2 else external_contours[1]

    for contourn in external_contours:
        peri = cv2.arcLength(contourn, True)
        approx = cv2.approxPolyDP(contourn, 0.015 * peri, True)
        if len(approx) == 4:
            
            return approx


def order_corner_points(corners):
    corners = [(corner[0][0], corner[0][1]) for corner in corners]
    top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
    return top_l, top_r, bottom_r, bottom_l


def perspective_transform(image, corners):
    # Order points in clockwise order
    ordered_corners = order_corner_points(corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners

    # Determine width of new image which is the max distance between
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_A = np.sqrt(((bottom_r[0] - bottom_l[0])
                      ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) +
                      ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))

    # Determine height of new image which is the max distance between
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) +
                       ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) +
                       ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))

    # Construct new points to obtain top-down view of image in
    # top_r, top_l, bottom_l, bottom_r order
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                           [0, height - 1]], dtype="float32")

    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")

    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    grid = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # Return the transformed image
    return cv2.warpPerspective(image, grid, (width, height))


image = cv2.imread('01042021_1655.jpg', 0)
temp = preprocess(image)
temp_corner = find_corner(temp)
trans = perspective_transform(temp, temp_corner)
cv2.imwrite('temp.jpg', trans)
