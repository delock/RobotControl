#!/usr/bin/python3
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import _thread as thread
import time

import ncs
import camera
import telemetry
import bottom_half
import settings as st

st.connected = False

# initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

_, st.frame = cap.read()

ncs.init_ncs('googlenet')
st.compressed_frame = None
st.frame_index = 0
st.compressed_index = 0

thread.start_new_thread (camera.grab_frame, ("Capture thread", cap))
thread.start_new_thread (telemetry.compress_frame, ("Compress thread", cap))
thread.start_new_thread (ncs.inference_frame, ("Inference thread", cap))

# network stuff
HOST = ''
PORT = int(sys.argv[1])

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('Socket created')

s.bind((HOST,PORT))
print ('Socket bind complete')
s.listen(10)
print ('Socket now listening')

conn,addr = s.accept()

st.connected = True
print ('Connected from ' + str(addr))

old_time = time.time()

bottom_half.init_bottom_half()

bottom_half.cam_position(1000, 0)

try:
    local_index = 0
    while True:
        if (local_index < st.compressed_index):
            local_frame = st.compressed_frame
            local_index = st.compressed_index

            #time0 = time.time()

            data = pickle.dumps(st.compressed_frame)
            try:
                conn.sendall(struct.pack("L", len(data))+data)
                label = st.labels[st.order[0]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = st.labels[st.order[1]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = st.labels[st.order[2]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = st.labels[st.order[3]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = st.labels[st.order[4]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)

                # receieve a key from client, and show it
                command = conn.recv(2).decode("utf-8")

                if (command == "C8"):
                    bottom_half.cam_up();
                elif (command == "C2"):
                    bottom_half.cam_down();
                elif (command == "C4"):
                    bottom_half.cam_left();
                elif (command == "C6"):
                    bottom_half.cam_right();
                elif (command == "C0"):
                    bottom_half.cam_position(0, 0)
                elif (command == "C5"):
                    bottom_half.cam_position(1000, 0)
                elif (command == "W8"):
                    bottom_half.wheel_forward()
                elif (command == "W5"):
                    bottom_half.wheel_stop()
                elif (command == "W2"):
                    bottom_half.wheel_backward()
                elif (command == "W4"):
                    bottom_half.wheel_left()
                elif (command == "W6"):
                    bottom_half.wheel_right()
                elif (command == "W7"):
                    bottom_half.wheel_speed(600, 1000)
                elif (command == "W9"):
                    bottom_half.wheel_speed(1000, 600)
                elif (command == "W1"):
                    bottom_half.wheel_speed(-600, -1000)
                elif (command == "W3"):
                    bottom_half.wheel_speed(-1000, -600)

                #print (command)
            except socket.error as msg:
                st.connected = False
                print ('Connection closed')
                print ('Wait for new connection')
                conn,addr = s.accept()
                st.connected = True
                print ('Connected from ' + str(addr))
                old_time = time.time()

            #time1 = time.time()
            #print (str(local_index) + ": send data (" + str(len(data)) + " bytes) took "
            #        + str(1000*(time1 - time0)) + " ms")
        time.sleep(0.0001)

finally:
    print ("closing")
    s.close()
    ncs.close()
