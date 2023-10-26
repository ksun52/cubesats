from socket import create_connection
from datetime import datetime
from os import _exit
import time
from decode import decode_rap

KISS_FEND = b'\xC0'
KISS_FESC = b'\xDB'
KISS_TFEND = b'\xDC'
KISS_TFESC = b'\xDD'
SYNC_CHARS = bytearray(b'\xAB\xCD')

BEACON_FLAG = 0x03

def remove_kiss_framing(packet):
    return packet.strip(KISS_FEND).replace(KISS_FESC + KISS_TFEND, KISS_FEND).replace(KISS_FESC + KISS_TFESC, KISS_FESC)

def listen():
    try:
        while True:
            sock = create_connection(('127.0.0.1', 12600))

            while True:
                packet = sock.recv(4096)
                if not packet:
                    break
                sync_index = packet.find(SYNC_CHARS)
                if sync_index < 0:
                    continue

                sid = packet[sync_index+4:sync_index+6]
                sid = int.from_bytes(bytes(sid), byteorder='big')
                print("Packet from sid {}:".format(sid))
                print(packet, '\n\n')

                if sid == 69:
                    with open("golf_beacons.txt", 'a') as f:
                        f.write(packet.hex() + '\n\n')
                elif sid == 42:
                    with open("hotel_beacons.txt", 'a') as f:
                        f.write(packet.hex() + '\n\n')
                        
                #packet = remove_kiss_framing(packet)
                #packet, rap, pid, sid, rap_type = decode_rap(packet)
            
                #if rap_type in BEACON_FLAG:
                #    print(packet)

                #    with open("rawbeacons.txt", 'a') as f:
                #        f.write(packet.hex() + '\n')

    except Exception as e:
        print(e)
        _exit(1)

listen()
