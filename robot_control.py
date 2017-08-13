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

data = ""
payload_size = struct.calcsize("L")

old_time = time.time()
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    compressed_frame = pickle.loads(frame_data)
    frame = cv2.imdecode(compressed_frame, 1)
    #big_frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == 27:
        cv2.destoryWindow()
        break
    cur_time = time.time()
    fps = 1/(cur_time - old_time)
    print ("fps = " + str(fps))
    old_time = cur_time
