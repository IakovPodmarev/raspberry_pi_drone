import numpy as np
import cv2
from heapq import nlargest
from InternalLogic import MotorTurnOnRide,MotorTurnRight,MotorStop
from multiprocessing import Process 
from multiprocessing import Pipe
video_capture = cv2.VideoCapture(-1)
# print (video_capture.get(cv2.CAP_PROP_FRAME_WIDTH),video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
#
def nothing(g):
    print(g)
    return(g)

video_capture.set(3, 640)
video_capture.set(4, 480)
#cv2.namedWindow("frame")
# cv2.createTrackbar("Kp",'frame',0,100,nothing)
# cv2.createTrackbar("Target_posiiton",'frame',0,640,nothing)
# cv2.createTrackbar("start/stop",'frame',0,1,nothing)
# cv2.createTrackbar("Kpd",'frame',0,100,nothing)
# cv2.createTrackbar("thresh",'frame',0,250,nothing)
# cv2.createTrackbar("param1",'frame',0,200,nothing)
# cv2.createTrackbar("param2",'frame',0,200,nothing)


# def motor_run(pipe):
#     while True:
#         if pipe.poll() is None:
#             continue
#         err=pipe.recv()
#         if err==51:
#             MotorStop()
#             continue
#         MotorTurnOnRide(err,40)
        
# conn,conn1=Pipe()
# motors=Process(target=motor_run,args=(conn1,))
# motors.start()

arr_error_x=0


while(True):
    
    # Capture the frames
    ret, frame = video_capture.read()
    crop_img = frame[0:480, 0:640]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray,(5,5),0) 
    thresh=220 #cv2.getTrackbarPos("thresh",'frame')
    canny = cv2.Canny(gray, thresh, 250)
    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 30, minLineLength=60, maxLineGap=10)
    if lines is None:
       continue
       print ("I don't see the line")
    lines = lines [:,0,:]
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
            if y1m-y2m==0:
                continue
            tn=(x1m-x2m)/(y1m-y2m)
            print (tn)   
            param1=0.3#cv2.getTrackbarPos("param1",'frame')/10
            param2=2#cv2.getTrackbarPos("param2",'frame')/10
            if tn < param2 and tn > param1:   
                Kp=0#cv2.getTrackbarPos("Kp",'frame')/100
                target=0.9#cv2.getTrackbarPos("Target_posiiton",'frame')  
                Kpd=0#cv2.getTrackbarPos("Kpd",'frame')/100
                cv2.line(crop_img,(x1m,y1m),(x2m,y2m),(255,0,0),4)
                cx=tn-target
                cx=tn*Kp+(tn-arr_error_x)*Kpd
                arr_error_x=cx
#     #          arr_error_y=cy
#                cx=cx+cy/2
                if cx>50:
                    cx=50
                if cx<-50:
                    cx=-50
                print ('cx:=' + str(cx))
#                MotorTurnOnRide(cx,20)
#                 if(cv2.getTrackbarPos("start/stop",'frame')):
#                     conn.send(cx)
#                 else:
#                     conn.send(51)
            else:
                print("wrong line")
#             MotorTurnOnRide(cx,50)
#    else:
#         MotorTurnOnRide(cx,50)
#    conn.send(51)
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_capture.close()
        print("close")
video_capture.close()