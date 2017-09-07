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
from mvnc import mvncapi as mvnc

def init_ncs(network):
    global dim
    global ilsvrc_mean
    global graph
    global labels
    global device

    # get labels
    labels_file = 'words.txt'
    labels = np.loadtxt(labels_file,str,delimiter='\t')
    # configuration NCS
    mvnc.SetGlobalOption(mvnc.GlobalOption.LOGLEVEL, 2)
    devices = mvnc.EnumerateDevices()
    if len(devices) == 0:
        print('No devices found')
        quit()
    device = mvnc.Device(devices[0])
    device.OpenDevice()
    opt = device.GetDeviceOption(mvnc.DeviceOption.OPTIMISATIONLIST)

    if network == "squeezenet":
        print ("using squeezenet")
        network_blob='networks/SqueezeNet/graph'
        dim=(227,227)
    elif network=="googlenet":
        print ("using goolenet")
        network_blob='networks/GoogLeNet/graph'
        dim=(224,224)
    elif network=='alexnet':
        print ("using alexnet")
        network_blob='networks/AlexNet/graph'
        dim=(227,227)
    #Load blob
    with open(network_blob, mode='rb') as f:
        blob = f.read()
    graph = device.AllocateGraph(blob)
    graph.SetGraphOption(mvnc.GraphOption.ITERATIONS, 1)
    iterations = graph.GetGraphOption(mvnc.GraphOption.ITERATIONS)
    ilsvrc_mean = np.load('ilsvrc_2012_mean.npy').mean(1).mean(1)


def inference_frame(threadName, cap):
    global frame
    global dim
    global ilsvrc_mean
    global graph
    global labels
    global order

    while True:
        #begin = time.time()
        local_frame = frame
        img = local_frame[360:720, 360:720]
        img = cv2.resize(img, dim)
        img = img.astype(np.float32)
        img[:,:,0] = (img[:,:,0] - ilsvrc_mean[0])
        img[:,:,1] = (img[:,:,1] - ilsvrc_mean[1])
        img[:,:,2] = (img[:,:,2] - ilsvrc_mean[2])
        graph.LoadTensor(img.astype(np.float16), 'user object')
        output, userobj = graph.GetResult()
        order = output.argsort()[::-1][:6]
        #end = time.time()
        #print ("inference in " + str(end-begin) + " s")

def grab_frame(threadName, cap):
    global frame
    global frame_index
    frame_index = 0
    while True:
        #begin = time.time()
        _, cap_frame = cap.read()
        frame = cap_frame[0:1079, 420:1499]
        frame_index = frame_index + 1
        #end = time.time()
        #print ("capture frame in " + str(end-begin) + " s")

def compress_frame(threadName, cap):
    global frame
    global compressed_frame
    global frame_index
    global compressed_index
    global sleep_time
    global connected
    local_index = 0

    compressed_index = 0
    while True:
        if (connected and local_index < frame_index):
            #begin = time.time()
            local_frame = frame

            local_index = frame_index
            resize_frame = cv2.resize(local_frame, (500, 500))
            _,compressed_frame = cv2.imencode(".jpg", resize_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            compressed_index = compressed_index + 1
            #end = time.time()
            #print ("compress frame in " + str(1000*(end-begin)) + " ms")
        time.sleep(0.0001)

global frame
global compressed_frame
global frame_index
global compressed_index
global sleep_time
global graph
global device
global order
global labels
global connected

connected = False
sleep_time = 0.0001

# initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

_, frame = cap.read()

init_ncs('googlenet')
compressed_frame = None
frame_index = 0
compressed_index = 0

thread.start_new_thread (grab_frame, ("Capture thread", cap))
thread.start_new_thread (compress_frame, ("Compress thread", cap))
thread.start_new_thread (inference_frame, ("Inference thread", cap))

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

connected = True
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
    if (string == "+OK\r\n"):
        break

try:
    local_index = 0
    while True:
        if (local_index < compressed_index):
            local_frame = compressed_frame
            local_index = compressed_index

            #time0 = time.time()

            data = pickle.dumps(compressed_frame)
            try:
                conn.sendall(struct.pack("L", len(data))+data)
                label = labels[order[0]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = labels[order[1]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = labels[order[2]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = labels[order[3]]
                label = label.encode()
                conn.sendall(struct.pack("L", len(label))+label)
                label = labels[order[4]]
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
                    if (string == "+OK\r\n"):
                        break

                #print (command)
            except socket.error as msg:
                connected = False
                print ('Connection closed')
                print ('Wait for new connection')
                conn,addr = s.accept()
                connected = True
                print ('Connected from ' + str(addr))
                old_time = time.time()

            #time1 = time.time()
            #print (str(local_index) + ": send data (" + str(len(data)) + " bytes) took "
            #        + str(1000*(time1 - time0)) + " ms")
        time.sleep(0.0001)

finally:
    print ("closing")
    s.close()
    graph.DeallocateGraph()
    device.CloseDevice()
