#!/usr/bin/python3
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import _thread as thread
import time
import serial

import ncs
import camera
import telemetry
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

ser = serial.Serial('/dev/ttyACM0', 9600)

cam_pitch = 1000
cam_yaw = 0
ser.write(bytes("campos 1000 0\n", "utf-8"))
while True:
    val = ser.readline()
    string = val.decode("utf-8")
    #print (string)
    if (string.startswith("+OK")):
        print (string)
        break

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

                wait_serial = False
                if (command == "C8"):
                    cam_pitch = cam_pitch - 100
                    if(cam_pitch < -1000):
                        cam_pitch = -1000
                    ser.write(bytes("campos "+str(cam_pitch)+" "+str(cam_yaw)+"\n", "utf-8"))
                    wait_serial = True
                elif (command == "C2"):
                    cam_pitch = cam_pitch + 100
                    if(cam_pitch > 1400):
                        cam_pitch = 1400
                    ser.write(bytes("campos "+str(cam_pitch)+" "+str(cam_yaw)+"\n", "utf-8"))
                    wait_serial = True
                elif (command == "C4"):
                    cam_yaw = cam_yaw - 100
                    if(cam_yaw < -1200):
                        cam_yaw = -1200
                    ser.write(bytes("campos "+str(cam_pitch)+" "+str(cam_yaw)+"\n", "utf-8"))
                    wait_serial = True
                elif (command == "C6"):
                    cam_yaw = cam_yaw + 100
                    if(cam_yaw > 1200):
                        cam_yaw = 1200
                    ser.write(bytes("campos "+str(cam_pitch)+" "+str(cam_yaw)+"\n", "utf-8"))
                    wait_serial = True
                elif (command == "C0"):
                    cam_yaw = 0
                    cam_pitch = 0
                    ser.write(bytes("campos "+str(cam_pitch)+" "+str(cam_yaw)+"\n", "utf-8"))
                    wait_serial = True
                elif (command == "C5"):
                    cam_yaw = 0
                    cam_pitch = 1000
                    ser.write(bytes("campos "+str(cam_pitch)+" "+str(cam_yaw)+"\n", "utf-8"))
                    wait_serial = True
                elif (command == "W8"):
                    ser.write(bytes("wheel 800 800\n", "utf-8"))
                    wait_serial = True
                elif (command == "W5"):
                    ser.write(bytes("wheel 0 0\n", "utf-8"))
                    wait_serial = True
                elif (command == "W2"):
                    ser.write(bytes("wheel -800 -800\n", "utf-8"))
                    wait_serial = True
                elif (command == "W4"):
                    ser.write(bytes("wheel -800 800\n", "utf-8"))
                    wait_serial = True
                elif (command == "W6"):
                    ser.write(bytes("wheel 800 -800\n", "utf-8"))
                    wait_serial = True
                elif (command == "W7"):
                    ser.write(bytes("wheel 600 1000\n", "utf-8"))
                    wait_serial = True
                elif (command == "W9"):
                    ser.write(bytes("wheel 1000 600\n", "utf-8"))
                    wait_serial = True
                elif (command == "W1"):
                    ser.write(bytes("wheel -600 -1000\n", "utf-8"))
                    wait_serial = True
                elif (command == "W3"):
                    ser.write(bytes("wheel -1000 -600\n", "utf-8"))
                    wait_serial = True

                while wait_serial:
                    val = ser.readline()
                    string = val.decode("utf-8")
                    #print (string)
                    if (string.startswith("+OK")):
                        print (string)
                        break

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
