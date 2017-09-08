/****************************************************
 * BaseControl
 *****************************************************
 * Based on MotoTest of DFRobot Devaster with extended change
 * Created 2017-5-20
 * By Guokai
 ******************************************************/
#include <L3G.h>
#include <LSM303.h>
#include <10dof.h>

/***************************
Sensor related functions
****************************/
L3G gyro;
LSM303 compass;
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

void gyro_init(void)
{
  if (!gyro.init()) {
    Serial.println("Failed to autodetect gyro type!");
    while (1);
  }
  gyro.enableDefault();

  gyro_calib();
}

void compass_init(void)
{
  if (!compass.init()) {
    Serial.println("Failed to autodetect gyro type!");
    while (1);
  }
  compass.enableDefault();
}

void initSensors(void)
{
    gyro_init();
    compass_init();
}

void getSensors(float readings[3][3])
{
    compass.read();
    float *gyros = get_gyro();
    readings[0][0] = gyros[0];
    readings[0][1] = gyros[1];
    readings[0][2] = gyros[2];
    readings[1][0] = compass.a.x;
    readings[1][1] = compass.a.y;
    readings[1][2] = compass.a.z;
    readings[2][0] = compass.m.x;
    readings[2][1] = compass.m.y;
    readings[2][2] = compass.m.z;
}
