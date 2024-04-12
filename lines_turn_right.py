import numpy as np
import cv2
from heapq import nlargest
from InternalLogic import MotorTurnOnRide, MotorForward, MotorTurnRight
from multiprocessing import Process 
from multiprocessing import Pipe

video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 640)
video_capture.set(4, 480)

# def motor_run(pipe):
#     while True:
#         if pipe.poll() is None:
#             brake
#         MotorTurnOnRide(pipe.recv(),50)
#
# conn,conn1=Pipe()
# motors=Process(target=motor_run,args=(conn1,))
# motors.start()
while(True):
    #print("1 cycle")
    # Capture the frames
    ret, frame = video_capture.read()

    # Crop the image
    crop_img = frame[0:480, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 

    canny = cv2.Canny(gray, 210, 250)

    # Find the lines in the frame
    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 30, minLineLength=60, maxLineGap=10)
    
    
    if lines is None:
        MotorTurnRight(90)
        continue
    
    lines = lines [:,0,:]
    
#    print(lines)
    if len(lines) > 0:
        mx=0
        x1m=0
        x2m=0
        y1m=0
        y2m=0
        for x1, y1, x2, y2 in lines:
            if mx<abs(x1-x2): 
                mx=abs(x1-x2)
                y1m=y1
                y2m=y2
                x1m=x1
                x2m=x2
#         if mx<200:
#             MotorForward(50)
#             continue
        tn=(x1m-x2m)/(y1m-y2m)
        print (tn)
        #yc=int ((y1m+y2m)/2)
        #cv2.line(crop_img,(0,yc),(640,yc),(255,0,0),1)                     
        cv2.line(crop_img,(x1m,y1m),(x2m,y2m),(255,0,0),4)
        if tn < 1.2 or tn > 1.5:
            MotorTurnRight(90)
        else:
            break
#             
            
#     else:
#         print ("I don't see the line")

    #Display the resulting frame
    cv2.imshow('frame',crop_img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
MotorTurnRight(0)