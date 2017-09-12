#include <Servo.h>
#include "cam_servo.h"
#include <Arduino.h>

Servo pitch_cam; // attach your pitch servo to pin 9
Servo yaw_cam;   // I have not installed this servo yet
#define YAW_CAM_SERVO_PIN 8
#define PITCH_CAM_SERVO_PIN 9

#define PITCH_START 20
#define PITCH_UPRIGHT 105
#define PITCH_FORWARD 45
#define PITCH_END 165
#define PITCH_LIMIT (PITCH_UPRIGHT-PITCH_START)*1.0/(PITCH_UPRIGHT-PITCH_FORWARD)

#define YAW_START 12
#define YAW_RIGHT 30
#define YAW_FRONT 96
#define YAW_LEFT 162
#define YAW_END   180
#define YAW_LIMIT (YAW_END-YAW_FRONT)*1.0/(YAW_LEFT-YAW_FRONT)


void initCamServo(void)
{
    pitch_cam.attach(PITCH_CAM_SERVO_PIN);
    yaw_cam.attach(YAW_CAM_SERVO_PIN);
}

// pitch -- 0: upright, 1.0: right forward, PITH_LIMIT: max down angle, -1.0: max backward angle
// yaw   -- 0: to the front, 1.0: to the right, -1.0: to the left
void camTurnTo(float pitch, float yaw)
{
    int pitch_val, yaw_val;

    // pitch is within [-0.5, 1]
    if (pitch > PITCH_LIMIT) pitch = PITCH_LIMIT;
    if (pitch <-1) pitch = -1;
    pitch_val = -pitch * (PITCH_UPRIGHT - PITCH_FORWARD) + PITCH_UPRIGHT;

    // yaw is within [-1, 1]
    if (yaw > YAW_LIMIT) yaw = YAW_LIMIT;
    if (yaw <-YAW_LIMIT) yaw = -YAW_LIMIT;
    yaw_val = - yaw * (YAW_FRONT - YAW_RIGHT) + YAW_FRONT;

    pitch_cam.write(pitch_val);
    delay(10); // avoid power over drive
    yaw_cam.write(yaw_val);
}
