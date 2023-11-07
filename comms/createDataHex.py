import csv
import ast
import os
import glob

# Specify the directory path where your CSV files are located
directory_path = '/home/pi/code/team-papa/downlink_telem'

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

    print("The most recent CSV file is:", most_recent_csv)
else:
    print("No CSV files found in the specified directory.")

'''
 Structure:
 1. determine if DAP we are transmitting is for telem (PID = 1) or thumbnail (PID = 2)
 2. DAP has PID, length, file number, file part, total parts in file, and data
'''

data_dict = {}        

with open('CFL_beacon_def.csv', 'r', newline='') as csv_file, open(most_recent_csv, 'r', newline='') as csv_file2:
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
        print(example_unencoded_X)
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
    inner_dict['Encoded X'] = apply_conversion(inner_dict['Encoding Conversion'],inner_dict['Unencoded X'])
    inner_dict['Encoded X'] = int(inner_dict['Encoded X'])
    inner_dict['Encoded X'] = inner_dict['Encoded X'].to_bytes(inner_dict['Size'],'little',signed=inner_dict['Signed'])
    beacon = beacon + inner_dict['Encoded X']

print(beacon)
