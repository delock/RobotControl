import serial
import sys
import time

print ("command is \"" + sys.argv[1] + "\"")

ser = serial.Serial('/dev/ttyACM0', 9600)


ser.write(bytes(sys.argv[1]+"\n", "utf-8"))
while True:
    val = ser.readline()
    string = val.decode("utf-8");
    print (string)
    if (string == "+OK\r\n"):
        break

