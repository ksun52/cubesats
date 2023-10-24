from math import sqrt
import pdb
# documentation link: https://docs.google.com/spreadsheets/d/1UO--kbqhnvFxWSW4DkALG8KMoHwPn-7fcskuqaRLpkQ/edit#gid=0


def little_to_big_endian(little_endian_hex):
    # Convert little-endian hex string to bytes
    little_endian_bytes = bytes.fromhex(little_endian_hex)
    
    # Reverse the byte order to convert from little-endian to big-endian
    big_endian_bytes = little_endian_bytes[::-1]
    
    # Convert bytes back to hexadecimal and remove the '0x' prefix
    big_endian_hex = big_endian_bytes.hex()
    
    return big_endian_hex


def decode_data(data):
    # convert to big endian 
    start = 0*2
    dist = 4*2
    RTC_Unix_Time = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 4*2
    dist = 2*2
    num_resets = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 18*2
    dist = 2*2
    total_mem = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 20*2
    dist = 2*2
    free_mem = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 44*2
    dist = 2*2
    FCPU_temp0 = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 60*2
    dist = 2*2
    battery_voltage = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 62*2
    dist = 2*2
    battery_current = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 64*2
    dist = 2*2
    battery_temp = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 150*2
    dist = 2*2
    pos_Y_mag_X = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 152*2
    dist = 2*2
    pos_Y_mag_Y = int(little_to_big_endian(data[start:start+dist]), 16)

    start = 154*2
    dist = 2*2
    pos_Y_mag_Z = int(little_to_big_endian(data[start:start+dist]), 16)


    RTC_Unix_Time_conv = RTC_Unix_Time
    num_resets_conv = num_resets
    total_mem_conv = total_mem * 4
    free_mem_conv = free_mem * 4
    # pdb.set_trace()
    FCPU_temp0_conv = -1481.96+sqrt(2.1962*1000000+(1.8639-(FCPU_temp0/1000.0))/(3.88/1000000))
    battery_voltage_conv = (battery_voltage/1000)*(2.2) + 0
    battery_current_conv = (battery_current/1000)*(2.0) + -3
    battery_temp_conv = (battery_temp/1000)*(-85.54319) + 159.6493
    pos_Y_mag_X_conv = pos_Y_mag_X / 219.0
    pos_Y_mag_Y_conv = pos_Y_mag_Y / 219.0
    pos_Y_mag_Z_conv = pos_Y_mag_Z / 219.0
    pos_Y_mag_magnitude = sqrt(pos_Y_mag_X_conv*pos_Y_mag_X_conv + pos_Y_mag_Y_conv*pos_Y_mag_Y_conv + pos_Y_mag_Z_conv*pos_Y_mag_Z_conv)

    print("RTC_Unix_Time_conv: " + str(RTC_Unix_Time_conv))
    print("num_resets_conv: " + str(num_resets_conv))
    print("total_mem_conv: " + str(total_mem_conv))
    print("free_mem_conv: " + str(free_mem_conv))
    print("FCPU_temp0_conv: " + str(FCPU_temp0_conv))
    print("battery_voltage_conv: " + str(battery_voltage_conv))
    print("battery_current_conv: " + str(battery_current_conv))
    print("battery_temp_conv: " + str(battery_temp_conv))
    print("pos_Y_mag_X_conv: " + str(pos_Y_mag_X_conv))
    print("pos_Y_mag_Y_conv: " + str(pos_Y_mag_Y_conv))
    print("pos_Y_mag_Z_conv: " + str(pos_Y_mag_Z_conv))
    print("pos_Y_mag_magnitude: " + str(pos_Y_mag_magnitude))



data = '862b1c65cc0609000b000900010023001f2fee7bef040100000000976a0700395b19006f2e2500004a4a3e0081067106fa0c60002800fa0ccf0e0d00ba0efc05ba06c80e10005f0d20001500f60c910056005e06610d8600f40cb400310a55013c0f6f00600664064909dc001c0f410056065c06d50745002d0f110065066506ea076b00320f18005b065e06fdfcb606b106b00600c03100160074ff5b000100e9ff8600efff6600c000c1ffcc00950a8f0ad209a309dd09b409620b4c0b88007402320a5b00b8338b334c20001000000002005d03000004000000ff723d00beffffffff'
decode_data(data)
=======
def extract_bits(data, offset, data_length):
    full_size = 245
    # each datapoint is 4 bits 
    # data length of 1 = 4 bits 
    bitmask = (1 << data_length * 4) - 1
    return (data & (bitmask << offset)) >> offset




