#!/usr/bin/python3
import sys
import cv2
import time
import telebotics

# create connection
telebotics.init(sys.argv[1], int(sys.argv[2]))

old_time = time.time()

command = "00"
while True:
    compressed_frame = telebotics.recvFrame()
    frame = cv2.imdecode(compressed_frame, 1)
    resize_frame = cv2.resize(frame, (1080,1080))
    resize_frame = cv2.copyMakeBorder(resize_frame, 0, 0, 840, 0, cv2.BORDER_CONSTANT)

    # print label
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(resize_frame,telebotics.recvString(), (10,50), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,telebotics.recvString(), (10,100), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,telebotics.recvString(), (10,150), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,telebotics.recvString(), (10,200), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,telebotics.recvString(), (10,250), font, 1,(255,255,255),2,cv2.LINE_AA)       

    telebotics.sendString(command)

    cur_time = time.time()
    fps = 1/(cur_time - old_time)
    fps = int(fps*10)/10
    cv2.putText(resize_frame, "FPS: "+str(fps), (10, 1000), font, 1, (255,255,255),2,cv2.LINE_AA)
    old_time = cur_time

    cv2.imshow('frame', resize_frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k==-1:
        command = "00"
    elif k==113:  #Q
        command = "W7"
    elif k==119:  #W
        command = "W8"
    elif k==101:  #E
        command = "W9"
    elif k==97:   #A
        command = "W4"
    elif k==115:  #S
        command = "W2"
    elif k==100:  #D
        command = "W6"
    elif k==81:   #Left key
        command = "C4"
    elif k==82:   #Up key
        command = "C8"
    elif k==83:   #Right key
        command = "C6"
    elif k==84:   #Down key
        command = "C2"
    elif k==85:   #PgUp key
        command = "C0"
    elif k==86:   #PgDn key
        command = "C5"
    elif k==49:   #1 key
        command = "L1"
    elif k==50:   #0 key
        command = "L0"
    else:
        print("key=" + str(k))
        command = "01"
