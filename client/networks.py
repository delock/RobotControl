import socket
import pickle
import struct

def init(addr, port):
    global conn
    global data
    global payload_size

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((addr, port))
    data = ''.encode('utf-8')
    payload_size = struct.calcsize("L")

def recv_data():
    global conn
    global data
    global payload_size

    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    ret_data = data[:msg_size]
    data = data[msg_size:]
    return ret_data

def recvFrame():
    ret_data = recv_data()
    return pickle.loads(ret_data)

def recvString():
    ret_data = recv_data()
    return ret_data.decode()

def sendString(string):
    global conn
    conn.send(string.encode('utf-8'))
