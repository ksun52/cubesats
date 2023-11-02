import smbus2
import time

def magnetometer_data():
            
    # I2C address of the RM3100 magnetometer
    i2c_address = 0x20

    # Register addresses for RM3100 magnetometer
    REG_DATA_X = 0x00
    REG_DATA_Y = 0x02
    REG_DATA_Z = 0x04

    # Initialize I2C (SMBus)
    bus = smbus2.SMBus(1)  # Use 1 for I2C bus 1 on Raspberry Pi
    
    data_x = read_magnetometer_data(REG_DATA_X, bus, i2c_address)
    data_y = read_magnetometer_data(REG_DATA_Y, bus, i2c_address)
    data_z = read_magnetometer_data(REG_DATA_Z, bus, i2c_address)

    # Convert raw data to magnetic field strength (in microteslas)
    magnetic_field_x = data_x * 0.15  # 0.15 µT/LSB (sensitivity of RM3100 in low-power mode)
    magnetic_field_y = data_y * 0.15
    magnetic_field_z = data_z * 0.15

    bus.close()


def read_magnetometer_data(register, bus, i2c_address):
    # Read 2 bytes of data from the specified register (little-endian format)
    data = bus.read_word_data(i2c_address, register)
    # RM3100 outputs 16-bit signed data, so we need to convert it to a signed integer
    data = ((data << 8) & 0xFF00) | (data >> 8)
    return data

