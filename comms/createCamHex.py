# DAP structure (bytes): PID (1), Length(2), File Number (2), File Part (2), Total Parts in File (2), Data (<1013)

from PIL import Image
import os
import csv
import binascii
import pickle
import ast
import glob

def createCamfunc(count):
    
    # Specify the directory path
    directory_path = '/home/pi/team-papa/thumbnails'

    # Define a pattern to match
    file_pattern = '*.jpg'

    # Use glob to list jpg files in the directory
    jpg_files = glob.glob(os.path.join(directory_path, file_pattern))

    # Check if any jpg files were found
    if jpg_files:
        # Sort the list of files by modification time (newest first)
        jpg_files.sort(key=os.path.getmtime, reverse=True)

        # Get the path of the most recent jpg file
        most_recent_jpg = jpg_files[0]

        print("The most recent jpg file is:", most_recent_jpg)
    else:
        print("No jpg files found in the specified directory.")
    
    # Open the JPG image
    image = Image.open(most_recent_jpg)

    # Get the size of the image in pixels
    width, height = image.size

    # Print the size (pixels)
    print(f"Image size (width x height): {width} x {height} pixels")

    # Get the mode of the image, which indicates the color depth
    color_mode = image.mode

    # Print the color mode
    print(f"Color mode: {color_mode}")

    # Get the file size in bytes
    file_size_bytes = os.path.getsize(most_recent_jpg)

    print(f"Image size in bytes: {file_size_bytes} bytes")

    # Resize the image
    # Define the new size (width and height)
    scale_factor = 10

    new_width = int(width/scale_factor)  # Set the new width in pixels
    new_height = int(height/scale_factor)  # Set the new height in pixels

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Save the resized image
    resized_image_path = "/home/pi/team-papa/comms/transmitted_thumbnails/output_image_" + str(count)+ "_.jpg"
    resized_image.save(resized_image_path)
  
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

    with open(resized_image_path,'rb') as file:
        image_data = file.read()

    image_bytes = bytearray(image_data)
    print(len(image_bytes))
    # Split the RGB hex array into chunks
    chunks = []
    # Maximum byte array size for each chunk
    max_chunk_size = 1012
    
    for i in range(0, len(image_bytes), max_chunk_size * 2):
        chunk = image_bytes[i:i + max_chunk_size * 2]
        chunks.append(chunk)
    
    # RECONSTRUCT IMAGE --> MOVE INTO SEPARATE FILE
    
    return chunks
    
    # image_bytes = pickle.dumps(byte_array)
    # print(image_bytes)

    # CHUNK into rows of bytes <1013
    

createCamfunc(1)

# print(len(image_bytes))
# print(createChunks(image_bytes)[0])




# OLD METHOD ------------->>>>
# byte_data = b''
# for i in range(0,len(createChunks(image_bytes))):
#     byte_data = byte_data + createChunks(image_bytes)[i]

# # Create an image from the byte data
# image = Image.frombytes("RGB", (new_width, new_height), byte_data)

# # Save the image to a file (optional)
# image.save("reconstructed_image.jpg")