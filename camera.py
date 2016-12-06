
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np 

windowName = "Hough Circle Detection Original"
windowName2 = "Hough Circle Detection Masked Red"
cannyThresholdTrackbarName = "Canny threshold"
accumulatorThresholdTrackbarName = "Accumulator Threshold"
cannyThresholdInitialValue = 200 
accumulatorThresholdInitialValue = 100
maxAccumulatorThreshold = 200
maxCannyThreshold = 255
LOWER_RED1 = (0, 181, 3)
LOWER_RED2 = (1, 232, 200)
UPPER_RED1 = (168, 181, 3)  
UPPER_RED2 = (179, 232, 200)
LOWER_IR   = (110, 100, 47)
UPPER_IR   = (138, 184, 255)
     
def nothing(x):
    pass 
    
#Pyimagesearch.com
def main_method():
    ######################################################
    # TEMP VARIABLES
    #imageType = "Glove"
    #color = "Infared" 
    imageType = "Ball"
    color = "Red" 
    ######################################################
    camera, rawCapture, cannyThreshold, accumulatorThreshold = setup_camera()
    #Grab frame
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #Apply masks to frame. 
        src, masked_image, accumulatorThreshold, cannyThreshold = processFrame(frame, cannyThreshold, accumulatorThreshold, imageType) 
        #Find ball and IR leds.   
        src, coordinates = houghDetection(src,masked_image, imageType)
        #Display images. 
        display_images(src, masked_image, color, imageType)
        ###############################################################
        #ADD STUFFS!!!!!!!!!!
        ###############################################################


        ###############################################################
        #END ADD STUFFS!!!!!!!!!
        #################################################################
        key = cv2.waitKey(1) & 0xFF
        #Get new frame. 
        rawCapture.truncate(0)
        if key == ord("q"):
            break

def display_images(src, masked_image, color, imageType):   
        cv2.imshow("Masked " + color, masked_image)
        cv2.imshow("Detecting " + imageType, src)
  
def setup_camera():    
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32  
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(1)  
    cannyThreshold = cannyThresholdInitialValue;
    accumulatorThreshold = accumulatorThresholdInitialValue;
    return camera, rawCapture, cannyThreshold, accumulatorThreshold 
    #Loop!
  
def processFrame(frame, cannyThreshold, accumulatorThreshold, masktype):       
        src = frame.array  
        image = cv2.medianBlur(src, 3)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #Reduce the noise so we avoid false circle detection
        #From documentation tutorial:
        if masktype == "Ball":
            lower_red = cv2.inRange(hsv, LOWER_RED1, LOWER_RED2)
            upper_red = cv2.inRange(hsv, UPPER_RED1, UPPER_RED2)
            masked_image = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0)
            masked_image = cv2.GaussianBlur(masked_image, (9, 9), 0)
        else:   
            masked_image = cv2.inRange(hsv, LOWER_IR, UPPER_IR)
        cannyThreshold = max(cannyThreshold, 1)  
        accumulatorThreshold = max(accumulatorThreshold, 1)
        cv2.createTrackbar(cannyThresholdTrackbarName, windowName, cannyThreshold, maxCannyThreshold, nothing)
        cv2.createTrackbar(accumulatorThresholdTrackbarName, windowName, accumulatorThreshold, maxAccumulatorThreshold, nothing)
        return src, masked_image, accumulatorThreshold, cannyThreshold  
 
  
def houghDetection(src, masked_image, imageType):
    if imageType == 'Ball':
        circles = cv2.HoughCircles(masked_image, cv2.HOUGH_GRADIENT, 1, 40,param1=35, param2=20, minRadius=0, maxRadius=0)
    else:  
        circles = cv2.HoughCircles(masked_image, cv2.HOUGH_GRADIENT, 1, 40,param1=25, param2=15, minRadius=0, maxRadius=0)
    if circles != None:
        src = markup_image(src, circles)
    print circles      
    return src, circles  
    
def markup_image(image, circles):              
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:   
        #Outer circle
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        #Center point 
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
    return image  


main_method()  
