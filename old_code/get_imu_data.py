#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex1_qwiic_ICM20948.py
#
# Simple Example for the Qwiic ICM20948 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, March 2020
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

from __future__ import print_function
import qwiic_icm20948
import time
import sys


def get_imu_dict(data_dict):
    IMU = qwiic_icm20948.QwiicIcm20948()

    IMU.begin()
    IMU.getAgmt()

    data_dict["AccelX"] = IMU.axRaw
    data_dict["AccelY"] = IMU.ayRaw
    data_dict["AccelZ"] = IMU.azRaw
    data_dict["GyroX"] = IMU.gxRaw
    data_dict["GyroY"] = IMU.gyRaw
    data_dict["GyroZ"] = IMU.gzRaw
    data_dict["MagX"] = IMU.mxRaw
    data_dict["MagY"] = IMU.myRaw
    data_dict["MagZ"] = IMU.mzRaw

def test_imu():
    IMU = qwiic_icm20948.QwiicIcm20948()

    IMU.begin()

    # we need to set the full scale range and then convert the raw value based on the conversion
    
    # set range to max 
    IMU.setFullScaleRangeAccel(qwiic_icm20948.gpm16)
    IMU.setFullScaleRangeGyro(qwiic_icm20948.dps2000)
    
    IMU.getAgmt()

    # sensitivities based on full scale range:
    # accelerometer - 2048
    # gyroscope - 16.4

    acc_sensitivity = 2048
    gyr_sensitivity = 16.4
    mag_sensitivity = 0.15

    print(IMU.axRaw / acc_sensitivity)
    print(IMU.ayRaw / acc_sensitivity)
    print(IMU.azRaw / acc_sensitivity)
    print(IMU.gxRaw / gyr_sensitivity)
    print(IMU.gyRaw / gyr_sensitivity)
    print(IMU.gzRaw / gyr_sensitivity)
    print(IMU.mxRaw * mag_sensitivity)
    print(IMU.myRaw * mag_sensitivity)
    print(IMU.mzRaw * mag_sensitivity)


# def runExample():

#	print("\nSparkFun 9DoF ICM-20948 Sensor  Example 1\n")
#	IMU = qwiic_icm20948.QwiicIcm20948()

#	if IMU.connected == False:
#		print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
#			file=sys.stderr)
#		return

#	IMU.begin()

#	while True:
#	if IMU.dataReady():
#		IMU.getAgmt() # read all axis and temp from sensor, note this also updates all instance variables
#		 '{: 06d}'.format(IMU.axRaw)\
#		, '\t', '{: 06d}'.format(IMU.ayRaw)\
#		, '\t', '{: 06d}'.format(IMU.azRaw)\
#		, '\t', '{: 06d}'.format(IMU.gxRaw)\
#		, '\t', '{: 06d}'.format(IMU.gyRaw)\
#		, '\t', '{: 06d}'.format(IMU.gzRaw)\
#		, '\t', '{: 06d}'.format(IMU.mxRaw)\
#		, '\t', '{: 06d}'.format(IMU.myRaw)\
#		, '\t', '{: 06d}'.format(IMU.mzRaw)\
#		)
#		time.sleep(0.03)
#	else:
#		print("Waiting for data")
#		time.sleep(0.5)


# if __name__ == '__main__':
#	try:
#		runExample()
#	except (KeyboardInterrupt, SystemExit) as exErr:
#		print("\nEnding Example 1")
#		sys.exit(0)


if __name__ == '__main__':
    test_imu()