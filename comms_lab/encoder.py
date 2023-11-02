import pdb

def tester():
    data = {
        "RTC_unix_time": 1696344966, 
        "Num_resets": 1740, 
        "tot_Mem": 126904, 
        "free_Mem": 5052,
        "FCPU_temp0": 17.194056992788774,
        "Battery_voltage": 8.294,
        "Battery_current": 0.06400000000000006,
        "Battery_temp": 12.343926820000007,
        "pos_y_mag_x": 0.2237442922374429,
        "pos_y_mag_y": 0.1004566210045662,
        "pos_y_mag_z": 298.61187214611874
        }

    print(encode(data))

# data comes in  a dictionary
def encode(data):
    packet_list = ['0'] * 245 * 2

    sync = 'abcd'
    place_bytes(packet_list, sync, 0, 2)
    
    pid = '0000'
    place_bytes(packet_list, pid, 2, 2)

    sid = '0042'
    place_bytes(packet_list, sid, 4, 2)
    
    flags = '03'
    place_bytes(packet_list, flags, 6, 1)

    length = '00f5'
    place_bytes(packet_list, length, 7, 2)
    
    # do checksum and other stuff
    # Fletcher 16 implementation for header checksum
    sum1 = 0
    sum2 = 0
    for i in range(0,18,2):
        # pdb.set_trace()
        sum1 = (sum1 + int(''.join(packet_list[i:i+2]),16)) % 255
        sum2 = (sum2 + sum1) % 255
    headerChecksum_F16_decimal = (sum2 << 8) | sum1
    headerChecksum_F16_hex = hex(headerChecksum_F16_decimal)[2:]

    place_bytes(packet_list, headerChecksum_F16_hex, 9, 2)

    hmac = 'b0151c40'
    place_bytes(packet_list, hmac, 241, 4)


    # first try to get data
    RTC_unix_time_convt = data.get("RTC_unix_time") or 0
    Num_resets_convt = data.get("Num_resets") or 0
    tot_Mem_convt = data.get("tot_Mem") or 0
    free_Mem_convt = data.get("free_Mem") or 0
    FCPU_temp0_convt = data.get("FCPU_temp0") or 0
    Battery_voltage_convt = data.get("Battery_voltage") or 0
    Battery_current_convt = data.get("Battery_current") or 0
    Battery_temp_convt = data.get("Battery_temp") or 0
    pos_y_mag_x_convt = data.get("pos_y_mag_x") or 0
    pos_y_mag_y_convt= data.get("pos_y_mag_y") or 0
    pos_y_mag_z_convt = data.get("pos_y_mag_z") or 0

    # then convert everything to right format 
    RTC_unix_time = RTC_unix_time_convt
    Num_resets = Num_resets_convt
    tot_Mem = int(tot_Mem_convt / 4)
    free_Mem = int(free_Mem_convt / 4)
    FCPU_temp0 = int(((((FCPU_temp0_convt+1481.96)**2 - 2.1962*1000000)*(3.88/1000000)) - 1.8639)*-1000.0)
    Battery_voltage = int(Battery_voltage_convt *(1000/2.2))
    Battery_current = int((Battery_current_convt + 3)*1000/2)
    Battery_temp = int((Battery_temp_convt - 159.6493) * (1000 / -85.54319)) 
    pos_y_mag_x = int(pos_y_mag_x_convt * 219.0)
    pos_y_mag_y = int(pos_y_mag_y_convt * 219.0)
    pos_y_mag_z = int(pos_y_mag_z_convt * 219.0)
   
    # put converted value into hex 
    RTC_unix_time_hex = hex(RTC_unix_time)[2:]
    Num_resets_hex = hex(Num_resets)[2:]
    tot_Mem_hex = hex(tot_Mem)[2:]
    free_Mem_hex = hex(free_Mem)[2:]
    FCPU_temp0_hex = hex(FCPU_temp0)[2:]
    Battery_voltage_hex = hex(Battery_voltage)[2:]
    Battery_current_hex = hex(Battery_current)[2:]
    Battery_temp_hex = hex(Battery_temp)[2:]
    pos_y_mag_x_hex = hex(pos_y_mag_x)[2:]
    pos_y_mag_y_hex = hex(pos_y_mag_y)[2:]
    pos_y_mag_z_hex = hex(pos_y_mag_z)[2:]
    
    # put hex values into the right positions 
    # data length and beacon_offset are in bytes 
  
    # pre_data_bytes = 11 <--change back to this
    pre_data_bytes = 11
    
    place_bytes(packet_list, value=RTC_unix_time_hex, beacon_offset=pre_data_bytes+0, data_length=4)
    place_bytes(packet_list, value=Num_resets_hex, beacon_offset=pre_data_bytes+4, data_length=2)
    place_bytes(packet_list, value=tot_Mem_hex, beacon_offset=pre_data_bytes+18, data_length=2)
    place_bytes(packet_list, value=free_Mem_hex, beacon_offset=pre_data_bytes+20, data_length=2)
    place_bytes(packet_list, value=FCPU_temp0_hex, beacon_offset=pre_data_bytes+44, data_length=2)
    place_bytes(packet_list, value=Battery_voltage_hex, beacon_offset=pre_data_bytes+60, data_length=2)
    place_bytes(packet_list, value=Battery_current_hex, beacon_offset=pre_data_bytes+62, data_length=2)
    place_bytes(packet_list, value=Battery_temp_hex, beacon_offset=pre_data_bytes+64, data_length=2)
    place_bytes(packet_list, value=pos_y_mag_x_hex, beacon_offset=pre_data_bytes+150, data_length=2)
    place_bytes(packet_list, value=pos_y_mag_y_hex, beacon_offset=pre_data_bytes+152, data_length=2)
    place_bytes(packet_list, value=pos_y_mag_z_hex, beacon_offset=pre_data_bytes+154, data_length=2)


    # Fletcher 16 implementation for data checksum
    sum1 = 0
    sum2 = 0
    for i in range(22,478,2):
        sum1 = (sum1 + int(''.join(packet_list[i:i+2]),16)) % 255
        sum2 = (sum2 + sum1) % 255
    dataChecksum_F16_decimal = (sum2 << 8) | sum1
    dataChecksum_F16_hex = hex(dataChecksum_F16_decimal)[2:]    
    place_bytes(packet_list, dataChecksum_F16_hex, 239, 2)

    return ''.join(packet_list)


# start placing characters into the packet list starting from the back 
def place_bytes(packet_list, value, beacon_offset, data_length):
    end_position = beacon_offset*2 + data_length * 2 - 1

    for char in value[::-1]:
        packet_list[end_position] = char
        end_position -= 1


if __name__ == "__main__":
    tester()