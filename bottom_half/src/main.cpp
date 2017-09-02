// Bottom half firmware
// by delock https://github.com/delock

#include <Arduino.h>
#include "cam_servo.h"
#include "wheel.h"

void setup()
{
    Serial.begin (9600);

    initCamServo();
    camTurnTo (0.0, 0.0);
    delay (1000);
    camTurnTo (0.5, 0.0);

    initWheel();
    setKeepTime(1.0);
    while (!Serial);
}

void processCommand (String command)
{
    if (command.startsWith("campos ")) {
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
    String val;
    #if 1
    if (Serial.available()) {
        val = Serial.readString();
        processCommand(val);
        Serial.println("+OK");
    }
    #endif
    wheelLoop();
    delay (1);
}
