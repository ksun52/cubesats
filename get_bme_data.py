#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_env_bme280_ex1.py
#
# Simple Example for the Qwiic BME280 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#

import qwiic_bme280
import time
import sys


# def get_imu_dict(data_dict):
#     mySensor = qwiic_bme280.QwiicBme280()

#     # data_dict["AccelX"] = '{: 06d}'.format(IMU.axRaw())
#     # data_dict["AccelY"] = '{: 06d}'.format(IMU.ayRaw)
#     # data_dict["AccelZ"] = '{: 06d}'.format(IMU.azRaw)
#     # data_dict["GyroX"] = '{: 06d}'.format(IMU.gxRaw)
#     # data_dict["GyroY"] = '{: 06d}'.format(IMU.gyRaw)
#     # data_dict["GyroZ"] = '{: 06d}'.format(IMU.gzRaw)
#     # data_dict["MagX"] = '{: 06d}'.format(IMU.mxRaw)
#     # data_dict["MagY"] = '{: 06d}'.format(IMU.myRaw)
#     # data_dict["MagZ"] ='{: 06d}'.format(IMU.mzRaw)
#     mySensor.begin()
#     IMU.getAgmt()
#     data_dict["AccelX"] = '{: 07d}'.format(IMU.axRaw)
#     data_dict["AccelY"] = '{: 07d}'.format(IMU.ayRaw)
#     data_dict["AccelZ"] = '{: 07d}'.format(IMU.azRaw)
#     data_dict["GyroX"] = '{: 07d}'.format(IMU.gxRaw)
#     data_dict["GyroY"] = '{: 07d}'.format(IMU.gyRaw)
#     data_dict["GyroZ"] = '{: 07d}'.format(IMU.gzRaw)
#     data_dict["MagX"] = '{: 07d}'.format(IMU.mxRaw)
#     data_dict["MagY"] = '{: 07d}'.format(IMU.myRaw)
#     data_dict["MagZ"] = '{: 07d}'.format(IMU.mzRaw)

def runExample():

	print("\nSparkFun BME280 Sensor  Example 1\n")
	mySensor = qwiic_bme280.QwiicBme280()

	if mySensor.connected == False:
		print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	mySensor.begin()

	while True:
		print("Humidity:\t%.3f" % mySensor.humidity)

		print("Pressure:\t%.3f" % mySensor.pressure)	

		print("Altitude:\t%.3f" % mySensor.altitude_feet)

		print("Temperature:\t%.2f" % mySensor.temperature_fahrenheit)		

		print("")
		
		time.sleep(1)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