data = '862b1c65cc0609000b000900010023001f2fee7bef040100000000976a0700395b19006f2e2500004a4a3e0081067106fa0c60002800fa0ccf0e0d00ba0efc05ba06c80e10005f0d20001500f60c910056005e06610d8600f40cb400310a55013c0f6f00600664064909dc001c0f410056065c06d50745002d0f110065066506ea076b00320f18005b065e06fdfcb606b106b00600c03100160074ff5b000100e9ff8600efff6600c000c1ffcc00950a8f0ad209a309dd09b409620b4c0b88007402320a5b00b8338b334c20001000000002005d03000004000000ff723d00beffffffff'

# RTC_Unix_Time = data[0:0+4]
# num_resets = data[4:4+2]
# total_mem = data[18:18+2]
# free_mem = data[20:20+2]
# FCPU_temp0 = data[44:44+2]
# battery_voltage = data[60:60+2]
# battery_current = data[62:62+2]
# battery_temp = data[64:64+2]
# pos_Y_mag_X = data[150:150+2]
# pos_Y_mag_Y = data[152:152+2]
# pos_Y_mag_Z = data[154:154+2]

data_num = int(data,16)
RTC_Unix_Time = extract_bits(data_num, offset=0, data_length=4)
pdb.set_trace()
# convert RTC_Unix_Time to big endian 
RTC_Unix_Time = (RTC_Unix_Time & 0xFF) << 0xFF | (RTC_Unix_Time >> 0xFF)

num_resets = extract_bits(data_num, offset=4, data_length=2)
total_mem = extract_bits(data_num, offset=18, data_length=2)
free_mem = extract_bits(data_num, offset=20, data_length=2)
FCPU_temp0 = extract_bits(data_num, offset=44, data_length=2)
battery_voltage = extract_bits(data_num, offset=60, data_length=2)
battery_current = extract_bits(data_num, offset=62, data_length=2)
battery_temp = extract_bits(data_num, offset=64, data_length=2)
pos_Y_mag_X = extract_bits(data_num, offset=150, data_length=2)
pos_Y_mag_Y = extract_bits(data_num, offset=152, data_length=2)
pos_Y_mag_Z = extract_bits(data_num, offset=154, data_length=2)


RTC_Unix_Time_conv = RTC_Unix_Time
num_resets_conv = num_resets
total_mem_conv = total_mem * 4
free_mem_conv = free_mem * 4
# pdb.set_trace()
FCPU_temp0_conv = -1481.96+sqrt(2.1962*1000000+(1.8639-(FCPU_temp0/1000.0))/(3.88/1000000))
battery_voltage_conv = (battery_voltage/1000)*(2.2) + 0
battery_current_conv = (battery_current/1000)*(2.0) + -3
battery_temp_conv = (battery_temp/1000)*(-85.54319) + 159.6493
pos_Y_mag_X_conv = pos_Y_mag_X / 219.0
pos_Y_mag_Y_conv = pos_Y_mag_Y / 219.0
pos_Y_mag_Z_conv = pos_Y_mag_Z / 219.0
pos_Y_mag_magnitude = sqrt(pos_Y_mag_X_conv*pos_Y_mag_X_conv + pos_Y_mag_Y_conv*pos_Y_mag_Y_conv + pos_Y_mag_Z_conv*pos_Y_mag_Z_conv)

print("RTC_Unix_Time_conv: " + str(RTC_Unix_Time_conv))
print("num_resets_conv: " + str(num_resets_conv))
print("total_mem_conv: " + str(total_mem_conv))
print("free_mem_conv: " + str(free_mem_conv))
print("FCPU_temp0_conv: " + str(FCPU_temp0_conv))
print("battery_voltage_conv: " + str(battery_voltage_conv))
print("battery_current_conv: " + str(battery_current_conv))
print("battery_temp_conv: " + str(battery_temp_conv))
print("pos_Y_mag_X_conv: " + str(pos_Y_mag_X_conv))
print("pos_Y_mag_Y_conv: " + str(pos_Y_mag_Y_conv))
print("pos_Y_mag_Z_conv: " + str(pos_Y_mag_Z_conv))
print("pos_Y_mag_magnitude: " + str(pos_Y_mag_magnitude))



>>>>>>> ba17a06b51f508b20c1366efca7f0b264682adab
