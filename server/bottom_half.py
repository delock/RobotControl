#!/usr/bin/python3
import time
import serial
import settings as st

def init():
    global ser

    ser = serial.Serial('/dev/ttyACM0', 115200)
    cam_position(1000, 0)

def send_command(command):
    global ser
    ser.write(bytes(command+"\n", "utf-8"))
    while True:
        val = ser.readline()
        string = val.decode("utf-8")
        #print (string)
        if (string.startswith("+OK")):
            print (string)
            break

def cam_position(pitch, yaw):
    global cam_pitch
    global cam_yaw

    send_command("campos "
                        + str(pitch) + " "
                        + str(yaw))
    cam_pitch = pitch
    cam_yaw   = yaw

def cam_up(delta = 100):
    global cam_pitch
    global cam_yaw

    cam_pitch = cam_pitch - delta
    if (cam_pitch < -1000):
        cam_pitch = -1000
    cam_position(cam_pitch, cam_yaw)

def cam_down(delta = 100):
    global cam_pitch
    global cam_yaw

    cam_pitch = cam_pitch + delta
    if (cam_pitch > 1400):
        cam_pitch = 1400
    cam_position(cam_pitch, cam_yaw)

def cam_left(delta = 100):
    global cam_pitch
    global cam_yaw

    cam_yaw = cam_yaw - delta
    if (cam_yaw < -1200):
        cam_yaw = -1200
    cam_position(cam_pitch, cam_yaw)

def cam_right(delta = 100):
    global cam_pitch
    global cam_yaw

    cam_yaw = cam_yaw + delta
    if (cam_yaw > 1200):
        cam_yaw = 1200
    cam_position(cam_pitch, cam_yaw)

def wheel_speed (l_speed, r_speed):
    send_command("wheel " + str(l_speed) + " " + str(r_speed));

def wheel_forward(speed = 1000):
    wheel_speed (speed, speed)

def wheel_backward(speed = 1000):
    wheel_speed (-speed, -speed)

def wheel_left(speed = 1000):
    wheel_speed (-speed, speed)

def wheel_right(speed = 1000):
    wheel_speed (speed, -speed)

def wheel_stop():
    wheel_speed (0, 0);

def light(on):
    if (on):
        send_command("light 1")
    else:
        send_command("light 0")

def nop():
    send_command("nop ")

def close():
    global ser
    ser.close()
