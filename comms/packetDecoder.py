# take in txt file
import binascii
import pdb

def extract_bytes(hex_string):
    # Convert the hex string to bytes
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

# First, create a list of just image data
for byte_array in result:
    PID = byte_array[0] # type int
    length = int.from_bytes(byte_array[1:2],byteorder='little')
    file_num = int.from_bytes(byte_array[3:4],byteorder='little')
    file_part = int.from_bytes(byte_array[5:6],byteorder='little')
    total_parts = int.from_bytes(byte_array[7:8],byteorder='little')    
    data = byte_array[9:]

    #pdb.set_trace()
    
    # See if we have an image
    if PID == 69:
        image_dict[str(file_num)] = {
            'Length': length,
            'File Part': file_part,
            'Total Parts': total_parts,
            'Data': data
        }

for outer_key, inner_dict in image_dict.items():
    if 


       

#for byte_array in image_byte_array:
    #print(byte_array[0])
    #print(int.from_bytes(byte_array[0],byteorder='little'))
        

# Print the result (list of byte arrays)
# for i, byte_array in enumerate(result):
#     print(f"Packet {i + 1}: {byte_array}")



# with open('reconstructed_image.jpg','wb') as image_file:
#     image_file.write(byte_array)