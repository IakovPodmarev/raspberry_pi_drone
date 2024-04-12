import RPi.GPIO as GPIO
import time
import logging
import cv2
import datetime
import os
import serial


logPath = "{}".format(datetime.datetime.now())
os.mkdir(logPath)
logging.basicConfig(filename="{}/logs.log".format(logPath), level=logging.DEBUG)
logging.info("Python start new logging")
GPIO.setwarnings(False)


def ClearPins():
    GPIO.cleanup()
    exit()
    return


def GetPositionOnMap():
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = '/dev/ttyACM0'
    ser.open()
    ser.write(b'lep\n')# les
    ser.read_until(b'\n').decode()
    ser.read_until(b'\n').decode()
    lep_rec = ser.read_until(b'\n').decode()
    print(type(lep_rec))
    newInfo = "GetPositionOnMap:{}".format(str(lep_rec))
    logging.info("{}".format(newInfo))
    ser.write(b'\r')
    ser.close()
    return lep_rec[:-2]


def GetImage():
    '''
        Return picture from video camer
    '''
    cam = cv2.VideoCapture(0)
    ret, image = cam.read()
    cam.release()
    cv2.imwrite('{}/{}.png'.format(logPath, datetime.datetime.now()), image)
    logging.info("GetImage:Сamera photo get")
    return image


def GetDistance():
    '''
        Determine the distance to the nearest obstacle in centimeters. Return distance and error.
        If everything is OK: distance, "OK"
        If the response waiting time is exceeded: 0, "Timeout"
        If the distance exceeds 3 meters or is equal to 0: distance, "Out of reach"
    '''

    StartTime = time.time()
    StopTime = time.time()
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
    pulseDuration = (StopTime - StartTime)
    distance = pulseDuration * 17000;
    if pulseDuration >= 0.01746:
        logging.error("GetDistance:Time out")
        return 0, 'Time out'
    elif distance > 300 or distance == 0:
        logging.error("GetDistance:Out of range")
        return distance, 'Out of range'
    print("Distance = {} cm.".format(round(distance, 3)))

    logging.info("GetDistance:Distance = {} cm.".format(round(distance, 3)))

    return distance, 'Ok'


def MoveCameraVertical(angle):
    '''
        Rotate the camera vertically by a certain angle in the range [60, 120],
        where 60 is the lowest camera position, 120 is the highest.
        The function returns the photo from the position to which the rotation led.
        If the angle is not a number, no rotation will occur.
    '''
    try:
        angle = int(angle)
        if angle >= 60 and angle <= 120:
            pwm = GPIO.PWM(IR_R, 50)
            pwm.start(7.5)
            pwm.ChangeDutyCycle(angle / 18. + 3.)
            time.sleep(0.2)
            pwm.stop()
    except:
        print("Not number")

    image = GetImage()

    logging.info("MoveCameraVertical:Angle vertically  = {} deg".format(round(angle, 3)))

    return image


def MoveCameraHorizontal(angle):
    '''
        Rotate the camera horizontally by a certain angle in the range [35, 145],
        where 60 is the lowest camera position, 120 is the highest.
        The function returns the photo from the position to which the rotation led.
        If the angle is not a number, no rotation will occur.
    '''
    try:
        angle = int(angle)
        if angle >= 35 and angle <= 145:
            pwm = GPIO.PWM(IR_L, 50)
            pwm.start(7.5)
            pwm.ChangeDutyCycle(angle / 18. + 3.)
            time.sleep(0.2)
            pwm.stop()
    except:
        print("Not number")

    image = GetImage()

    logging.info("MoveCameraHorizontal:Angle horizontally = {} deg".format(round(angle, 3)))

    return image

log_param_Forw=0
def MotorForward(param):
    '''
        The car is going forward.
        The movement will continue until another motion function or the MotorStop() function is called.
    '''
    pwmA = GPIO.PWM(ENA, 100)
    pwmB = GPIO.PWM(ENB, 100)
    

    print('motor forward')
    if(param==0):
        
        GPIO.output(IN1, False)    
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)
        pwmA.stop()
        pwmB.stop()
    else:
        
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)
        pwmA.start(param)
        pwmB.start(param)
        pwmB.ChangeDutyCycle(param)
        time.sleep(0.2)
    logging.info("MotorForward:motor forward")


def MotorBackward():
    '''
        The car is going forward.
         The movement will continue until another motion function or the MotorStop() function is called.
    '''
    print('motor backward')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    logging.info("MotorBackward:motor backward")


def MotorTurnOnRide(param, speed):
    pwmA = GPIO.PWM(ENA, 100)
    pwmB = GPIO.PWM(ENB, 100)
    i_p=speed-param
    i_pp=speed+param
    if(i_p<0 or i_p>100):
        i_p=0
    if(i_pp>100 or i_pp<0):
        i_pp=100

    if(speed==0):
        pwmA.stop()
        pwmB.stop()
        time.sleep(0.2)
    else:
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)
        pwmA.start(i_p)
        pwmB.start(i_pp)
        time.sleep(0.2)
        
    
        
def MotorTurnRight():
    '''
        The car turns right. The turn will continue until another motion function or the MotorStop() function is called.
    '''
    print('motor turnright')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    logging.info("MotorTurnRight:motor turnright")


def MotorTurnLeft():
    '''
        The car turns left. The turn will continue until another motion function or the MotorStop() function is called.
    '''
    print('motor turnleft')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    logging.info("MotorTurnLeft:motor turnleft")


def MotorStop():
    '''
        The car stops. The car will continue to stand until another movement is called.
    '''
    print('motor stop')
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
    logging.info("MotorStop:motor stop")


# Set the type of GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

######## Motor drive interface definition ##############################################################################
ENA = 13  # //L298 Enable A
ENB = 20  # //L298 Enable B
IN1 = 19  # //Motor interface 1
IN2 = 16  # //Motor interface 2
IN3 = 21  # //Motor interface 3
IN4 = 26  # //Motor interface 4
######## Infrared sensor interface definition ##########################################################################

IR_R = 18  # Rotate the camera vertically
IR_L = 27  # Rotate the camera horizontally

# IRF_R = 24    # Follow line right infrared sensor
# IRF_L = 23    # Follow line left infrared sensor

ECHO = 4  # Sensor distance
TRIG = 17  # Sensor distance

######### Motor initialized to LOW #####################################################################################
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

######### INFRARED SENSOR  #############################################################################################
######### Infrared initialized to input,and internal pull up ###########################################################
# GPIO.setup(IRF_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(IRF_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)

######### SERVOS SENSOR  ###############################################################################################
GPIO.setup(IR_R, GPIO.OUT)
GPIO.setup(IR_L, GPIO.OUT)

######### DISTANCE SENSOR  ###############################################################################################

GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

########################################################################################################################

angle_h = 90
angle_v = 70

pwm = GPIO.PWM(IR_R, 50)
pwm.start(7.5)
time.sleep(0.2)
pwm.stop()

pwm = GPIO.PWM(IR_L, 50)
pwm.start(7.5)
time.sleep(0.2)
pwm.stop()
######### Infrared initialized to input,and internal pull up #########