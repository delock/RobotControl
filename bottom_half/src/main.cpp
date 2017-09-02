// Bottom half firmware
// by delock https://github.com/delock

#include <Arduino.h>
#include "cam_servo.hpp"

void setup()
{
    Serial.begin (9600);

    initCamServo();
    camTurnTo (0.0, 0.0);
    delay (1000);
    camTurnTo (0.5, 0.0);
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
    delay (1000);
}
