def circle(conn):
    arr_error_x=0
    low_red=(17,50,110)
    high_red=(101,140,180)
    while(x>target_x):
        
        
    # Capture the frames
        ret, frame = video_capture.read()
        crop_img = frame[0:480, 0:640]
        red=cv2.inRange(crop_img,low_red,high_red)
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 210, 250)
        canny_red = cv2.Canny(red, 210, 250)
        contours,hierarchy = cv2.findContours(canny.copy(), 1, cv2.CHAIN_APPROX_NONE)
        contours_red,hierarchy_red = cv2.findContours(canny_red.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours_red) > 1:
            c = max(contours_red, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if(cy>160):
                MotorsStop()
                break
        if len(contours) > 1:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            Kp=6.3#cv2.getTrackbarPos("Kp",'frame')/100
            target=150#cv2.getTrackbarPos("Target_posiiton",'frame')
            Kp2=0.13#cv2.getTrackbarPos("Kpd",'frame')/100
            cx=cx-target
            cx=cx*-Kp+(cx-arr_error_x)*-Kp2
            print("cx="+str(cx))
            
            if cy>50:
				MotorTurnRight()
				#motorkill
				continue
            if cy<-50:
				MotorTurnLeft()
				#motorkill
				continue
            print ('cy:=' + str(cy))
            
            MotorTurnOnRide(cx,50)
        else:     
             MotorTurnOnRide(cx,50)
             print ("I don't see the line")
        
   
        