import numpy as np
import cv2
from collections import deque


def Values(x):
   print("")


cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,Values)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,Values)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,Values)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,Values)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,Values)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,Values)


Blue_Point   = [deque(maxlen=1024)]
Green_Point  = [deque(maxlen=1024)]
Red_Point    = [deque(maxlen=1024)]
Yellow_Point = [deque(maxlen=1024)]


Blue_Index = 0
Green_Index = 0
Red_Index = 0
Yellow_Index = 0


kernel = np.ones((5,5),np.uint8)

Colour_List = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
Color_Index = 0


Colour_Screen = np.zeros((471,636,3)) + 255
Colour_Screen = cv2.rectangle(Colour_Screen, (40,1), (140,65), (0,0,0), 2)
Colour_Screen = cv2.rectangle(Colour_Screen, (160,1), (255,65), Colour_List[0], -1)
Colour_Screen = cv2.rectangle(Colour_Screen, (275,1), (370,65), Colour_List[1], -1)
Colour_Screen = cv2.rectangle(Colour_Screen, (390,1), (485,65), Colour_List[2], -1)
Colour_Screen = cv2.rectangle(Colour_Screen, (505,1), (600,65), Colour_List[3], -1)

cv2.putText(Colour_Screen, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(Colour_Screen, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(Colour_Screen, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(Colour_Screen, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(Colour_Screen, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Colour', cv2.WINDOW_AUTOSIZE)



Click = cv2.VideoCapture(0)


while True:
    
    ret, Canvas = Click.read()
    
    Canvas = cv2.flip(Canvas, 1)
    hsv = cv2.cvtColor(Canvas, cv2.COLOR_BGR2HSV)


    Hue_Upper = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    Saturation_Upper = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    Value_Upper = cv2.getTrackbarPos("Upper Value", "Color detectors")
    Hue_Lower = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    Saturation_Lower = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    Value_Lower = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([Hue_Upper,Saturation_Upper,Value_Upper])
    Lower_hsv = np.array([Hue_Lower,Saturation_Lower,Value_Lower])


    
    Canvas = cv2.rectangle(Canvas, (40,1), (140,65), (122,122,122), -1)
    Canvas = cv2.rectangle(Canvas, (160,1), (255,65), Colour_List[0], -1)
    Canvas = cv2.rectangle(Canvas, (275,1), (370,65), Colour_List[1], -1)
    Canvas = cv2.rectangle(Canvas, (390,1), (485,65), Colour_List[2], -1)
    Canvas = cv2.rectangle(Canvas, (505,1), (600,65), Colour_List[3], -1)
    cv2.putText(Canvas, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(Canvas, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(Canvas, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(Canvas, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(Canvas, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)


    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    
    Contours,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    center = None

    
    if len(Contours) > 0:
    	
        Contour = sorted(Contours, key = cv2.contourArea, reverse = True)[0]
        
        ((x, y), radius) = cv2.minEnclosingCircle(Contour)
        
        M = cv2.moments(Contour)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

       
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear Button
                Blue_Point   = [deque(maxlen=512)]
                Green_Point  = [deque(maxlen=512)]
                Red_Point    = [deque(maxlen=512)]
                Yellow_Point = [deque(maxlen=512)]

                Blue_Index   = 0
                Green_Index  = 0
                Red_Index    = 0
                Yellow_Index = 0

                Colour_Screen[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    Color_Index = 0 # Blue
            elif 275 <= center[0] <= 370:
                    Color_Index = 1 # Green
            elif 390 <= center[0] <= 485:
                    Color_Index = 2 # Red
            elif 505 <= center[0] <= 600:
                    Color_Index = 3 # Yellow
        else :
            if Color_Index == 0:
                Blue_Point[Blue_Index].appendleft(center)
            elif Color_Index == 1:
                Green_Point[Green_Index].appendleft(center)
            elif Color_Index == 2:
                Red_Point[Red_Index].appendleft(center)
            elif Color_Index == 3:
                Yellow_Point[Yellow_Index].appendleft(center)
   
    else:
        Blue_Point.append(deque(maxlen=512))
        Blue_Index += 1
        Green_Point.append(deque(maxlen=512))
        Green_Index += 1
        Red_Point.append(deque(maxlen=512))
        Red_Index += 1
        Yellow_Point.append(deque(maxlen=512))
        Yellow_Index += 1

    
    All_point = [Blue_Point, Green_Point, Red_Point, Yellow_Point]
    for i in range(len(All_point)):
        for j in range(len(All_point[i])):
            for k in range(1, len(All_point[i][j])):
                if All_point[i][j][k - 1] is None or All_point[i][j][k] is None:
                    continue
                
                cv2.line(Colour_Screen, All_point[i][j][k - 1], All_point[i][j][k], Colour_List[i], 2)

   
    cv2.imshow("Video", Canvas)
    cv2.imshow("Canvas", Colour_Screen)
    cv2.imshow("Mask",Mask)

	
    key = cv2.waitKey(1) & 0xff
    if key==27:
        break


Click.release()
cv2.destroyAllWindows()