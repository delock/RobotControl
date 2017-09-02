// Bottom half firmware
// by delock https://github.com/delock

#include <Arduino.h>
#include <Servo.h>

Servo pitchCam;   // attach your pitch servo to pin 9
#define PIT_CAM_SERVO_PIN 9
//Servo yawCam;   // I have no installed this servo yet

void initCamServo()
{
    pitchCam.attach(PITCH_CAM_SERVO_PIN);
}

void setup()
{
    initCamServo();
}
