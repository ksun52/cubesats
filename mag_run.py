import numpy as np
import datetime
import time
from pathlib import Path
import csv 
import magnetometer
import pni_rm3100


def main():
    # Instantiate Objects
    mag_device1 = pni_rm3100.PniRm3100()
    mag_device2 = pni_rm3100.PniRm3100()

    address1 = mag_device1.DeviceAddress.I2C_ADDR_HL #0x21
    address2 = mag_device2.DeviceAddress.I2C_ADDR_HH #0x23

    mag_device1.assign_device_addr(address1)
    mag_device2.assign_device_addr(address2)

    mag_device1.write_config()
    mag_device2.write_config()


    accumulated_mag = []
    recent_mag = []

    ten_second_counter = time.time() - 11
    thirty_second_counter = time.time()

    starttime = time.time()
    value = datetime.datetime.fromtimestamp(starttime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')
    filename = f"all_imu_data_{date}"

    csv_file = create_mag_all_file(filename)

    while True:

        mag1_readings = mag_device1.read_meas()
        mag2_readings = mag_device2.read_meas()

        x_mag1 = mag1_readings[0]
        y_mag1 = mag1_readings[1]
        z_mag1 = mag1_readings[2]
        x_mag2 = mag2_readings[0]
        y_mag2 = mag2_readings[1]
        z_mag2 = mag2_readings[2]
         
        recent_mag = [x_mag1, y_mag1, z_mag1, x_mag2, y_mag2, z_mag2]
        accumulated_mag.append(recent_mag)
        
        if time.time() - ten_second_counter > 10:
            ten_second_counter = time.time()

            with open("mag_data/recent_mag.csv", mode='w') as file:
                writer = csv.writer(file)
                writer.writerow([0 if data is None else data for data in recent_mag])

        if time.time() - thirty_second_counter > 30:
            thirty_second_counter = time.time()
            with open(csv_file, mode='a') as file:
                writer = csv.writer(file)
                for mag_dataset in accumulated_mag:
                    writer.writerow([0 if data is None else data for data in mag_dataset])

        time.sleep(0.027)   # 37 Hz 


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
        csvwriter.writerow(["Mag1X", "Mag1Y", "Mag1Z", "Mag2X", "Mag2Y", "Mag2Z"])
    
    return csv_file

if __name__ == "__main__":
    main()