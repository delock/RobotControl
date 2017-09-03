#!/usr/bin/python3
import socket
import sys
import cv2
import pickle
import struct
import numpy as np
import time

# create connection
conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
conn.connect(('192.168.0.114',8087))

old_time = time.time()
data = ''.encode('utf-8')
payload_size = struct.calcsize("L")

command = "00"
while True:
    # receieve image
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # receieve annotation
    # label 0
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    label0 = data[:msg_size]
    data = data[msg_size:]

    # label 1
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    label1 = data[:msg_size]
    data = data[msg_size:]

    # label 2
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    label2 = data[:msg_size]
    data = data[msg_size:]

    # label 3
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    label3 = data[:msg_size]
    data = data[msg_size:]

    # label 4
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    label4 = data[:msg_size]
    data = data[msg_size:]

    conn.send(command.encode('utf-8'))

    compressed_frame = pickle.loads(frame_data)
    frame = cv2.imdecode(compressed_frame, 1)
    resize_frame = cv2.resize(frame, (1080,1080))
    resize_frame = cv2.copyMakeBorder(resize_frame, 0, 0, 840, 0, cv2.BORDER_CONSTANT)

    # print label
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(resize_frame,label0.decode(), (10,50), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,label1.decode(), (10,100), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,label2.decode(), (10,150), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,label3.decode(), (10,200), font, 1,(255,255,255),2,cv2.LINE_AA)       
    cv2.putText(resize_frame,label4.decode(), (10,250), font, 1,(255,255,255),2,cv2.LINE_AA)       

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
        command = "W5"
    elif k==100:  #D
        command = "W6"
    elif k==122:  #Z
        command = "W1"
    elif k==120:  #X
        command = "W2"
    elif k==99:   #C
        command = "W3"
    elif k==81:   #Left key
        command = "C4"
    elif k==82:   #Up key
        command = "C8"
    elif k==83:   #Right key
        command = "C6"
    elif k==84:   #Right key
        command = "C2"
    else:
        print("key=" + str(k))
        command = "01"
    cur_time = time.time()
    #fps = 1/(cur_time - old_time)
    #print ("fps = " + str(fps))
    old_time = cur_time
