def circle(target_x1, target_y2,target_x2,target_y2,conn):
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
            target=150#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            Kp2y=0.13
            Kpy=6.3
            
            cy=y-target_y
            cy=cy*-Kpy+(cy-arr_error_y)*-Kp2y
            cx=cx-target
            cx=cx*-Kp+(cx-arr_error_x)*-Kp2
            print("cx="+str(cx))
            arr_error_x=cx
            arr_error_y=cy
            cy=cy+cx/2
            if cy>50:
				MotorTurnRight()
				#motorkill
				continue
            if cy<-50:
				MotorTurnLeft()
				#motorkill
				continue
            print ('cy:=' + str(cy))
            conn.send(cy)
#             MotorTurnOnRide(cx,50)
        else:
#         MotorTurnOnRide(cx,50)
            print ("I don't see the line")
        
    #Display the resulting frame
        
    conn.send(51)