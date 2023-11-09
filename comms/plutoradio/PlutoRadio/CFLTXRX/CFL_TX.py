import time
from socket import create_connection
from encode import encode_rap
import sys
sys.path.append('/home/pi/code/team-papa/comms')
from createDataHex import createDataHexfunc
from createCamHex import createCamfunc


# Socket-level communications between the radio and the beaconing program uses KISS protocol. These
#   constants are header and footer bytes for packets sent to the radio software

KISS_FEND = b'\xC0'
KISS_FESC = b'\xDB'
KISS_TFEND = b'\xDC'
KISS_TFESC = b'\xDD'

# Your transmissions will be in the form of a RAP packet. This is the flag for a beacon, as seen
#   in RAXRadioPacketFormat.pdf
BEACON_FLAG = 0x03

def add_kiss_framing(packet, port):
    # Function used to add kiss bytes to a packet
    cmd_bytes = bytes.fromhex(str(port) + '0')
    return KISS_FEND + cmd_bytes + packet.replace(KISS_FESC, KISS_FESC + KISS_TFESC).replace(
        KISS_FEND, KISS_FESC + KISS_TFEND) + KISS_FEND

def send():
    # Keeping track of number of beacons sent
    count = 0
    while True:
        # Only current RAP type is beacon
        # Future iterations may send other types of packets

        # Example beacon. You can mdo the code here and elsewhere as necessary, to customize your
        #   team's beacon
        # beacon = bytearray(b'\x53\x74\x72\x61\x74\x6f\x53\x61\x74')
        # beacon = bytearray(b'\xd1\x916eG\x00\xbe\xfb\xaf\xfb\xec\xfc\x80\xfe\x80\x00\x10\x08\xda\xffN\x00E\x01e\x81\x00\x00u\xa8\x00\x00\xf8\xfe\x0c\x00\x00\x00N\x01\x00\x00h\x10\x99\x89_.\xa0#\xf0\x01\x14,\x7f\r\xe8\x0ct\x01y\x13\xd1\x16\x0f,f\r\xe8\x04>\x06\xbas\x06\x00\x00\xbb\xc5\x0c\x00\x01`=\x03\x00d\x006\xe0\x15\x00\x00\xe3\xf1\xff\xff\xc5\xb5\x00\x00h\xf2\xff\xff\xb89\xff\xff\x98\xea\xff\xff')
        beacon_created = createDataHexfunc()
        beacon = bytearray(beacon_created)

        #beacon+= count.to_bytes(1, 'little')

        # Adding RAP packets
        rap = encode_rap(BEACON_FLAG, beacon)

        # Creates a socket object to communicate with the radio software. 127.0.0.1 is your local
        #   computer's IP. 12600 is the TCP port the radio software is listening on
        # Amal's computer's current IP address
        sock = create_connection(('127.0.0.1', 12600))
        kiss_port = 1
        
        # Adding kiss_framing
        packet = add_kiss_framing(rap, kiss_port)
        
        print(packet.hex())
        
        # Sending the betys 
        sock.sendall(packet)
        #print(count, count.to_bytes(1,'little').hex())
        print(count)
        count += 1

        # Beacon frequency: sends beacons every 30 seconds 
        time.sleep(10)

        chunks = createCamfunc()

        for i in len(chunks):
            beacon_created = chunks(i)
            beacon = bytearray(beacon_created)

            #beacon+= count.to_bytes(1, 'little')

            # Adding RAP packets
            rap = encode_rap(BEACON_FLAG, beacon)

            # Creates a socket object to communicate with the radio software. 127.0.0.1 is your local
            #   computer's IP. 12600 is the TCP port the radio software is listening on
            # Amal's computer's current IP address
            sock = create_connection(('127.0.0.1', 12600))
            kiss_port = 1
            
            # Adding kiss_framing
            packet = add_kiss_framing(rap, kiss_port)
            
            print(packet.hex())
            
            # Sending the betys 
            sock.sendall(packet)
            #print(count, count.to_bytes(1,'little').hex())
            print(count)
            count += 1

            # Beacon frequency: sends beacons every 30 seconds 
            time.sleep(10)
        time.sleep(10)
send()


# import time
# from socket import create_connection
# from encode import encode_rap
# import sys

# # Add the directory containing file1 to sys.path
# sys.path.append('~/code/team-papa/comms/createCamHex.py')

# # Socket-level communications between the radio and the beaconing program uses KISS protocol. These
# #   constants are header and footer bytes for packets sent to the radio software

# KISS_FEND = b'\xC0'
# KISS_FESC = b'\xDB'
# KISS_TFEND = b'\xDC'
# KISS_TFESC = b'\xDD'

