#!/usr/bin/python3
import time
import serial
import settings as st
import _thread as thread

def init():
    global ser
    global command_list

    ser = serial.Serial('/dev/ttyACM0', 115200)

    command_list = []
    thread.start_new_thread(send_command_thread, ("Bottom half thread", (0)))

    cam_position(1000, 0)

def send_command_thread(threadName, arg):
    global ser

    try:
        while True:
            send_next_command()
            time.sleep(0.01)
    finally:
        close()

def send_next_command():
    global command_list
    if (len(command_list) > 0):
        command = command_list[0]
        send_command(command)
        command_list.remove(command)
        return True
    else:
        send_command("nop")
        return False

def send_command(command):
    ser.write(bytes(command+"\n", "utf-8"))
    while True:
        val = ser.readline()
        string = val.decode("utf-8")
        if (string.startswith("+OK")):
            print (string)
            break

def cam_position(pitch, yaw):
    global cam_pitch
    global cam_yaw

    command_list.append("campos "
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
    command_list.append("wheel " + str(l_speed) + " " + str(r_speed));

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
        command_list.append("light 1")
    else:
        command_list.append("light 0")

def close():
    global ser
    ser.close()
