import math
import time
import cv2
import numpy as np
import serial
from matplotlib import pyplot as plt

font = cv2.FONT_HERSHEY_SIMPLEX

def nothing(x):
    pass

#Create Trackbar
def createTrackbar():
    cv2.createTrackbar('Use Default','Threshold',0,1,nothing)
    cv2.createTrackbar('Upper H','Threshold',0,255,nothing)
    cv2.createTrackbar('Lower H','Threshold',0,255,nothing)
    cv2.createTrackbar('Upper S','Threshold',0,255,nothing)
    cv2.createTrackbar('Lower S','Threshold',0,255,nothing)
    cv2.createTrackbar('Upper V','Threshold',0,255,nothing)
    cv2.createTrackbar('Lower V','Threshold',0,255,nothing)
    cv2.createTrackbar('Min Value','Threshold',0,10000,nothing)
    cv2.createTrackbar('Max Value','Threshold',0,10000,nothing)
    
#Color Tresholding
use_default = 1

default_upper = np.array([50,255,255])
default_lower = np.array([0,170,170])

upper_h = 255
lower_h = 0
upper_s = 255
lower_s = 0
upper_v = 255
lower_v = 0

def thresholding(image):
    upper_h = cv2.getTrackbarPos('Upper H','Threshold')
    lower_h = cv2.getTrackbarPos('Lower H','Threshold')
    upper_s = cv2.getTrackbarPos('Upper S','Threshold')
    lower_s = cv2.getTrackbarPos('Lower S','Threshold')
    upper_v = cv2.getTrackbarPos('Upper V','Threshold')
    lower_v = cv2.getTrackbarPos('Lower V','Threshold')
    
    use_default = cv2.getTrackbarPos('Use Default','Threshold')

    if use_default == 1 :
        upper = default_upper
        lower = default_lower
    else:
        upper = np.array([upper_h, upper_s, upper_v])
        lower = np.array([lower_h, lower_s, lower_v])

    mask = cv2.inRange(image,lower,upper)
    return mask

#Contour
default_min_value = 100
default_max_value = 300

min_value = 0
max_value = 0

def find_contour(image):
    use_default = cv2.getTrackbarPos('Use Default','Threshold')
    
    if use_default == 1:
        min_value = default_min_value
        max_value = default_max_value
    else:
        min_value = cv2.getTrackbarPos('Min Value','Threshold')
        max_value = cv2.getTrackbarPos('Max Value','Threshold')
        
    edge = cv2.Canny(mask,min_value,max_value,3,3,True)

    image, contours, hierarhy = cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
    return edge, contours

#Moment
def calculate_moments(frame, contours):
    cv2.putText(frame,"ROBO KEEPER",(int(width/5),int(height/10)),font,2,(255,0,0),2,cv2.LINE_AA)
    if len(contours)== 0:
        return
    #print("Length",len(contours))
    max_cnt = contours[0]
    max_area = 0#cv2.contourArea(max_cnt)
    for cnt in contours:
        if cv2.contourArea(cnt) > max_area :
            max_cnt = cnt
            max_area = cv2.contourArea(max_cnt)
        else:
            continue
        
    (x,y), radius = cv2.minEnclosingCircle(max_cnt)
    center = (int(x), int(y))
    radius = int(radius)
    frame = cv2.circle(frame,center,radius,(0,0,255),5)
    cv2.putText(frame,str(center),center,font,1.5,(0,0,255),2,cv2.LINE_AA)
    start = (int(width/2),int(height))
    cv2.line(frame,start,center,(0,255,0),30)
    frame = cv2.circle(frame,start,50,(0,255,0),10)
    angle = math.atan2(start[1]-center[1],start[0]-center[0])*360/6.28
    cv2.putText(frame,str(angle),start,font,1.5,(0,0,255),2,cv2.LINE_AA)
    
    return angle

#Main
cap = cv2.VideoCapture(0)
#frame = cv2.imread('pingpong.jpg')
ser = serial.Serial('COM5',115200)
print(ser.name)

height = 480
width = 640
channel = 3
cv2.namedWindow('Threshold')
cv2.namedWindow('Image')

createTrackbar()
while(True):
    command_angle=180
    data = str(command_angle)+'\r\n'
    ser.write(data.encode())
    command_angle=0
    data = str(command_angle)+'\r\n'
    ser.write(data.encode())
        
while(False):
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    #now = time.time()
    ret, frame = cap.read()
    #get = time.time()
    height, width, channel = frame.shape

    ori = frame.copy()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    mask = thresholding(hsv)
    
    edge, contours = find_contour(mask)

    command_angle = calculate_moments(ori, contours)
    if(command_angle==None):
        continue
    command_angle = math.floor(command_angle)
    print(command_angle)
    data = str(command_angle)+'\r\n'
    ser.write(data.encode())
    #time.sleep(1)
    cv2.imshow('Image',ori)
    cv2.imshow('Mask',mask)
    cv2.imshow('Edge',edge)
    #then = time.time()
    #print((get-now)*1000,(then-now)*1000)
    
cap.release()
ser.close()
cv2.destroyAllWindows()
