#include <DFMobile.h>
#include "wheel.h"
#include "milli_time.h"

// if no new command came in, wheel will stop after 0.5s
int keep_speed_millis = 500;

DFMobile wheel (4,5,7,6);

int l_speed = 0, r_speed = 0;

void initWheel(void)
{
    wheel.Direction (HIGH, LOW);
}

unsigned long set_time;
// set the speed of each wheel
// the value is between [-1.0, 1.0]
void setSpeed (float left, float right)
{
    if (left > 1.0) left = 1.0;
    else if (left <-1.0) left = 1.0;

    if (right > 1.0) right = 1.0;
    else if (right <-1.0) right = 1.0;

    l_speed = left * 255;
    r_speed = right * 255;
    set_time = millis();
    wheel.Speed (r_speed, l_speed);
}

float getLSpeed(void)
{
    return l_speed / 255.0;
}

float getRSpeed(void)
{
    return r_speed / 255.0;
}

// keep current speed for another 0.5s
void keepSpeed (void)
{
    set_time = millis();
}

void setKeepTime(float time)
{
    if (time > 1.0) time = 1.0;
    if (time < 0.01) time = 0.01;
    keep_speed_millis = time * 1000;
}

void wheelLoop(void)
{
    unsigned long cur_time = millis();
    unsigned long period = getPeriod(cur_time, set_time);
    if (period > keep_speed_millis) {
        setSpeed (0.0, 0.0);
    }
}
