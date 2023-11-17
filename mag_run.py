import numpy as np
import datetime
import time
from pathlib import Path
import csv 
import pni_rm3100
import utils


def main():
    try:
        starttime = time.time()
        value = datetime.datetime.fromtimestamp(starttime)
        date = value.strftime('%Y-%m-%d_%H:%M:%S')
        
        LOGGER = utils.create_logger(logger_name="mag_logger", logfolder="mag", logfile_name=f"mag_logger_{date}")

        LOGGER.info("Starting up magnetometers")

        # create data file 
        filename = f"all_mag_data_{date}"
        csv_file = create_mag_all_file(filename)
        LOGGER.info("Created magnetometer data file")

        # Instantiate Objects
        mag_device1 = pni_rm3100.PniRm3100()
        mag_device2 = pni_rm3100.PniRm3100()

        address1 = mag_device1.DeviceAddress.I2C_ADDR_HL #0x21
        address2 = mag_device2.DeviceAddress.I2C_ADDR_HH #0x23

        mag_device1.assign_device_addr(address1)
        mag_device2.assign_device_addr(address2)

        mag_device1.write_config()
        mag_device2.write_config()

        LOGGER.info("Set special magnetomer settings")


        accumulated_mag = []
        recent_mag = []

        update_data_counter = time.time()
        thirty_second_counter = time.time()


        while True:

            mag1_readings = mag_device1.read_bytes()
            mag2_readings = mag_device2.read_bytes()

            extract_time = time.time()

            x_mag1 = to_hex_BE(mag1_readings[0])
            y_mag1 = to_hex_BE(mag1_readings[1])
            z_mag1 = to_hex_BE(mag1_readings[2])
            x_mag2 = to_hex_BE(mag2_readings[0])
            y_mag2 = to_hex_BE(mag2_readings[1])
            z_mag2 = to_hex_BE(mag2_readings[2])
            
            recent_mag = [x_mag1, y_mag1, z_mag1, x_mag2, y_mag2, z_mag2]
            recent_mag.insert(0, extract_time)
            accumulated_mag.append(recent_mag)
            
            # TODO: change time 
            if extract_time - update_data_counter > 5:
                update_data_counter = extract_time

                with open("mag_data/recent_mag.csv", mode='w') as file:
                    writer = csv.writer(file)
                    writer.writerow([0 if data is None else data for data in recent_mag])
                
                LOGGER.info("Wrote recent results to shared file")
                
                # write watchdog status 
                with open("watcher/mag_watch.txt", mode='w') as file:
                    file.write(str(time.time()))
                
                LOGGER.info("Updated status to watchdog")

            if extract_time - thirty_second_counter > 30:
                thirty_second_counter = extract_time
                with open(csv_file, mode='a') as file:
                    writer = csv.writer(file)
                    for mag_dataset in accumulated_mag:
                        writer.writerow([0 if data is None else data for data in mag_dataset])
                
                LOGGER.info("Dumped 30 seconds of magnetometer data to data file")

            time.sleep(0.027 - (extract_time - time.time()) % 0.027) # 37 Hz 

    except Exception as e:
        LOGGER.info(f"mag error: {e}")

def to_hex_BE(val):
    # data comes in as unsigned
    return val.to_bytes(length=4, byteorder='big', signed=False).hex()


def create_mag_all_file(filename):
    csv_file = Path("mag_data", f'{filename}.csv')
    counter = 1
    
    while csv_file.exists():
        new_name = f"{filename}_({counter}).csv"
        csv_file = Path("mag_data", new_name)
        counter += 1

    with open(csv_file, 'w', newline='') as csvfile:
        # Write the header row
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(["UnixTime", "Mag1X", "Mag1Y", "Mag1Z", "Mag2X", "Mag2Y", "Mag2Z"])
    
    return csv_file

if __name__ == "__main__":
    main()