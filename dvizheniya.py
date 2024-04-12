import numpy as np
import cv2
from heapq import nlargest
from InternalLogic import *
from multiprocessing import Process 
from multiprocessing import Pipe
import serial
from serial import Serial
import time
import sys
sys.path.insert(1,'/home/piArtem/GY-85_Raspberry-Pi/i2clibraries')
from i2c_itg3205 import *




ser=serial.Serial()                            # содержимое порта сохраняется в переменную ser, затем используется в дальнейшем
ser.baudrate = 115200                 # скорость передачи данных
ser.port = '/dev/ttyACM0'                     # выбор порта передачи
ser.open()                            # отркываем файл чтобы достать содержимое
ser.write(b'\r\r')                    # Для передачи данных используется метод write. Ему нужно передавать байтовую строку:
ser.write(str.encode("les"))
print(ser.portstr)


video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 640)
video_capture.set(4, 480)
# # def motor_run(pipe):
# #     while True:
# #         if pipe.poll() is None:
# #             continue
# #         err=pipe.recv()
# #         if err==51:
# #             MotorStop()
# #             continue
# #         MotorTurnOnRide(err,25)
# conn,conn1=Pipe()
# motors=Process(target=motor_run,args=(conn1,))
# motors.start()

def go_until_right(target_x,target_y):
    arr_error_x=0
    x,y=SHP_read(ser)
    cx=0
    while(x<target_x):
        print("go_until_right")
        x,y=SHP_read(ser)
        print(x,y)
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
        canny = cv2.Canny(gray, 220, 250)      
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
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
            print ('cx:=' + str(cx))
#           conn.send(cx*0.3)
            MotorTurnOnRide(cx*0.3,15)
        else:
            MotorTurnOnRide(cx*0.1,10)
  #  conn.send(51)

def go_until_left(target_x,target_y):
    arr_error_x=0
    arr_error_y=0
    x,y=SHP_read(ser)
    while(x>target_x):
        print("go_until_left")
        x,y=SHP_read(ser)
        print(x,y)
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
        canny = cv2.Canny(gray, 220, 250)        
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
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
            print ('cx:=' + str(cx))
#            conn.send(cx*0.3)
            MotorTurnOnRide(cx*0.3,15)
        else:
            MotorTurnOnRide(cx*0.2,10)
            print ("I don't see the line")
#            conn.send(51)


def go_until_up(target_x,target_y):
    arr_error_y=0
    x,y=SHP_read(ser)
    while(y<target_y):
        print("go_until_up")
        x,y=SHP_read(ser)
        print(x,y)
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
        canny = cv2.Canny(gray, 220, 250)        
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cy = int(M['m10']/M['m00'])
            Kp=0.53#cv2.getTrackbarPos("Kp",'frame')/100
            target=420#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            cy=cy-target
            cy=cy*Kp+(cy-arr_error_y)*Kp2
            arr_error_y=cy
            if cy>50:
                cy=50
            if cy<-50:
                cy=-50
            print ('cy:=' + str(cy))
#            conn.send(cy*0.3)
            MotorTurnOnRide(cy*0.3,15)
        else:
            MotorTurnOnRide(cy*0.2,10)
            print ("I don't see the line")


def go_until_down(target_x,target_y):
    arr_error_y=0
    x,y=SHP_read(ser)
    while(y>target_y):
        print("go_until_down")
        x,y=SHP_read(ser)
        print(x,y)
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 220, 250)        
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
            Kp=0.53#cv2.getTrackbarPos("Kp",'frame')/100
            target=450#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            cx=cx-target
            cx=cx*Kp+(cx-arr_error_y)*Kp2
            arr_error_x=cx
            if cx>50:
                cx=50
            if cx<-50:
                cx=-50
            print ('cx:=' + str(cx))
#            conn.send(cy*0.3)
            MotorTurnOnRide(cx*0.3,15)
        else:
            MotorTurnOnRide(cx*0.2,10)
#            conn.send(51)
            print ("I don't see the line")

def go_one_way(target_x,target_y):
    arr_error_y=0
    x,y=SHP_read(ser)
    while(y>target_y):
        print("go_one_way")
        x,y=SHP_read(ser)
        print(x,y)
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 220, 250)        
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
            Kp=6.3#cv2.getTrackbarPos("Kp",'frame')/100
            target=450#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            cx=cx-target
            cx=cx*Kp+(cx-arr_error_y)*Kp2
            arr_error_x=cx
            if cx>50:
                cx=50
            if cx<-50:
                cx=-50
            print ('cx:=' + str(cx))
#            conn.send(cy*0.3)
            MotorTurnOnRide(cx*0.3,15)
        else:
            MotorTurnOnRide(cx*0.1,5)
#            conn.send(51)
            print ("I don't see the line")

