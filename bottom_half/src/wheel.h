#ifndef WHEEL_H
#define WHEEL_H

void initWheel (void);

// set the speed of both wheel.  The wheel will stop after 500 milliseconds
// the default value is 500ms, if you want to change this value call setKeepTime
void setSpeed (float left, float right);

float getLSpeed(void);
float getRSpeed(void);

// when this is called, the wheel will keep current speed for a while
void keepSpeed (void);

// set keep speed time in seconds, this value must between 0.01s and 1.0s
void setKeepTime(float time);

void wheelLoop(void);

#endif//WHEEL_H
