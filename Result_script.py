import numpy as np
import cv2
from heapq import nlargest
from InternalLogic import MotorTurnOnRide,MotorStop,GetPositionOnMap,MotorForward,MotorTurnRight,MotorTurnLeft,GetDistance
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


def GetDist():
    Sm=0
    for i in range(3):
        Sm+=GetDistance()
    return (Sm/3)

# def motor_run(pipe):
#     while True:
#         if pipe.poll() is None:
#             continue
#         err=pipe.recv()
#         if err==51:
#             MotorStop()
#             continue
#         MotorTurnOnRide(err,25)
        
def SHP_read(se):
    while True:
        new_str = se.read_until(b'\n')        # Перебор с указанием послежней строки
        if len(new_str) > 130:                 # Функция len() возвращает длину (количество элементов) в объекте, проверка условия больше 130 символов
            q = new_str.decode('ascii')        # декодируем
            a = q.find('est')                  # Поиск подстроки в строке
            b = q.find('\r', a, len(q))        # нашли ест , передвинули каретку в начало и вернули количство декодированных элементов
            c = q[a + 4:b - 1]                 #
            d = c.split(',')  # сканирует строку,видит запятую и разделяет слова
            x = float(d[0])
            y = float(d[1])
            z = float(d[2])

            return(x,y)

        
        

# conn,conn1=Pipe()
# 
# motors=Process(target=motor_run,args=(conn1,))

# motors.start()
def go_until_right(target_x,target_y,video_capture):
    arr_error_x=0
    arr_error_y=0
    x,y=SHP_read(ser)
    while(x<target_x):
        x,y=SHP_read(ser)
        print(x,y)
    # Capture the frames
        ret, frame = video_capture.read()
    # Crop the image
        crop_img = frame[0:480, 0:640]
    # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
        canny = cv2.Canny(gray, 210, 250)      
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
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
            Kp=6.3#cv2.getTrackbarPos("Kp",'frame')/100
            target=150#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            Kp2y=0.13
            Kpy=6.3
            
            cy=y-target_y
            cy=cy*Kpy+(cy-arr_error_y)*Kp2y
            print("cy="+str(cy))
            cx=cx-target
            cx=cx*Kp+(cx-arr_error_x)*Kp2
            arr_error_x=cx
            arr_error_y=cy
            cx=cx+cy/2
            if cx>50:
                cx=50
            if cx<-50:
                cx=-50
            
            print ('cx:=' + str(cx))
#           conn.send(cx*0.3)
            MotorTurnOnRide(cx*0.6,30)
        else:
#         MotorTurnOnRide(cx,50)
            print ("I don't see the line")
            Kpy=63#cv2.getTrackbarPos("Kp",'frame')/100
        #cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2y=1.3#cv2.getTrackbarPos("Kpd",'frame')/100
            cy=y-target_y
            cy=cy*Kpy+(cy-arr_error_y)*-Kp2y
            arr_error_y=cy
            if cy>50:
                cy=50
            if cy<-50:
                cy=-50
                
            print ('cy:=' + str(cy))
            #conn.send(cy)
            MotorTurnOnRide(cx*0.7,35)
    #Display the resulting frame
        
  #  conn.send(51)

    



def go_until_left(target_x,target_y):
    arr_error_x=0
    arr_error_y=0
    x,y=SHP_read(ser)
    while(x>target_x):
        x,y=SHP_read(ser)
        print(x,y)
    # Capture the frames
        ret, frame = video_capture.read()
    # Crop the image
        crop_img = frame[0:480, 0:640]
    # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
        canny = cv2.Canny(gray, 210, 250)        
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
# Find the biggest contour (if detected)
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
            Kp=6.3#cv2.getTrackbarPos("Kp",'frame')/100
            target=450#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            Kp2y=0.13
            Kpy=6.3
            
            cy=y-target_y
            cy=cy*Kpy+(cy-arr_error_y)*Kp2y
            print("cy="+str(cy))
            cx=cx-target
            cx=cx*Kp+(cx-arr_error_x)*Kp2
            arr_error_x=cx
            arr_error_y=cy
            
            if cx>50:
                cx=50
            if cx<-50:
                cx=-50
            
            print ('cx:=' + str(cx))
#            conn.send(cx*0.3)
            MotorTurnOnRide(cx*0.6,30)
        else:
            MotorTurnOnRide(cx*0.6,30)
            print ("I don't see the line")
#            conn.send(51)
    #Display the resulting frame
        
    



def go_until_up(target_x,target_y):
    arr_error_x=0
    arr_error_y=0
    x,y=SHP_read(ser)
    while(y<target_y):
        x,y=SHP_read(ser)
        print(x,y)
    # Capture the frames
        ret, frame = video_capture.read()
    # Crop the image
        crop_img = frame[0:480, 0:640]
    # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
        canny = cv2.Canny(gray, 220, 250)        
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
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
            Kp=6.3#cv2.getTrackbarPos("Kp",'frame')/100
            target=150#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            Kp2y=0.13
            Kpy=6.3
            
            cy=y-target_y
            cy=cy*Kpy+(cy-arr_error_y)*Kp2y
            cx=cx-target
            cx=cx*Kp+(cx-arr_error_x)*Kp2
            print("cx="+str(cx))
            arr_error_x=cx
            arr_error_y=cy
            cy=cy+cx/2
            if cy>50:
                cy=50
            if cy<-50:
                cy=-50
            print ('cy:=' + str(cy))
