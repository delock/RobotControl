// Bottom half firmware
// by delock https://github.com/delock

#include <Arduino.h>
#include <Wire.h>
#include "cam_servo.h"
#include "wheel.h"
#include "10dof.h"

void setup()
{
    Serial.begin (9600);
    Wire.begin();

    initSensors();

    initCamServo();
    camTurnTo (1.0, 0.0);

    initWheel();
    //setKeepTime(1.0);
    while (!Serial);
}

void processCommand (String command)
{
    if (command.startsWith("echo ")) {
        Serial.println(command);
    } else if (command.startsWith("campos ")) {
        float pitch, yaw;

        String pitchStr = command.substring(7);
        int index = pitchStr.indexOf(' ');
        String yawStr = pitchStr.substring(index+1);

        pitch = pitchStr.toInt()/1000.0;
        yaw   = yawStr.toInt()/1000.0;

        Serial.print("set camera pos: ");
        Serial.print(pitch);
        Serial.print(" , ");
        Serial.println(yaw);
        camTurnTo(pitch, yaw);
    } else if (command.startsWith("wheel ")) {
        float left, right;

        String leftStr = command.substring(6);
        int index = leftStr.indexOf(' ');
        String rightStr = leftStr.substring(index+1);

        left = leftStr.toInt()/1000.0;
        right = rightStr.toInt()/1000.0;

        Serial.print("set wheel speed: ");
        Serial.print(left);
        Serial.print(" , ");
        Serial.println(right);
        setSpeed(left, right);
    }
}

void loop()
{
    float sensors[3][3];

    getSensors(sensors);

    String val;
    #if 1
    if (Serial.available()) {
        val = Serial.readStringUntil('\n');
        processCommand(val);
        Serial.print("+OK ");
        Serial.print(sensors[0][0]);
        Serial.print(" ");
        Serial.print(sensors[0][1]);
        Serial.print(" ");
        Serial.print(sensors[0][2]);
        Serial.print(" ");
        Serial.print(sensors[1][0]);
        Serial.print(" ");
        Serial.print(sensors[1][1]);
        Serial.print(" ");
        Serial.print(sensors[1][2]);
        Serial.print(" ");
        Serial.print(sensors[2][0]);
        Serial.print(" ");
        Serial.print(sensors[2][1]);
        Serial.print(" ");
        Serial.print(sensors[2][2]);
        Serial.println("");
    }
    #endif
    wheelLoop();
    //delay (1);
}
