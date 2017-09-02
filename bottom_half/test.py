import serial
import sys

print ("command is \"" + sys.argv[1] + "\"")

ser = serial.Serial('/dev/ttyACM0', 9600)

ser.write(bytes(sys.argv[1], "utf-8"))
val = ser.readline()
string = val.decode("utf-8");
print (string)

while (string != "+OK\r\n"):
    val = ser.readline()
    string = val.decode("utf-8");
    print (string)

ser.write(bytes(sys.argv[1], "utf-8"))
val = ser.readline()
string = val.decode("utf-8");
print (string)

while (string != "+OK\r\n"):
    val = ser.readline()
    string = val.decode("utf-8");
    print (string)
