import cv2
from InternalLogic import MotorTurnOnRide, MotorTurnRight, MotorTurnLeft, MotorStop
import numpy as np

video_capture = cv2.VideoCapture(-1)
video_capture.set(3,640)
video_capture.set(4, 480)

# def nothing(g):
#     print(g)
#     return(g)

# cv2.namedWindow("frame")
# cv2.createTrackbar("low_h",'frame',0,360,nothing)
# cv2.createTrackbar("high_h",'frame',0,360,nothing)
# cv2.createTrackbar("low_s",'frame',0,100,nothing)
# cv2.createTrackbar("high_s",'frame',0,100,nothing)
# cv2.createTrackbar("low_v",'frame',0,100,nothing)
# cv2.createTrackbar("high_v",'frame',0,100,nothing)

# low_h=90#cv2.getTrackbarPos("low_h",'frame')#0
# high_h=130#cv2.getTrackbarPos("high_h",'frame')#15
# low_s=130#cv2.getTrackbarPos("low_s",'frame')#75
# high_s=255#cv2.getTrackbarPos("high_s",'frame')#100
# low_v=130#cv2.getTrackbarPos("low_v",'frame')#75
# high_v=255#cv2.getTrackbarPos("high_v",'frame')#100
# low_red=np.array((low_h,low_s,low_v), np.uint8)
# high_red=np.array((high_h,high_s,high_v), np.uint8)


while True:

    arr_error_x=0
    ret, frame = video_capture.read()
    crop_img = frame[0:480, 0:640]
    
    
#     hsv = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV )
#     red=cv2.inRange(hsv,low_red,high_red)
#     contours_red,hierarchy_red = cv2.findContours(red.copy(), 1, cv2.CHAIN_APPROX_NONE)
    
    
    gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 220, 255)
    contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
#     if len(contours_red) > 1:
#         c = max(contours_red, key=cv2.contourArea)
#         M = cv2.moments(c)
#         if M['m00'] == 0:
#             continue
#         cx = int(M['m10']/M['m00'])
#         cy = int(M['m01']/M['m00'])
# #         print(cy)
#         cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
#         cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
#         cv2.drawContours(crop_img, contours_red, -1, (0,200,100), 1)
#         if(cy>100):
#             print("stop")
# #             MotorStop()
# #             break
    if len(contours) > 1:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M['m00'] == 0:
            continue
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1) 
        Kp=0.53#cv2.getTrackbarPos("Kp",'frame')/100
        target=420#cv2.getTrackbarPos("Target_posiiton",'frame')
        Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
        cx=cx-target
        cx=cx*Kp+(cx-arr_error_x)*Kp2
        arr_error_x=cx
        if cx>50:
            cx=50
        if cx<-50:
            cx=-50
        print("cx="+str(cx))
        MotorTurnOnRide(cx*0.3,15)
    else:
       MotorTurnOnRide(cx*0.2,10)
       print ("I don't see the line")
        
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break