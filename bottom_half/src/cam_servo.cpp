#include <Servo.h>
#include "cam_servo.hpp"

Servo pitchCam; // attach your pitch servo to pin 9
Servo yawCam;   // I have not installed this servo yet
#define PITCH_CAM_SERVO_PIN 9

#define START 20
#define UPRIGHT 105
#define FORWARD 45
#define END 165

void initCamServo(void)
{
    pitchCam.attach(PITCH_CAM_SERVO_PIN);
}

// pitch -- 0: upright, 0.5: right forward, 1.0: max down angle, -0.5: max backward angle
// yaw   -- 0: to the front, 1.0: to the right, -1.0: to the left
void camTurnTo(float pitch, float yaw)
{
    int pitchVal;

    // pitch is within [-1, 1]
    if (pitch > 1.0) pitch = 1.0;
    if (pitch <-0.5) pitch = -0.5;

    if (pitch >= 0 && pitch <= 0.5) {
        pitchVal = UPRIGHT - pitch * 2 * (UPRIGHT - FORWARD);
    } else if (pitch >= 0.5) {
        pitchVal = FORWARD - (pitch-0.5) * 2 * (FORWARD- START);
    } else { // pitch <0
        pitchVal = UPRIGHT + (UPRIGHT - END) * pitch*2;
    }

    pitchCam.write(pitchVal);
}
