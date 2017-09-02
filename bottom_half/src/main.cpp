// Bottom half firmware
// by delock https://github.com/delock

#include <Arduino.h>
#include "cam_servo.hpp"

void setup()
{
    initCamServo();
    camTurnTo (1.0, 0.0);
    delay (1000);
    camTurnTo (0.5, 0.0);
    delay (1000);
    camTurnTo (0.0, 0.0);
    delay (1000);
    camTurnTo (-0.5, 0.0);
    delay (1000);
    camTurnTo (0.5, 0.0);
}

void loop()
{
}
