import socket
import sys
import cv2
import pickle
import struct
import numpy as np

# create connection
conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
conn.connect(('192.168.0.114',8089))

data = ""
payload_size = struct.calcsize("L") 

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
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == 27:
        cv2.destoryWindow()
        break
