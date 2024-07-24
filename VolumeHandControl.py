import cv2
import mediapipe as mp
import time 
import math
import numpy as np
import HandTrakingModule as htm


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


pTime = 0
cTime = 0
cap = cv2.VideoCapture(1)
detector = htm.handDetector()




devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

volBar=400
volPer=0







while True:
    success , img = cap.read()
    img = detector.findHands(img)
    lmsList = detector.findPosition(img , draw=False)
    if len(lmsList) !=0:
        x1, y1 = lmsList[4][1] , lmsList[4][2]
        x2, y2 = lmsList[8][1] , lmsList[8][2]

        cx , xy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img , (x1,y1) ,  8 , (255,0,255) , cv2.FILLED)
        cv2.circle(img , (x2,y2) ,  8 , (255,0,255) , cv2.FILLED)
        cv2.line(img , (x1,y1) , (x2,y2) , (255,255,0) , 3)
        cv2.circle(img , (cx,xy) ,  8 , (255,0,255) , cv2.FILLED)

        length = math.hypot(x2-x1 , y2-y1)
        # print(length)

        #range of hand distance iss 50 - 300
        # volume range -65 - 0
        vol = np.interp(length , [50,300] , [minVol , maxVol])
        volBar = np.interp(length , [50,300] , [400 , 150])
        volPer = np.interp(length , [50,300] , [0 , 100])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)

        if length<50:
            cv2.circle(img , (cx,xy) ,  8 , (0,255,0) , cv2.FILLED)

    cv2.rectangle(img, (50,150) , (85,400) ,(0,255,0) , 3)
    cv2.rectangle(img, (50,int(volBar)) , (85,400) ,(0,255,0) , cv2.FILLED)
    cv2.putText(img, f'{(int(volPer))} %' , (35, 450) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0,255,0) , 2)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {(int(fps))}' , (10, 70) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,0,255) , 2)

    cv2.imshow("image" , img)
    cv2.waitKey(1)