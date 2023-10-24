from math import sqrt
import pdb

def decode(packet):
    data = decode_RAP(packet)
    decode_data(data)


def decode_RAP(packet):
    # Search for the starting index of 'abcd' in the file content
    startIndex = packet.find('abcd')
    currentIndex = startIndex

    syncChars = packet[startIndex:startIndex+4]
    currentIndex = startIndex+4

    pID = packet[currentIndex:currentIndex+4]
    currentIndex = currentIndex+4

    sID = packet[currentIndex:currentIndex+4]
    sID_decimal = int(sID,16)
    currentIndex = currentIndex+4

    flags = packet[currentIndex:currentIndex+2]
    flags_decimal = int(flags,16)
    currentIndex = currentIndex+2

    # stored in wrong -> converted to good endian for byte size
    length = packet[currentIndex:currentIndex+4] #f500 
    length_decimal = int(length, 16) # converts hex to decimal
    currentIndex = currentIndex+4


    # Fletcher 16 implementation for header checksum
    sum1 = 0
    sum2 = 0
    for i in range(0,18,2):
        sum1 = (sum1 + int(packet[i:i+2],16)) % 255
        sum2 = (sum2 + sum1) % 255
    headerChecksum_F16_decimal = (sum2 << 8) | sum1

    headerChecksum = packet[currentIndex:currentIndex+4]
    headerChecksum_decimal = int(headerChecksum,16)
    currentIndex = currentIndex+4 # now at end of header checksum / beginning of real data

    dataBytes = length_decimal - 17
    realData = packet[currentIndex:currentIndex+dataBytes*2]

    currentIndex = currentIndex+dataBytes*2

    checksum = packet[currentIndex:currentIndex+4]
    checksum_decimal = int(checksum,16)
    currentIndex = currentIndex+4

    # Fletcher 16 implementation for data checksum
    sum1 = 0
    sum2 = 0
    for i in range(22,22+dataBytes*2,2):
        sum1 = (sum1 + int(packet[i:i+2],16)) % 255
        sum2 = (sum2 + sum1) % 255
    dataChecksum_F16_decimal = (sum2 << 8) | sum1

    HMAC = packet[currentIndex:currentIndex+8]
    currentIndex = currentIndex+8

    print('Sync Characters: ' + syncChars)
    print('pID: ' + pID)
    print('sID (decimal): ' + str(sID_decimal))
    print('flags (decimal): ' + str(flags_decimal))
    print('length (bytes): ' + length)
    print('Header Checksum (decimal): ' + str(headerChecksum_decimal))
    print('Header Checksum (Fletcher-16, decimal): ' + str(headerChecksum_F16_decimal))
    print('Data: ' + realData)
    print('Data Checksum (decimal): ' + str(checksum_decimal))
    print('Data Checksum Fletcher 16 (decimal): ' + str(dataChecksum_F16_decimal))
    print('HMAC: ' + HMAC)
    print('Full Header: ' + syncChars + pID + sID + flags + str(length) + headerChecksum)
    print('Footer: ' + checksum + HMAC)

    return realData



def decode_data(data):
    # convert to big endian 
    start = 0*2
    dist = 4*2
    RTC_Unix_Time = int((data[start:start+dist]), 16)

    start = 4*2
    dist = 2*2
    num_resets = int((data[start:start+dist]), 16)

    start = 18*2
    dist = 2*2
    total_mem = int((data[start:start+dist]), 16)

    start = 20*2
    dist = 2*2
    free_mem = int((data[start:start+dist]), 16)

    start = 44*2
    dist = 2*2
    FCPU_temp0 = int((data[start:start+dist]), 16)

    start = 60*2
    dist = 2*2
    battery_voltage = int((data[start:start+dist]), 16)

    start = 62*2
    dist = 2*2
    battery_current = int((data[start:start+dist]), 16)

    start = 64*2
    dist = 2*2
    battery_temp = int((data[start:start+dist]), 16)

    start = 150*2
    dist = 2*2
    pos_Y_mag_X = int((data[start:start+dist]), 16)

    start = 152*2
    dist = 2*2
    pos_Y_mag_Y = int((data[start:start+dist]), 16)

    start = 154*2
    dist = 2*2
    pos_Y_mag_Z = int((data[start:start+dist]), 16)


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


packet = 'abcd000000420300f57fb4651c2b8606cc0000000000000000000000007bee04ef00000000000000000000000000000000000000000000068100000000000000000000000000000eba05fc06ba00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000310016ff740000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005d33b0151c40'
decode(packet)
