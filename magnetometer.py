
import smbus2
import time
import pni_rm3100

# pass in magnetometer device_address - ours are 0x21 and 0x23
def get_mag_data(device_address):
    
    # Instantiate Objects
    pni_rm3100_device = pni_rm3100.PniRm3100()

    match device_address:
        case 0x20:
            address = pni_rm3100_device.DeviceAddress.I2C_ADDR_LL #0x20
        case 0x21:
            address = pni_rm3100_device.DeviceAddress.I2C_ADDR_HL #0x21
        case 0x22:
            address = pni_rm3100_device.DeviceAddress.I2C_ADDR_LH #0x22
        case 0x23:
            address = pni_rm3100_device.DeviceAddress.I2C_ADDR_HH #0x23
        case _: # default case
            address = pni_rm3100_device.DeviceAddress.I2C_ADDR_LL #0x20

    # Assign PNI Device Address
    # Default is I2C_ADDR_LL (0x20)
    # Note: this line is only necessary if you want to change from the default values --> see execute_continuous_measurements_with_default_config(),
    #       (it is still good to be explicit in your code/documentation!)
    pni_rm3100_device.assign_device_addr(address)

   
    magnetometer_readings = pni_rm3100_device.read_meas()

    x_mag = magnetometer_readings[0]
    y_mag = magnetometer_readings[1]
    z_mag = magnetometer_readings[2]

    return x_mag, y_mag, z_mag



# custom code - wrong 
"""# specify I2C address of the RM3100 magnetometer
# ours are 0x20 and 0x
def magnetometer_data(i2c_address):

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
    return [magnetic_field_x, magnetic_field_y, magnetic_field_z]


def read_magnetometer_data(register, bus, i2c_address):
    # Read 2 bytes of data from the specified register (little-endian format)
    data = bus.read_word_data(i2c_address, register, 2)
    # RM3100 outputs 16-bit signed data, so we need to convert it to a signed integer
    data = ((data << 8) & 0xFF00) | (data >> 8)
    return data

if __name__ == "__main__":
    print(magnetometer_data(0x20))
    print(magnetometer_data(0x21))


"""