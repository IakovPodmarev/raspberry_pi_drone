def go_down_until(target_x,target_y,conn):
    arr_error_x=0
    arr_error_y=0
    x,y=SHP_read(ser)
    def nothing(g):
        print(g)
        return(g)

    cv2.namedWindow("frame")
    cv2.createTrackbar("param1",'frame',0,200,nothing)
    cv2.createTrackbar("param2",'frame',0,200,nothing)
    cv2.createTrackbar("start/stop",'frame',0,1,nothing)
    cv2.createTrackbar("Kp",'frame',0,100,nothing)
    cv2.createTrackbar("Target_posiiton",'frame',0,640,nothing)
    cv2.createTrackbar("start/stop",'frame',0,1,nothing)
    cv2.createTrackbar("Kpd",'frame',0,100,nothing)
    
    
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
        lines = cv2.HoughLinesP(canny, 1, np.pi/180, 30, minLineLength=60, maxLineGap=10)
        if lines is None:
            MotorTurnRight(30)
            continue
        
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
            tn=(x1m-x2m)/(y1m-y2m)
            print (tn)   
            param1=cv2.getTrackbarPos("param1",'frame')/10
            param2=cv2.getTrackbarPos("param2",'frame')/10
            if tn < param1 or tn > param2:   
                Kp=cv2.getTrackbarPos("Kp",'frame')/100
                target=cv2.getTrackbarPos("Target_posiiton",'frame')  
                Kpd=cv2.getTrackbarPos("Kpd",'frame')/100
#                Kp=6.3
#                target=150
#               Kp2=0.13
##                Kp2y=0.13
##                Kpy=6.3
                cv2.line(crop_img,(x1m,y1m),(x2m,y2m),(255,0,0),4)            
# #               cy=y-target_y
# #               cy=cy*-Kpy+(cy-arr_error_y)*-Kp2y
##                print("cy="+str(cy))
                cx=cx-target
                cx=tn*-Kp+(tn-arr_error_x)*-Kpd
                arr_error_x=cx
#     #          arr_error_y=cy
                cx=cx+cy/2
                if cx>50:
                    cx=50
                if cx<-50:
                    cx=-50
                print ('cx:=' + str(cx))
                conn.send(cx)
            else:
                    continue
#             MotorTurnOnRide(cx,50)
        else:
#         MotorTurnOnRide(cx,50)
            print ("I don't see the line")
        
        
        cv2.imshow('frame',crop_img)
    #Display the resulting frame
        
    conn.send(51)