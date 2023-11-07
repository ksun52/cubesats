# DAP structure (bytes): PID (1), Length(2), File Number (2), File Part (2), Total Parts in File (2), Data (<1013)

from PIL import Image
import os
import csv
import binascii
import pickle

# Open the JPG image
image = Image.open("team.jpg")
image_path = "team.jpg"

# Get the size of the image in pixels
width, height = image.size

# Print the size (pixels)
print(f"Image size (width x height): {width} x {height} pixels")

# Get the mode of the image, which indicates the color depth
color_mode = image.mode

# Print the color mode
print(f"Color mode: {color_mode}")

# Get the file size in bytes
file_size_bytes = os.path.getsize(image_path)

print(f"Image size in bytes: {file_size_bytes} bytes")

# Resize the image
# Define the new size (width and height)
scale_factor = 150

new_width = int(width/scale_factor)  # Set the new width in pixels
new_height = int(height/scale_factor)  # Set the new height in pixels

# Resize the image
resized_image = image.resize((new_width, new_height))

# Save the resized image
resized_image.save("output_image.jpg")

resized_image_path = "output_image.jpg"

# Get the size of the image in pixels
width, height = resized_image.size

# Print the size (pixels)
print(f"Image size (width x height): {width} x {height} pixels")

# Get the file size in bytes
file_size_bytes = os.path.getsize(resized_image_path)

print(f"Image size in bytes: {file_size_bytes} bytes")

# Convert image to hex bytes

# Open the image
# image = Image.open("output_image.jpg")

# Convert the image to a byte array
# image_bytes = image.tobytes()

with open('output_image.jpg','rb') as file:
    image_data = file.read()

image_bytes = bytearray(image_data)
print(len(image_bytes))

# image_bytes = pickle.dumps(byte_array)
# print(image_bytes)

# CHUNK into rows of bytes <1013

def createChunks(image_bytes):

    # Split the RGB hex array into chunks
    chunks = []

    # Maximum byte array size for each chunk
    max_chunk_size = 1012
    
    for i in range(0, len(image_bytes), max_chunk_size * 2):
        chunk = image_bytes[i:i + max_chunk_size * 2]
        chunks.append(chunk)
    return chunks

# print(len(image_bytes))
# print(len(createChunks(image_bytes)))

# RECONSTRUCT IMAGE --> MOVE INTO SEPARATE FILE

# print(image_bytes)

byte_data = bytes.fromhex("abcdef01001003b40335c2ffd8ffe000104a46494600010100000100010000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333432ffdb0043010909090c0b0c180d0d1832211c213232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232ffc00011080014001b03012200021101031101ffc4001f0000010501010101010100000000000000000102030405060708090a0bffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffc4001f0100030101010101010101010000000000000102030405060708090a0bffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9faffda000c03010002110311003f00c6d375586e202f6b1c970e8c0346b1ed2339f9b736d1b7e53c923f3aafe20d56c6d9f4e8e779e07936dc3a08892133c6ef986391ef82bd3a545e14f10d9de5e2e9979033cd797518491a660539e47191b7f23d4673823d035df06c7abdf4290baa59952ae33f3a290436d6e47423008e31d4e788517b8da8ed738f924d016ca3bb05618a47548e5f21e324b0241c95181804e738c77e6aa1bfb10481afe0678c6a07ff008aabfe39baf0ae8166be1ed2a5b8865501c794fe6451a92fb918ee2c09273820ff000f4ea3c8268a3f39fcb7ca6e3b4e0f229a8b13b5ae8eb7e1fb2dc78cb4b69a28e421e561b9738210907dc83c827d07a57adde5ecf1e857b2a361d6db208edf2fff005e8a2b45f0913f88f12f1047e76a5aa4f248ecf0dd2c0a49ce570e067d4e116b0f1c9e7bd14553dd8743ffd9e2c3a4258cfc")
image_bytes = byte_data[11:-6]

with open('reconstructed_image.jpg','wb') as image_file:
    image_file.write(image_bytes)


# OLD METHOD ------------->>>>
# byte_data = b''
# for i in range(0,len(createChunks(image_bytes))):
#     byte_data = byte_data + createChunks(image_bytes)[i]

# # Create an image from the byte data
# image = Image.frombytes("RGB", (new_width, new_height), byte_data)

# # Save the image to a file (optional)
# image.save("reconstructed_image.jpg")