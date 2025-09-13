#imports
import numpy as np
import cv2

def preprocess(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)            # RGB to grayscale conversion
    blur = cv2.GaussianBlur(gray,(7,7),0)                    # Apply Gaussian blur to reduce noise
    canny = cv2.Canny(blur,10,150)                           # Apply Canny Edge Deetection
    # cv2.imshow("canny",canny)                     
    return canny

def region(image):                                           # Find the Region of Interest(ROI) in the image
    height, width = image.shape[0:2]
    triangle = np.array([
        [(0, height), (0.35*width, 0.4*height),(width*0.55, height*0.4), (width, height)], #parameters can be varied accordingly
    ],dtype=np.int32)

    mask = np.zeros_like(image)
    mask = cv2.fillPoly(mask,triangle,255)
    mask = cv2.bitwise_and(image, mask)
    # cv2.imshow("region",mask)
    return mask

def lines(copy,image):                                        # Apply Hough Transform to obtain all straight lines from the image
    line = cv2.HoughLinesP(image, 2, np.pi / 180, 200, np.array([]), minLineLength=40, maxLineGap=5)
    avg = average(copy,line)                                  # Obtain the average of lines on both left and right
    black_lines=display_lines(copy,line)                      
    lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
    # cv2.imshow("lines",lanes)
    return lanes

def average(image, lines):                                    # Function to obtain average
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
     if lines is not None and len(lines)==2:
       for line in lines:
         x1, y1, x2, y2 = line
         cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

       x1,y1,x2,y2 = lines[0]
       x3,y3,x4,y4 = lines[1]
       line1 = [(x1, y1), (x2, y2)]  # First line
       line2 = [(x3, y3), (x4, y4)]  # Second line

       # Combine the endpoints to form a polygon
       polygon_points = np.array([line1[0], line1[1], line2[1], line2[0]])

       overlay = image.copy()

       # Draw filled polygon on overlay to produce a mask
       cv2.fillPoly(overlay, [polygon_points], color=(0, 0, 255))  # Red mask

       # Blend overlay with original image
       alpha = 0.3  # Transparency factor
       highlighted = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
       return highlighted


#main code
img = cv2.imread('lane4.jpg')
img = cv2.resize(img,(640,480))
cv2.imshow('image',img)
cv2.waitKey(0)

copy = np.copy(img)

image = preprocess(img)
image2 = region(image)
line = cv2.HoughLinesP(image2, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
avg = average(copy, line)
black = display_lines(copy, avg)
cv2.imshow('lane', black)
cv2.waitKey(0)



