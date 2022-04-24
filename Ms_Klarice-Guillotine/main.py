import cv2
import numpy as np
from io import BytesIO
from Robot import Robot, Motor, Servo
import sys
import AprilTag as aprt
from time import time
#print("{}  {}".format("Analyze this file: ", sys.argv[1]))

# Motor1 -> Left motor
r = Robot(Motor(8, 10), Motor(16, 18), Servo(32))


def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v


tme = time()

while True:
    im = cv2.imread('image.jpg')
    im = cv2.rotate(im, cv2.ROTATE_180)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    n_time = time()
    diff_time = n_time-tme
    x = 0
    w = 0

    if diff_time < 120:

        #im = cv2.imread(sys.argv[1])
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        cv2.imshow('image',imgray)
        cv2.waitKey(50)
        # Thresholding - delete all points outside 60cm - 150cm
        ret, thresh = cv2.threshold(imgray, 60, 150, 0)
        cv2.imshow('thresh',thresh)
        cv2.waitKey(50)

        kernel = np.ones((7,7),np.uint8)
        erosion = cv2.erode(thresh, kernel, iterations = 4)
        dilation = cv2.dilate(erosion, kernel, iterations = 4)
        cv2.imshow('dilation', dilation)
        cv2.waitKey(50)


        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        cv2.drawContours(im, contours, -1, (255,255,0), 3)
        cv2.imshow('contours',im)
        cv2.waitKey(50)

        (x,y),radius = cv2.minEnclosingCircle(contours[8])
        h, w, z = im.shape

    else:
        try:
            x, w = aprt.find_apriltag(imgray, 0)
        except BaseException:
            x = -500
            w = 1000


    if x < w * 0.4:
        r.motor1.drive(50 + 50 * ((w / 2 - x) / (w / 2)))
        r.motor2.drive(100)
        # go left proportional to w/2 - x
    elif x > w * 0.6:
        r.motor1.drive(100)
        r.motor2.drive(50 + 50 * ((w / 2 - (w - x)) / (w / 2)))
        # go right proportional to w/2 - x
    else:
        r.forward()
        # go ahead
