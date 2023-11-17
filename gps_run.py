# old name - NEONM9NCheckoutNew
# Not a full unit checkout. Just getting meausrmeents from sensor
from smbus2 import SMBus
import time
import ublox_gps
import serial
import datetime
from pathlib import Path
import csv 
import pdb
import utils

# bus = SMBus(1)
# def readyBytes():
#     highByte = bus.read_byte_data(0x42, 0xfe) << 8
#     lowByte = bus.read_byte_data(0x42, 0xfd)
    
#     return highByte + lowByte

# def i2cReadPeriodic():

#     spareString = ""
#     while True:
#         time.sleep(1)
#         bytesReady = readyBytes()

#         if bytesReady:
#             NMEA = []
#             #numReads = bytesReady//32 + 1
#             for count in range(10):
#                 tempBytes = bus.read_i2c_block_data(0x42, 0xff, 32)
#                 NMEA += tempBytes

#             NMEAstring = []
#             for val in NMEA:
#                 if val < 255:
#                     NMEAstring.append(val)

#             NMEAstring = spareString + ''.join(chr(c) for c in NMEAstring)
#             for c in range(len(NMEAstring)-1, -1, -1):
#                 if ord(NMEAstring[c]) == 36:
#                     spareString = NMEAstring[c:-1]
#                     break

#             print(NMEAstring, "\n")

# def i2cReadContinuous():
#     NMEAString = ""
#     while True:
#         #time.sleep(0.05)
#         NMEAbyte = bus.read_byte(0x42)
        
#         if NMEAbyte == 36:
#             print(NMEAString)
#             NMEAString = ""
#             NMEAString += chr(NMEAbyte)
#         elif NMEAbyte < 255:
#             NMEAString += chr(NMEAbyte)


# RETURN A GPS REFERENCE TO PULL NMEA STRINGS FROM 
def initGPS():
    ser = serial.Serial("/dev/ttyS0", 38400)
    gps = ublox_gps.UbloxGps(ser)
    return gps


# USE FOR CONTINUOUS UPDATE TO DATA
def UARTRead():
    try:
        starttime = time.time()
        value = datetime.datetime.fromtimestamp(starttime)
        date = value.strftime('%Y-%m-%d_%H:%M:%S')

        LOGGER = utils.create_logger(logger_name="gps_logger", logfolder="gps", logfile_name=f"gps_logger_{date}")

        LOGGER.info("Starting up GPS")
        ser = serial.Serial("/dev/ttyS0", 38400)
        gps = ublox_gps.UbloxGps(ser)

        gnrmc_string = ""
        gngga_string = ""
        gpgsv_string = ""
        lon = ""
        lat = ""
        speed_knots = 0
        speed_kmh = 0
        fix_quality = ""
        altitude = ""
        snr = ""

        accumulated_gps = []
        recent_gps = [lon, lat, speed_kmh, fix_quality, altitude, snr]

        update_data_counter = time.time()
        thirty_second_counter = time.time()

        filename = f"all_gps_data_{date}"
        csv_file = create_gps_all_file(filename)
        LOGGER.info("Created GPS data file")

        while True:
            NMEA = gps.stream_nmea(wait_for_nmea = False)

            extract_time = time.time()
            # pdb.set_trace()
            if NMEA == None:
                LOGGER.info("No NMEA - wait longer")
                time.sleep(2)
                continue

            # print(NMEA)

            # Update the GPS parameters gotten from the NMEA string
            # Check if the NMEA string starts with GNRMC, GNGGA, or GPGSV
            if NMEA.startswith('$GNRMC'):
                gnrmc_string = NMEA
                split_parts = gnrmc_string.split(',')

                # Extract the required parts
                lon = split_parts[3] + ' ' + split_parts[4] if (split_parts[3] != '' and split_parts[4] != '') else ''
                lat = split_parts[5] + ' ' + split_parts[6] if (split_parts[5] != '' and split_parts[6] != '') else ''
                speed_knots = float(split_parts[7]) if split_parts[7] != "" else 0
                speed_kmh = speed_knots * 1.852  # Convert knots to km/h
                LOGGER.info("Getting info from $GNRMC NMEA")

            elif NMEA.startswith('$GNGGA'):
                gngga_string = NMEA
                split_parts_2 = gngga_string.split(',')
                
                # Extract the required parts
                fix_quality = split_parts_2[6]
                altitude = split_parts_2[9] + ' ' + split_parts_2[10] if (split_parts_2[9] != '' and split_parts_2[10] != '') else ''

                # print(gngga_string)
                LOGGER.info("Getting info from $GNGGA NMEA")

            elif NMEA.startswith('$GPGSV'):
                gpgsv_string = NMEA
                split_parts_3 = gpgsv_string.split(',')

                # Extract the required parts
                snr = split_parts_3[7]
                LOGGER.info("Getting info from $GPGSV NMEA")
            
            recent_gps = [extract_time, lon, lat, speed_kmh, fix_quality, altitude, snr]
            accumulated_gps.append(recent_gps)

            # TODO: change time 
            if extract_time - update_data_counter > 5:
                update_data_counter = extract_time

                with open("gps_data/recent_gps.csv", mode='w') as file:
                    writer = csv.writer(file)
                    writer.writerow(recent_gps)

                LOGGER.info("Wrote recent results to shared file")

                # write watchdog status 
                with open("watcher/gps_watch.txt", mode='w') as file:
                    file.write(str(time.time()))
                
                LOGGER.info("Updated status to watchdog")

            # pdb.set_trace()
            if extract_time - thirty_second_counter > 30:
                thirty_second_counter = extract_time
                with open(csv_file, mode='a') as file:
                    writer = csv.writer(file)
                    for gps_dataset in accumulated_gps:
                        writer.writerow(gps_dataset)
                LOGGER.info("Dumped 30 seconds of gps data to data file")

            time.sleep(1.5)
    except Exception as e:
        LOGGER.info(f"gps error: {e}")

        # # Print the strings if needed
        # # print("GNRMC:", gnrmc_string)
        # # print("GNGGA:", gngga_string)
        # # print("GPGSV:", gpgsv_string)
        # # Print the combined parts
        
        # print("Longitude:", lon)
        # print("Latitude:", lat)
        # print("Speed:", speed_kmh)
        # print("Fix Quality:", fix_quality)
        # print("Altitude:", altitude)
        # print("SNR:", snr)
    

def create_gps_all_file(filename):
    csv_file = Path("gps_data", f'{filename}.csv')
    counter = 1
    
    while csv_file.exists():
        new_name = f"{filename}_({counter}).csv"
        csv_file = Path("gps_data", new_name)
        counter += 1

    with open(csv_file, 'w', newline='') as csvfile:
        # Write the header row
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(["UnixTime", "Longitude", "Latitude", "Speed", "Fix Quality", "Altitude", "SNR"])
    
    return csv_file

#i2cReadPeriodic()
if __name__ == "__main__":
    UARTRead()