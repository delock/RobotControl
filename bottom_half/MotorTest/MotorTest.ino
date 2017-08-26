/****************************************************
 * MotorTest
 *****************************************************
 * This example is aimed to control DFMobile basic motion -- Forward and Back
 * Created 2015-3-2
 * By Gavin
 ******************************************************/
#include <DFMobile.h>

DFMobile Robot (4,5,7,6);     // initiate the Motor pin

void setup () {
  Robot.Direction (HIGH, LOW);  // initiate the positive direction  
}

#define SPEED 255
void loop () {
  Robot.Speed (SPEED, SPEED);      //Forward
  delay (1000);

  Robot.Speed (-SPEED,-SPEED);    //Back
  delay (1000);

  Robot.Speed (SPEED,-SPEED);      //Forward
  delay (1000);

  Robot.Speed (-SPEED,SPEED);    //Back
  delay (1000);
  
  Robot.Speed (0, 0);     //Stop
  delay (2000);

}








