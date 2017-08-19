import socket
import sys
import cv2
import pickle
import struct
import numpy as np
import time

# create connection
conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
conn.connect(('192.168.0.114',8086))

old_time = time.time()
data = ''.encode('utf-8')
payload_size = struct.calcsize("L")

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

    conn.send("B".encode('utf-8'))

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
    cur_time = time.time()
    fps = 1/(cur_time - old_time)
    #print ("fps = " + str(fps))
    old_time = cur_time