def red_stop(param,speed):
    low_red=np.array((97,130,130), np.uint8)
    high_red=np.array((130,255,255), np.uint8)
    while True:
        MotorForward(speed)
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        hsv = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV )
        red=cv2.inRange(hsv,low_red,high_red)
        contours_red,hierarchy_red = cv2.findContours(red.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours_red) > 1:
            c = max(contours_red, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cy = int(M['m01']/M['m00'])
            if(cy>param):
                print("stop")
                MotorStop()
                break

def circle(tim,speed):
    arr_error_x=0
    start_time=time()
    while ((time()-start_time)<tim):
        print("circle time")
        print(time()-start_time)
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 220, 250)
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
            Kp=0.53#cv2.getTrackbarPos("Kp",'frame')/100
            target=440#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            cx=cx-target
            cx=cx*Kp+(cx-arr_error_x)*Kp2
            arr_error_x=cx
            if cx>50:
                cx=50
            if cx<-50:
                cx=-50
            print("cx="+str(cx))
            MotorTurnOnRide(cx*15*0.02,15)
        else:
            MotorTurnOnRide(cx*0.1,10)
            print ("I don't see the line")
    

def circle_stop(speed):
    low_red=np.array((100,130,130), np.uint8)
    high_red=np.array((130,255,255), np.uint8)
    arr_error_x=0
    while True:
        print("circle_stop")
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        hsv = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV)
        red=cv2.inRange(hsv,low_red,high_red)
        contours_red,hierarchy_red = cv2.findContours(red.copy(), 1, cv2.CHAIN_APPROX_NONE)
        gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 220, 250)
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        if len(contours_red) > 1:
            c = max(contours_red, key=cv2.contourArea)
            M1 = cv2.moments(c)
            if M1['m00'] == 0:
                continue
            cy1 = int(M1['m01']/M1['m00'])
            if(cy1>100):
                print("stop")
                MotorStop()
                break
        
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
            Kp=0.53#cv2.getTrackbarPos("Kp",'frame')/100
            target=440#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            cx=cx-target
            cx=cx*Kp+(cx-arr_error_x)*Kp2
            arr_error_x=cx
            if cx>50:
                cx=50
            if cx<-50:
                cx=-50
            print("cx="+str(cx))
            MotorTurnOnRide(cx*15*0.02,15)
        else:
            MotorTurnOnRide(cx*0.1,10)
            print ("I don't see the line")
    
    
def goDownUntil(param_x, param_y,conn):
	x,y=SHP_read(ser)
	err_x=x-param_x
	kp=-63
	while(y>param_y):
		conn.send(err_x*kp)
		x,y=SHP_read(ser)
		print(x,y)
		err_x=(x-param_x)*(-1)
		print(err_x)
		
def goUpUntil(param_x, param_y,conn):
	x,y=SHP_read(ser)
	err_x=x-param_x
	kp=63
	while(y<param_y):
		conn.send(err_x*kp)
		x,y=SHP_read(ser)
		err_x=x-param_x
		
def goRightUntil(param_x, param_y,conn):
	x,y=SHP_read(ser)
	error_y=param_y-y
	kp=63
	while(x<param_x):
		conn.send(error_y*kp)
		x,y=SHP_read(ser)
		error_y=param_y-y
def goLeftUntil(param_x,param_y,conn):
	x,y=SHP_read(ser)
	error_y=param_y-y
	kp=-63
	while(x>param_x):
		conn.send(error_y*kp)
		x,y=SHP_read(ser)
		error_y=param_y-y
		#trackcorrect()
def goToDist(param,speed):
    while GetDist()>param:
            print("goToDist")
            MotorForward(speed)
                

def turn90Right(speed):
    itg3205 = i2c_itg3205(1)
    Degre=0
    while Degre<80:
        (itgready, dataready) = itg3205.getInterruptStatus ()
        if dataready:
            (x, y, z) = itg3205.getDegPerSecAxes ()
            print ("Z:" + str (z ))
            Degre+=(z-0.2)*0.12
            print ("")
            MotorTurnLeft(speed)
        
    
def turn90left(speed):
    itg3205 = i2c_itg3205(1)
    Degre=0
    while Degre>-80:
        (itgready, dataready) = itg3205.getInterruptStatus ()
        if dataready:
            (x, y, z) = itg3205.getDegPerSecAxes ()
            print ("Z:" + str (z ))
            Degre+=(z-0.2)*0.12
            print ("")
            MotorTurnRight(speed)
def turnDegRight(deg,speed):
    itg3205 = i2c_itg3205(1)
    Degre=0
    while Degre<deg:
        (itgready, dataready) = itg3205.getInterruptStatus ()
        if dataready:
            (x, y, z) = itg3205.getDegPerSecAxes ()
            print ("Z:" + str (z ))
            Degre+=(z-0.2)*0.12
            print ("")
            MotorTurnLeft(speed)  



#from P
go_until_left(0.89,0.4)
goToDist(30,20)
turn90Right(25)
go_until_up(0.47,0.85)
red_stop(0,13)
turn90Right(25)
go_until_right(1.6,0.91)
goToDist(15,20)
turn90left(25)
go_until_up(2.06,1.85)
red_stop(0,10)
turnDegRight(55,25)
circle(3,20)
circle_stop(20)
# circle
turnDegRight(50,25)
go_until_left(0.83,2.9)
goToDist(32,20)
turn90Right(25)
#left upper corner
go_until_up(0.25,4.23)
goToDist(25,20)
turn90Right(25)
go_until_right(4.4,4.57)
#right upper corner
goToDist(100,20)
turn90Right(25)
go_until_down(4.79,2.98)
red_stop(0,10)
turn90Right(25)
# одностороннее движение
go_one_way(2.69,0.60)
goToDist(30,20)
turn90Right(25)

#финишь!!!!