import csv
import ast

'''
 Structure:
 1. determine if DAP we are transmitting is for telem (PID = 1) or thumbnail (PID = 2)
 2. DAP has PID, length, file number, file part, total parts in file, and data

'''

data_dict = {}

with open('CFL_beacon_def.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        title = row['Title']
        data_type = row['Data Type']
        offset = row['Offset']
        size = row['Size']
        signed = row['Signed']
        decode_conversion_function = row['Decode Conversion Function']
        encode_conversion_function = row['Encode Conversion Function']
        unit = row['Unit']
        comments = row['Comments']
        example_unencoded_X = row['Example of Unencoded X']
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
