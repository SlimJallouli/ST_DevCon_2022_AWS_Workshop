#ifndef SENSORS_SENSOR_READOUT_H_
#define SENSORS_SENSOR_READOUT_H_

/* Kernel includes. */
#include "FreeRTOS.h"

/* Sensor includes */
#include "b_u585i_iot02a_env_sensors.h"
#include "b_u585i_iot02a_motion_sensors.h"

typedef struct
{
    float_t fTemperature0;
    float_t fTemperature1;
    float_t fHumidity;
    float_t fBarometricPressure;
} EnvironmentalSensorData_t;

typedef struct
{
	BSP_MOTION_SENSOR_Axes_t xAcceleroAxes;
	BSP_MOTION_SENSOR_Axes_t xGyroAxes;
	BSP_MOTION_SENSOR_Axes_t xMagnetoAxes;
	BaseType_t xFallDetected;
} MotionSensorData_t;

typedef struct
{
	float_t fLongitude;
	float_t fLatitude;
} GeoPositionData_t;

void vSensorReadoutTask(void * pvParameters);
BaseType_t SensorReadout_GetEnvSensorData(EnvironmentalSensorData_t * const dataOut);
BaseType_t SensorReadout_GetMotionSensorData(MotionSensorData_t * const dataOut);
BaseType_t SensorReadout_GetGeoPositionData(GeoPositionData_t * const dataOut);
void SensorReadout_ClearFreeFallAlarm(void);

#endif /* SENSORS_SENSOR_READOUT_H_ */
