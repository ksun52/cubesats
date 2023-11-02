import time
from socket import create_connection
from encode import encode_rap

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
        beacon = bytearray(b'\xd1\x916eG\x00\xbe\xfb\xaf\xfb\xec\xfc\x80\xfe\x80\x00\x10\x08\xda\xffN\x00E\x01e\x81\x00\x00u\xa8\x00\x00\xf8\xfe\x0c\x00\x00\x00N\x01\x00\x00h\x10\x99\x89_.\xa0#\xf0\x01\x14,\x7f\r\xe8\x0ct\x01y\x13\xd1\x16\x0f,f\r\xe8\x04>\x06\xbas\x06\x00\x00\xbb\xc5\x0c\x00\x01`=\x03\x00d\x006\xe0\x15\x00\x00\xe3\xf1\xff\xff\xc5\xb5\x00\x00h\xf2\xff\xff\xb89\xff\xff\x98\xea\xff\xff')
        #beacon+= count.to_bytes(1, 'little')

        # Adding RAP packets
        rap = encode_rap(BEACON_FLAG, beacon)

        # Creates a socket object to communicate with the radio software. 127.0.0.1 is your local
        #   computer's IP. 12600 is the TCP port the radio software is listening on
        # Amal's computer's current IP address
        sock = create_connection(('127.0.0.1', 631))
        kiss_port = 1
        
        # Adding kiss_framing
        packet = add_kiss_framing(rap, kiss_port)
        
        print(packet.hex())
        
        # Sending the betys 
        sock.sendall(packet)
        #print(count, count.to_bytes(1,'little').hex())
        print(count)
        count += 1

        # Beacon frequency
        time.sleep(1)

send()
