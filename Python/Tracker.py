import math
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt

class Camera:
    """Camera"""
    def __init__(self, camera_index):
        self.cap = None
        self.camera_index = camera_index
        
    def connect(self):
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
        except:
            print("Failed connect to camera ",self.camera_index)

    def disconnect(self):
        try:
            self.cap.release()
        except:
            print("Failed disconnect to camera ",self.camera_index)
            
    def get_frame(self):
        if(self.cap is None):
            print("Camera is not open")
            return
        ret, frame = self.cap.read()
        return ret, frame
    
class Tracker:
    """Tracker"""
    def __init__(self):
        self.upper_threshold = None
        self.lower_threshold = None

    def set_threshold(self, upper_threshold, lower_threshold):
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        
    def threshold(self, frame):
        return frame

    def track(self, frame):
        ball_distance = 0
        ball_degree = 0
        return frame, ball_distance, ball_degree
    
class Display:
    """Display"""
    def __init__(self, name, height, weight):
        self.name = name
        self.height = height
        self.weight = weight
        cv2.namedWindow(name)
        
    def show(self,image):
        cv2.imshow(self.name, image)

class Input:
    """Input"""
    def __init__(self):
        self.use_default = 1
        self.default_upper = np.array([50,255,255])
        self.default_lower = np.array([0,170,170])
        self.upper_h = 255
        self.lower_h = 0
        self.upper_s = 255
        self.lower_s = 0
        self.upper_v = 255
        self.lower_v = 0
        self.min_value = 0
        self.max_value = 1000
        
    def nothing(self,x):
        pass
    
    def create_trackbar(self):
        self.threshold = Display('Threshold',640,480)
        cv2.createTrackbar('Use Default','Threshold',0,1,self.nothing)
        cv2.createTrackbar('Upper H','Threshold',0,179,self.nothing)
        cv2.createTrackbar('Lower H','Threshold',0,179,self.nothing)
        cv2.createTrackbar('Upper S','Threshold',0,255,self.nothing)
        cv2.createTrackbar('Lower S','Threshold',0,255,self.nothing)
        cv2.createTrackbar('Upper V','Threshold',0,255,self.nothing)
        cv2.createTrackbar('Lower V','Threshold',0,255,self.nothing)
        cv2.createTrackbar('Min Value','Threshold',0,10000,self.nothing)
        cv2.createTrackbar('Max Value','Threshold',0,10000,self.nothing)
        
    def update_value(self):
        self.use_default = cv2.getTrackbarPos('Use Default','Threshold')
        self.upper_h = cv2.getTrackbarPos('Upper H','Threshold')
        self.lower_h = cv2.getTrackbarPos('Lower H','Threshold')
        self.upper_s = cv2.getTrackbarPos('Upper S','Threshold')
        self.lower_s = cv2.getTrackbarPos('Lower S','Threshold')
        self.upper_v = cv2.getTrackbarPos('Upper V','Threshold')
        self.lower_v = cv2.getTrackbarPos('Lower V','Threshold')

    def get_value(self):
        if(self.use_default is 1):
            return self.default_upper, self.default_lower
        else:
            return np.array([self.upper_h,self.upper_s,self.upper_v]), np.array([self.lower_h,self.lower_s,self.lower_v])