# # Your transmissions will be in the form of a RAP packet. This is the flag for a beacon, as seen
# #   in RAXRadioPacketFormat.pdf
# BEACON_FLAG = 0x03

# def add_kiss_framing(packet, port):
#     # Function used to add kiss bytes to a packet
#     cmd_bytes = bytes.fromhex(str(port) + '0')
#     return KISS_FEND + cmd_bytes + packet.replace(KISS_FESC, KISS_FESC + KISS_TFESC).replace(
#         KISS_FEND, KISS_FESC + KISS_TFEND) + KISS_FEND

# def send():
#     # Keeping track of number of beacons sent
#     count = 0
#     while True:
#         # Only current RAP type is beacon
#         # Future iterations may send other types of packets

#         # Example beacon. You can mdo the code here and elsewhere as necessary, to customize your
#         #   team's beacon
#         #beacon = bytearray(b'\xd1\x916eG\x00\xbe\xfb\xaf\xfb\xec\xfc\x80\xfe\x80\x00\x10\x08\xda\xffN\x00E\x01e\x81\x00\x00u\xa8\x00\x00\xf8\xfe\x0c\x00\x00\x00N\x01\x00\x00h\x10\x99\x89_.\xa0#\xf0\x01\x14,\x7f\r\xe8\x0ct\x01y\x13\xd1\x16\x0f,f\r\xe8\x04>\x06\xbas\x06\x00\x00\xbb\xc5\x0c\x00\x01`=\x03\x00d\x006\xe0\x15\x00\x00\xe3\xf1\xff\xff\xc5\xb5\x00\x00h\xf2\xff\xff\xb89\xff\xff\x98\xea\xff\xff')
        
#         beacon = bytearray(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xdb\x00C\x01\t\t\t\x0c\x0b\x0c\x18\r\r\x182!\x1c!22222222222222222222222222222222222222222222222222\xff\xc0\x00\x11\x08\x00\x14\x00\x1b\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xc6\xd3uXn /k\x1c\x97\x0e\x8c\x03F\xb1\xed#9\xf9\xb76\xd1\xb7\xe5<\x92?:\xaf\xe2\rV\xc6\xd9\xf4\xe8\xe7y\xe0y6\xdc:\x08\x89!3\xc6\xef\x98c\x91\xef\x82\xbd:T^\x14\xf1\r\x9d\xe5\xe2\xe9\x97\x903\xcdyu\x18I\x1af\x059\xe4q\x91\xb7\xf2=Fs\x82=\x03]\xf0lz\xbd\xf4)\x0b\xaaY\x95*\xe3?:)\x046\xd6\xe4t#\x00\x8e1\xd4\xe7\x88Q{\x8d\xa8\xeds\x8f\x92M\x01l\xa3\xbb\x05a\x8aGT\x8e_!\xe3$\xb0$\x1c\x95\x18\x18\x04\xe78\xc7~j\xa1\xbf\xb1\x04\x81\xaf\xe0g\x8cj\x07\xff\x00\x8a\xab\xfe9\xba\xf0\xae\x81f\xbe\x1e\xd2\xa5\xb8\x86U\x01\xc7\x94\xfedQ\xa9/\xb9\x18\xee,\t\'8 \xff\x00\x0fN\xa3\xc8&\x8a?9\xfc\xb7\xcan;N\x0f"\x9a\x8b\x13\xb5\xae\x8e\xb7\xe1\xfb-\xc7\x8c\xb4\xb6\x9a(\xe4!\xe5a\xb9s\x82\x10\x90}\xc8<\x82}\x07\xa5z\xdd\xe5\xec\xf1\xe8W\xb2\xa3a\xd6\xdb \x8e\xdf/\xff\x00^\x8a+E\xf0\x91?\x88\xf1/\x10G\xe7jZ\xa4\xf2H\xec\xf0\xdd,\nI\xceW\x0e\x06}N\x11k\x0f\x1c\x9e{\xd1ES\xdd\x87C\xff\xd9')
#         #beacon+= count.to_bytes(1, 'little')

#         # Adding RAP packets
#         rap = encode_rap(BEACON_FLAG, beacon)

#         # Creates a socket object to communicate with the radio software. 127.0.0.1 is your local
#         #   computer's IP. 12600 is the TCP port the radio software is listening on
#         sock = create_connection(('127.0.0.1', 12600))
#         kiss_port = 1
        
#         # Adding kiss_framing
#         packet = add_kiss_framing(rap, kiss_port)
        
#         print(packet.hex())
        
#         # Sending the betys 
#         sock.sendall(packet)
#         #print(count, count.to_bytes(1,'little').hex())
#         print(count)
#         count += 1

#         # Beacon frequency
#         time.sleep(1)

# send()