#            conn.send(cy*0.3)
            MotorTurnOnRide(cx*0.6,30)
        else:
            MotorTurnOnRide(cx*0.6,30)
            print ("I don't see the line")
        
    #Display the resulting frame
        


def go_until_down(target_x,target_y,video_capture):
    arr_error_x=0
    arr_error_y=0
    x,y=SHP_read(ser)
    while(y>target_y):
        x,y=SHP_read(ser)
        print(x,y)
    # Capture the frames
        ret, frame = video_capture.read()
    # Crop the image
        crop_img = frame[0:480, 0:640]
    # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 220, 250)        
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
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
            Kp=5#cv2.getTrackbarPos("Kp",'frame')/100
            target=450#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            cx=cx-target
            print("cx="+str(cx))
            cx=cx*Kp+(cx-arr_error_x)*Kp2
            
            print("cx="+str(cx))
            arr_error_x=cx
            if cx>50:
                cx=50
            if cx<-50:
                cx=-50

            print ('cx:=' + str(cx))
#            conn.send(cx*0.3)
            MotorTurnOnRide(cx*0.6,30)
        else:
#            conn.send(51)
            print ("I don't see the line")
def linesStop(param):
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
            MotorForward(30)
            continue
        
        lines = lines [:,0,:]
        print("farward2")
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
            yc=int ((y1m+y2m)/2)
            cv2.line(crop_img,(0,yc),(640,yc),(255,0,0),1)                     
            cv2.line(crop_img,(x1m,y1m),(x2m,y2m),(255,0,0),1)
    #        print ('mx=' + str(mx))
            if yc<param:#240
                MotorForward(40)
                print("forward1")
            else:
                break
    else:
        MotorForward(40)
        print ("I don't see the line while stop")
def turnRight(param1,param2):
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
            MotorTurnRight(30)
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
            if tn < param1 or tn > param2:#
                MotorTurnRight(30)
            else:
                break
    #             
                
    MotorTurnRight(0)

def turnLeft(param1,param2):
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
            MotorTurnLeft(30)
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
            if tn < param1 or tn > param2:#
                MotorTurnleft(30)
            else:
                break
    #             
                
    MotorTurnLeft(0)

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
            MotorForward(speed)
            print("forward1")
                

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
#goToDist(35,30)#30
# turnRight(0.9,1.3)
# print("turnRight 0")
# print("go down untill 1")
#go_until_down(4.79,0.8,video_capture)
print("go_until_down")
# # # #linesStop(160)# проверить нужно ли остановку по линии
#goToDist(27,20)#30
print("stop 1")
# # #turnRight(0.9,1.3)
#
goToDist(10,30)
turn90left(50)
# # print("gotodist")
go_until_up(2.06,2.07,conn)
linesStop(160)
# # #print("linesStop")

# # print("turnLeft")
# go_until_up(2.06,2.07,conn)
# # print("go_until_up 7")#7
# linesStop(160)
# #print("linesStop")
turnDegRight(70,70)
# # print("turnRight")
# # #круговое движение
# # turnRight(0.9,1.3)
# # print("turnRight 8")#8
# go_until_left(0.83,2.9,conn)
# # print("go until left 9")#9
# 
# turn90Right(70)
# 
# goToDist(30,30)
# print("gotodist 9")
# 
# go_until_up(0.25,4.23,conn)
# # print("go_until_up")#10
# goToDist(30,30)
# print("gotodist 10")
# turn90Right(70)
# # #linesStop(160)
# # #print("linesStop")
# # turnRight(0.9,1.3)
# # print("turnRight")
# go_until_right(5.31,4.66,conn)
# print("end")
# # # print("go until right 11")#11
# # # goRightUntil(2.11,4.63,conn)
# # # print("goRightUntil")#12
# # # go_until_right(3.09,4.61,conn)
# # # print("go until right")#13
# # # goRightUntil(3.6,4.58,conn)
# # # print("goRightUntil 14")#14
# # go_until_right(4.4,4.57,conn)
# # print("go until right")#15
# # goToDist(30,30)
# # print("gotodist")
# # #linesStop(160)
# # #print("linesStop")
# # turnRight(0.9,1.3)
# # print("turnRight")
# # go_until_down(4.79,2.98,conn,video_capture)
# # print("go down untill 16")#16
# # linesStop(160)
# # print("stop1")
# # turnRight(0.9,1.3)
# # #проезд по линии до 17 в отдельную функцию ибо не возможна корекция по shp
# # goToDist(30,30)
# # print("gotodist 17")
# # #linesStop(160)
# # #print("stop1")
# # turnLeft(0.9,1.3)
# # print("turnLeft")
# # go_until_right(3.55,0.17,conn)
# # print("go until right 18")#18
# # #поворот налево
# # go_until_up(3.95,0.83,conn)
# # print("ура конец")#19
# 
# # go_until_right(4.3,4.85,conn,video_capture)
# # print("okokokokokokokokokokokoko")
# # go_until_down(4.89,2.75,conn,video_capture)
# # conn.send(51)
# # motors.kill()
# # ser.close()


# video_capture.close()