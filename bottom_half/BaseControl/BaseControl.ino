/****************************************************
 * BaseControl
 *****************************************************
 * Based on MotoTest of DFRobot Devaster with extended change
 * Created 2017-5-20
 * By Guokai
 ******************************************************/
#include <DFMobile.h>
#include <Wire.h>
#include <L3G.h>
#include <LSM303.h>
#include <SFE_BMP180.h>

DFMobile Robot (4,5,7,6);     // initiate the Motor pin

/***************************
Sensor related functions
****************************/
L3G gyro;
LSM303 compass;
SFE_BMP180 pressure;
float gyro_zeros[3] = {0.0, 0.0, 0.0};

#define GYRO_CALIB_CNT 10
#define GYRO_SCALE (PI/180.0)*(200.0/22857.0)

void gyro_calib()
{
  for (int i=0; i<GYRO_CALIB_CNT; i++) {
    gyro.read();
    gyro_zeros[0] += gyro.g.x;
    gyro_zeros[1] += gyro.g.y;
    gyro_zeros[2] += gyro.g.z;
  }
  gyro_zeros[0] = gyro_zeros[0]/GYRO_CALIB_CNT;
  gyro_zeros[1] = gyro_zeros[1]/GYRO_CALIB_CNT;
  gyro_zeros[2] = gyro_zeros[2]/GYRO_CALIB_CNT;
}

float *get_gyro()
{
    static float gyro_ret[3];
    gyro.read();
    gyro_ret[0] = (gyro.g.x-gyro_zeros[0])*GYRO_SCALE;
    gyro_ret[1] = (gyro.g.y-gyro_zeros[1])*GYRO_SCALE;
    gyro_ret[2] = (gyro.g.z-gyro_zeros[2])*GYRO_SCALE;
    return gyro_ret;
}

void gyro_init()
{
  if (!gyro.init()) {
    Serial.println("Failed to autodetect gyro type!");
    while (1);
  }
  gyro.enableDefault();

  gyro_calib();  
}

void compass_init()
{
  if (!compass.init()) {
    Serial.println("Failed to autodetect gyro type!");
    while (1);
  }
  compass.enableDefault();
}

void pressure_init()
{
  if (!pressure.begin()) {
    Serial.println("BMP180 init fail (disconnected?)\n\n");
    while(1);
  }
}

void init_sensors()
{
    gyro_init();
    compass_init();
    pressure_init();
}
/***** end of sensor functions *********/

void setup () {
  Serial.begin(115200);
  Wire.begin();

  Robot.Direction (HIGH,LOW);  // initiate the positive direction
  init_sensors();
}

/************** speed stuff ***************/
int lSpeed = 0, rSpeed = 0;
int prevLSpeed = lSpeed-1, prevRSpeed = rSpeed+1;

int speed=0, turn=0;
void calcSpeed()
{
  int tempL, tempR;
  tempL = speed + turn;
  tempR = speed - turn;
  
  if (tempL >255) tempL=255;
  if (tempR >255) tempR=255;
  if (tempL <-255) tempL=-255;
  if (tempR <-255) tempR=255;
  
  lSpeed = tempL;
  rSpeed = tempR;
}

// input range from -5 to 5
// 0: stop
// 1: slow fwd
// 5: fast fwd
// -1: slow bwd
// -5: fast bwd
// other values in between: between fast and slow
void setSpeed(int input)
{
  speed = input*50;
  if (input > 5) speed = 250;
  if (input < -5) speed = -250;
  calcSpeed();
}

// input range from -5 to 5
// 0: no turn
// 1: turn right slowly
// 5: turn right fast
// -1: turn left slowly
// -5: turn left fast
void setTurn(int input)
{
  turn = input*50;
  if (input > 5) turn = 250;
  if (input < -5) turn = -250;
  calcSpeed();
}

void loop () {
    if (prevLSpeed != lSpeed || prevRSpeed != rSpeed) {
        Robot.Speed (rSpeed, lSpeed);
        prevLSpeed = lSpeed;
        prevRSpeed = rSpeed;
    }
#if 1
    setSpeed(0);
    compass.read();

    float *gyros = get_gyro();
    Serial.print("G: ");
    Serial.print(gyros[0]);
    Serial.print(",\t");
    Serial.print(gyros[1]);
    Serial.print(",\t");
    Serial.print(gyros[2]);

    Serial.print(";\t\tA: ");
    Serial.print(compass.a.x);
    Serial.print(",\t");
    Serial.print(compass.a.y);
    Serial.print(",\t");
    Serial.print(compass.a.z);

    Serial.print(";\t\tM: ");
    Serial.print(compass.m.x);
    Serial.print(",\t");
    Serial.print(compass.m.y);
    Serial.print(",\t");
    Serial.print(compass.m.z);
    
    double T;
    char status = pressure.startTemperature();
    delay(status);
    pressure.getTemperature(T);
    Serial.print(";\t\t: ");
    Serial.println(T);
#endif
   #if 1
    // there is no delay, we want the robot to respond to command as fast as possible
    delay (100);
    #endif
}








