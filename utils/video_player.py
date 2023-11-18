import cv2
import numpy as np
import os
import random

# Sources
source = "C:\Users\Dato\Desktop\TikTokVideo\VideoAdjuster\OutPutVideos\TikTok_55894306114.mp4"
# Instances of libraries
cap = cv2.VideoCapture(source)

while(cap.isOpened() == True):
    ret, frame = cap.read()

    if ret == True:
        cv2.imshow('Frame', frame)
        if(cv2.waitKey(25) == ord('q')):
            break
    else:
        break


cap.release()
cv2.destroyAllWindows()
