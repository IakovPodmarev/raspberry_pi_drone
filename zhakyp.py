from InternalLogic import GetDistance, GetPositionOnMap
import serial
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyACM0'
ser.open()
ser.write(b'13')
while True:
    
    ser.write(b'lep\n')# les
    ser.read_until(b'\n').decode()
    ser.read_until(b'\n').decode()
    lep_rec = ser.read_until(b'\n').decode()
    newInfo = "GetPositionOnMap:{}".format(str(lep_rec))
    logging.info("{}".format(newInfo))
    ser.write(b'\r')
    ser.close()
    print(lep_rec[:-2])