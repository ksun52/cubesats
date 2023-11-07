"""
# sparkfun documentation
# https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/experiment-4-i2c-temperature-sensor
"""

import time
import smbus2
# from qwiic_tmp102 import QwiicTmp102Sensor

"""Qwiic Version"""
# def sensor_temp():
#     tmp102 = QwiicTmp102Sensor()
#     return tmp102.read_temp_c()
    


"""Custom Version"""
def sensor_temperature(desired_i2c_address):

    i2c_ch = 1

    # TMP102 address on the I2C bus
    # 0x48 or 0x49
    i2c_address = desired_i2c_address

    # Register addresses
    reg_temp = 0x00

    # Initialize I2C (SMBus)
    bus = smbus2.SMBus(i2c_ch)

    # Read temperature registers
    val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
    # NOTE: val[0] = MSB byte 1, val [1] = LSB byte 2
    #print ("!shifted val[0] = ", bin(val[0]), "val[1] = ", bin(val[1]))

    temp_c = (val[0] << 4) | (val[1] >> 4)  # this is necessary - read the sparkfun docs 
    #print (" shifted val[0] = ", bin(val[0] << 4), "val[1] = ", bin(val[1] >> 4))
    #print (bin(temp_c))

    # Convert to 2s complement (temperatures can be negative)
    temp_c = twos_comp(temp_c, 12)

    # Convert registers value to temperature (C)
    temp_c = temp_c * 0.0625

    return round(temp_c, 2)    # returns temperature in degrees Celsius 
   

# Calculate the 2's complement of a number
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val
