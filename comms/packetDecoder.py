# take in txt file
import binascii
import pdb
import csv
import ast
import os
import time
import datetime
from pathlib import Path

def extract_bytes(hex_string):
    hex_bytes = bytes.fromhex(hex_string)
        
    # Extract bytes from [byte 12, -byte 6)
    extracted_bytes = hex_bytes[11:-6]
        
    return extracted_bytes

def process_txt_file(file_path):
    byte_arrays = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for i in range(0, len(lines), 2):
            hex_string = lines[i].strip() 
            extracted_bytes = extract_bytes(hex_string)
            byte_arrays.append(extracted_bytes)
    return byte_arrays

# Example usage
file_path = "downlinked_packets.txt"
result = process_txt_file(file_path)

image_byte_array = []
image_dict = {}

# File class
class File:
    def __init__(self, total_parts):
        self.total_parts = total_parts
        self.all_file_parts = []

def reconstructImage(file, filenum, full_image):
    
    if full_image == True:
        with open('/Users/kevin/Desktop/CubeSats/CODE/team-papa/comms/transmitted_thumbnails/reconstructed_image_FULL'+str(filenum)+'.jpg','wb') as image_file:
            byte_array = b''.join(file.all_file_parts)
            image_file.write(byte_array)
    else:
        with open('/Users/kevin/Desktop/CubeSats/CODE/team-papa/comms/transmitted_thumbnails/reconstructed_image_INCOMPLETE'+str(filenum)+'.jpg','wb') as image_file:
            byte_array = b''.join(file.all_file_parts)
            image_file.write(byte_array)

def create_file():
    
    csv_file2 = Path("transmitted_telem", "unencoded_telem.csv")

    with open(csv_file2, 'w', newline='') as csvfile2:
        # Write the header row
        csvwriter = csv.writer(csvfile2)
        
        csvwriter.writerow(
            ["UnixTime", "PacketCount", "GyroX", "GyroY", "GyroZ", "AccelX", "AccelY", "AccelZ", "MagX", "MagY", "MagZ",
            "BatteryTemp1", "BatteryTemp2", "BMETemp", "BMEPressure", "BMEHumidity", "UsedRam", "FreeMemory", "CPULoad",
            "CPUTemp", "BattRawVoltage", "BattRawCurrent", "V3v3", "I3v3", "V5v0", "I5v0", "VvBatt", "IvBatt", "RegTemp3v3","RegTemp5v0",
            "GPSLat", "GPSLatNS", "GPSLn", "GPSLonEW","GPSAlt", "GPSVelocity","GPSSNR","Mag1X","Mag1Y","Mag1Z","Mag2X", "Mag2Y", "Mag2Z" ])
    return csv_file2
    
def write_line(data_dict, csv_file2):
    with open(csv_file2, mode='a') as file:
        writer = csv.writer(file)
        new_data = list(data_dict.values())
        writer.writerow(["None" if data is None else data for data in new_data])

# First, create a list of just image data, assuming first file number is 0
current_filenum = 0
create_file()

for byte_array in result:
    PID = byte_array[0] # type int
    length = int.from_bytes(byte_array[1:2],byteorder='little')
    file_num = int.from_bytes(byte_array[3:4],byteorder='little')
    file_part = int.from_bytes(byte_array[5:6],byteorder='little')
    total_parts = int.from_bytes(byte_array[7:8],byteorder='little')    
    data = byte_array[9:]
    
    
    # See if we have an image
    if PID == 69:
        
        # Check to see if we need to make a new file and add to dictionary or append this data to existing file
        if file_num != current_filenum:
            image_dict[str(file_num)] = {
            'file': File(total_parts=total_parts)
            }

            image_dict[str(file_num)]['file'].all_file_parts.append(data)

            current_filenum = file_num
            #print(len(image_dict[str(file_num)]['file'].all_file_parts))
        else:
            image_dict[str(file_num)]['file'].all_file_parts.append(data)
            #print(len(image_dict[str(file_num)]['file'].all_file_parts))
    # Otherwise, we have telemetry data
    else:
        print("")
        # data_dict = {}        

        # with open('/home/pi/team-papa/comms/CFL_beacon_def.csv', 'r') as csv_file:
        #     csv_reader = csv.DictReader(csv_file)

        #     # Function to actually do the conversion function
        #     def apply_conversion(expression, X):
        #         try:
        #             result = eval(expression, {'X': X})
        #             return result
        #         except Exception as e:
        #             return f"Error: {e}"
            
        #     def gyro_conversion(lsb):
        #         # Gyro Conversion Function
        #         return lsb / 16.4  # ±2000 dps

        #     def accel_conversion(lsb):
        #         # Accel Conversion Function
        #         return lsb / 2048.0  # ±16 g

        #     for row in csv_reader:
        #         title = row['Title']
        #         data_type = row['Data Type']
        #         offset = row['Offset']
        #         size = row['Size']
        #         is_signed = True if int(row['Signed'])==1 else False
        #         decode_conversion_function = row['Decode Conversion Function']
        #         encode_conversion_function = row['Encode Conversion Function']
        #         unit = row['Unit']
        #         comments = row['Comments']
        #         encoded_X = byte_array[int(offset):int(offset)+int(size)]

        #         #print(encoded_X)
        #         #pdb.set_trace()

        #         # Apply specific conversion for Gyro and Accel, general conversion for others
        #         if title in ["Gyro X", "Gyro Y", "Gyro Z"]:
        #             unencoded_value = gyro_conversion(int.from_bytes(encoded_X, byteorder='little', signed=is_signed))
        #         elif title in ["Accel X", "Accel Y", "Accel Z"]:
        #             unencoded_value = accel_conversion(int.from_bytes(encoded_X, byteorder='little', signed=is_signed))
        #         else:
        #             unencoded_value = apply_conversion(decode_conversion_function,int.from_bytes(encoded_X,byteorder='little',signed=is_signed))


        #         data_dict[title] = {
        #             "Type": data_type,
        #             "Offset": offset,
        #             "Size": int(size),
        #             "Signed": is_signed,
        #             "Decoding Conversion": decode_conversion_function,
        #             "Encoding Conversion": encode_conversion_function,
        #             "Unit": unit,
        #             "Comments": comments,
        #             # "Unencoded X": apply_conversion(decode_conversion_function,int.from_bytes(encoded_X,byteorder='little',signed=is_signed)),
        #             "Unencoded X": unencoded_value,
        #             "Encoded X": encoded_X
        #         }
        #         #pdb.set_trace()
        # unencoded_x_values = {key: entry["Unencoded X"] for key, entry in data_dict.items() if "Unencoded X" in entry}    

        # # WRITE TO CSV 
        # csv_file2 = Path("transmitted_telem", "unencoded_telem.csv")
        # write_line(unencoded_x_values, csv_file2)
                
        # #pdb.set_trace()

# Finally, go through all files in dictionary, and if we have any complete files, run reconstruct method and save down thumbnails
for outer_key, inner_dict in image_dict.items():
    if len(inner_dict['file'].all_file_parts) == inner_dict['file'].total_parts:
        reconstructImage(inner_dict['file'], outer_key,True)
    else:
        reconstructImage(inner_dict['file'], outer_key, False)

            
#pdb.set_trace()



