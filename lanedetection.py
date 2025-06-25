import numpy as np
import pandas as pd
import cv2


#convert into grey scale image
def grey(image):
  image=np.asarray(image)
  return cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
#Gaussian blur to reduce noise and smoothen the image
def gauss(image):
  return cv2.GaussianBlur(image,(5,5),0)
#Canny edge detection
def canny(image):
    edges = cv2.Canny(image,50,150)
    return edges


def region(image):
    height, width = image.shape
    triangle = np.array([
        [(100, height), (475, 325), (width, height)]
    ])

    mask = np.zeros_like(image)

    mask = cv2.fillPoly(mask, triangle, 255)
    mask = cv2.bitwise_and(image, mask)
    return mask

def average(image, lines):
    left = []
    right = []
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        y_int = parameters[1]
        if slope < 0:
            left.append((slope, y_int))
        else:
            right.append((slope, y_int))
    right_avg = np.average(right, axis=0)
    left_avg = np.average(left, axis=0)
    left_line = make_points(image, left_avg)
    right_line = make_points(image, right_avg)
    return np.array([left_line, right_line])

def make_points(image, average):
 slope, y_int = average
 y1 = image.shape[0]
 y2 = int(y1 * (3/5))
 x1 = int((y1-y_int) // slope)
 x2 = int((y2-y_int) // slope)
 return np.array([x1, y1, x2, y2])

def display_lines(image, lines):
 lines_image = np.zeros_like(image)
 if lines is not None:
   for line in lines:
     x1, y1, x2, y2 = line
     cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
 return lines_image

img = cv2.imread('lane.jpg')
img = cv2.resize(img,(600,600))
cv2.imshow('image', img)
copy = np.copy(img)
grey = grey(copy)
gaus = gauss(grey)
edges = canny(gaus)
isolated = region(edges)
lines = cv2.HoughLinesP(isolated, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
averaged_lines = average(copy, lines)
black_lines = display_lines(copy, averaged_lines)
lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
cv2.imshow("lanes", lanes)
cv2.waitKey(0)