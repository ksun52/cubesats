import csv
import ast
import os
import glob
import pdb
from SNR import distance
from SNR import getSNR
from pathlib import Path
import glob
    
def write_line(data_dict):

    # Specify the directory path
    directory_path = '/home/pi/team-papa/comms/pluto_SNR'

    # Define a pattern to match
    file_pattern = '*.csv'

    # Use glob to list files in the directory
    csv_files = glob.glob(os.path.join(directory_path, file_pattern))

    # Check if any files were found
    if csv_files:
        # Sort the list of files by modification time (newest first)
        csv_files.sort(key=os.path.getmtime, reverse=True)

        # Get the path of the most recent file
        most_recent_csv = csv_files[0]

        #print("The most recent csv file is:", most_recent_csv)
        with open(most_recent_csv, mode='a') as file:
            writer = csv.writer(file)
            new_data = list(data_dict.values())
            writer.writerow(["None" if data is None else data for data in new_data])

    else:
        print("No csv files found in the specified directory.")
    


def createDataHexfunc(count) :
    # Specify the directory path where your CSV files are located
    #directory_path = '/home/pi/code/team-papa/downlink_telem'
    directory_path = '/home/pi/team-papa/downlink_telem'

    # Define a pattern to match CSV files (e.g., *.csv)
    file_pattern = '*.csv'

    # Use glob to list CSV files in the directory
    csv_files = glob.glob(os.path.join(directory_path, file_pattern))

    # Check if any CSV files were found
    if csv_files:
        # Sort the list of CSV files by modification time (newest first)
        csv_files.sort(key=os.path.getmtime, reverse=True)

        # Get the path of the most recent CSV file
        most_recent_csv = csv_files[0]

        # print("The most recent CSV file is:", most_recent_csv)
    else:
        print("No CSV files found in the specified directory.")

    # Open the CSV file in read mode
    with open(most_recent_csv, 'r') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)

        # Skip rows until you reach the 32nd row
        for _ in range(31):
            next(csv_reader)

        # Read the 32nd through 35th rows
        rows_32_to_35 = [next(csv_reader) for _ in range(4)]
    
    
    # Setup the Pluto SNR stuff
    lat_sign = int(rows_32_to_35[1][0])
    lon_sign = int(rows_32_to_35[3][0])
    
    lat = float(rows_32_to_35[0][0]) if lat_sign==0 else -1*float(rows_32_to_35[0][0])
    lon = float(rows_32_to_35[2][0]) if lon_sign==0 else -1*float(rows_32_to_35[2][0])
    
    dist = distance(lat,lon)
    pluto_snr = getSNR(lat,lon)

    snr_dict = {
        "dist": dist,
        "snr": pluto_snr
    }

    write_line(snr_dict)

    #pdb.set_trace()
    

    '''
    Structure:
    1. determine if DAP we are transmitting is for telem (PID = 1) or thumbnail (PID = 2)
    2. DAP has PID, length, file number, file part, total parts in file, and data
    '''

    data_dict = {}        

    #with open('/home/pi/code/team-papa/comms/CFL_beacon_def.csv', 'r', newline='') as csv_file, open(most_recent_csv, 'r', newline='') as csv_file2:
    with open('/home/pi/team-papa/comms/CFL_beacon_def.csv', 'r', newline='') as csv_file, open(most_recent_csv, 'r', newline='') as csv_file2:
        csv_reader = csv.DictReader(csv_file)
        csv_reader2 = csv.DictReader(csv_file2)

        for row, row2 in zip(csv_reader, csv_reader2):
            title = row['Title']
            data_type = row['Data Type']
            offset = row['Offset']
            size = row['Size']
            signed = row['Signed']
            decode_conversion_function = row['Decode Conversion Function']
            encode_conversion_function = row['Encode Conversion Function']
            unit = row['Unit']
            comments = row['Comments']
            example_unencoded_X = row2['Data']
            encoded_X = row['Encoded X']

            data_dict[title] = {
                "Type": data_type,
                "Offset": offset,
                "Size": int(size),
                "Signed": signed,
                "Decoding Conversion": decode_conversion_function,
                "Encoding Conversion": encode_conversion_function,
                "Unit": unit,
                "Comments": comments,
                "Unencoded X": float(example_unencoded_X),
                "Encoded X": 0
            }

    # Printing the resulting dictionary
    # for key, value in data_dict.items():
    #     print(key)
    #     print(value)

    # Function to actually do the conversion function
    def apply_conversion(expression, X):
        try:
            result = eval(expression, {'X': X})
            return result
        except Exception as e:
            return f"Error: {e}"

    # start placing characters into the packet list starting from the back 
    # def place_bytes(packet_list, value, beacon_offset, data_length):
    #     end_position = beacon_offset*2 + data_length * 2 - 1

    #     for char in value[::-1]:
    #         packet_list[end_position] = char
    #         end_position -= 1

    # Populate dictionary with the hex data, with the conversion function applied

    beacon = b''
    for outer_key, inner_dict in data_dict.items():
        #inner_dict['Unencoded X'] = apply_conversion(inner_dict['Decoding Conversion'],inner_dict['Encoded X'])
        # print(outer_key + ": " + str(inner_dict['Unencoded X']))
        inner_dict['Encoded X'] = apply_conversion(inner_dict['Encoding Conversion'],inner_dict['Unencoded X'])
        inner_dict['Encoded X'] = int(inner_dict['Encoded X'])

        #pdb.set_trace()

        if outer_key == 'Packet Count':
            inner_dict['Encoded X'] = count.to_bytes(inner_dict['Size'],'little',signed=inner_dict['Signed'])
            beacon = beacon + inner_dict['Encoded X']
        else:
            inner_dict['Encoded X'] = inner_dict['Encoded X'].to_bytes(inner_dict['Size'],'little',signed=inner_dict['Signed'])
            beacon = beacon + inner_dict['Encoded X']

    #print(beacon)

    # Record the SNR to a CSV


    return beacon  

createDataHexfunc(1)
