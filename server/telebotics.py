#!/usr/bin/python3
import cv2
import socket
import pickle
import struct
import time
import _thread as thread
import settings as st

global index

def init(host, port):
    global s
    global compressed_frame
    global connected
    global index

    compressed_frame = None
    index = 0
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1) # only allow one connection
    connected = False
    print ('Socket now listening')

    thread.start_new_thread (compress_frame, ("Compress thread", (0)))

def accept_connection():
    global s
    global conn
    global connected

    conn, addr = s.accept()
    connected = True
    print ('Connected from ' + str(addr))

def disconnected():
    global connected

    connected = False

def send_frame():
    global conn
    global compressed_frame

    data = pickle.dumps(compressed_frame)
    conn.sendall(struct.pack("L", len(data)) + data)

def send_string(string):
    global conn
    data = string.encode()
    conn.sendall(struct.pack("L", len(data)) + data)

def recv_command(length=2):
    global conn
    command = conn.recv(length).decode("utf-8")
    return command

def compress_frame(threadName, arg):
    global compressed_frame
    global connected
    global index

    local_index = 0

    index = 0
    try:
        while True:
            if (connected and local_index < st.frame_index):
                #begin = time.time()
                local_frame = st.frame

                local_index = st.frame_index
                resize_frame = cv2.resize(local_frame, (500, 500))
                _,compressed_frame = cv2.imencode(".jpg", resize_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
                index = index + 1
                #end = time.time()
                #print ("compress frame in " + str(1000*(end-begin)) + " ms")
            time.sleep(0.0001)
    finally:
        close()

def close():
    global s

    s.close()
