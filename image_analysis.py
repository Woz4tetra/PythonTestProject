import numpy as np
import cv2

def mouse_event(event, x, y, flags, param):
    print(x, y)

def analyze_image():
    dots = cv2.imread('sol_27_dots.png',0)
    rows, cols = np.where(dots == 0)

    img = cv2.imread('sol_27.png')

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_event)

    row = max(rows)
    col = cols[np.argmax(rows)]

    width = img.shape[1]
    height = img.shape[0]

    img = cv2.circle(img, (col, row), 10, (0, 0, 0), 10)
    img = cv2.line(img, (0, row), (width, row), (0, 0, 0), 4)

    #cv2.imshow('image', cv2.resize(img, (width // 4, height // 4)))
    #cv2.imshow('image', img[0:height // 2, 0:width // 2])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def linear_interp(x, x0, x1, y0, y1):
    return (y1 - y0) / (x1 - x0) * (x - x0) + y0

print(linear_interp(523, 529, 503, 690, 700))
print(linear_interp(156, 191, 157, 34, 36))
print(linear_interp(231, 208, 236, 60, 40))
