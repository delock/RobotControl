#include "Arduino.h"
#include "light.h"

const int led_pin = 10;
void initLight(void)
{
    pinMode(led_pin, OUTPUT);
}

void setLight(bool on)
{
    digitalWrite(led_pin, on?HIGH:LOW);
}
