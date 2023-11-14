import numpy as np
import datetime
import time
from pathlib import Path
import csv 
import qwiic_icm20948


def main():
    try:
        IMU = qwiic_icm20948.QwiicIcm20948()
        IMU.begin()
        # set range to max 
        IMU.setFullScaleRangeAccel(qwiic_icm20948.gpm16)
        IMU.setFullScaleRangeGyro(qwiic_icm20948.dps2000)
        acc_sensitivity = 2048 # divide
        gyr_sensitivity = 16.4  # divide
        mag_sensitivity = 0.15  # multiply

        accumulated_imu = []
        recent_imu = []

        ten_second_counter = time.time() - 11
        thirty_second_counter = time.time()

        starttime = time.time()
        value = datetime.datetime.fromtimestamp(starttime)
        date = value.strftime('%Y-%m-%d_%H:%M:%S')
        filename = f"all_imu_data_{date}"

        csv_file = create_imu_all_file(filename)

        while True:
            IMU.getAgmt()
            # get all IMU data 
            recent_imu = [IMU.gxRaw, 
                            IMU.gyRaw, 
                            IMU.gzRaw, 
                            IMU.axRaw, 
                            IMU.ayRaw,
                            IMU.azRaw, 
                            IMU.mxRaw, 
                            IMU.myRaw, 
                            IMU.mzRaw]
            accumulated_imu.append(recent_imu)
            
            # TODO: change time 
            if time.time() - ten_second_counter > 0.5:
                ten_second_counter = time.time()

                with open("imu_data/recent_imu.csv", mode='w') as file:
                    writer = csv.writer(file)
                    writer.writerow([0 if data is None else data for data in recent_imu])

                # write watchdog status 
                with open("watcher/imu_watch.txt", mode='w') as file:
                    file.write(str(time.time()))

            if time.time() - thirty_second_counter > 30:
                thirty_second_counter = time.time()
                with open(csv_file, mode='a') as file:
                    writer = csv.writer(file)
                    for imu_dataset in accumulated_imu:
                        writer.writerow([0 if data is None else data for data in imu_dataset])

            time.sleep(0.1)
    except Exception as e:
        print(f"imu error: {e}")


def create_imu_all_file(filename):
    csv_file = Path("imu_data", f'{filename}.csv')
    counter = 1
    
    while csv_file.exists():
        new_name = f"{filename}_({counter}).csv"
        csv_file = Path("imu_data", new_name)
        counter += 1

    with open(csv_file, 'w', newline='') as csvfile:
        # Write the header row
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(["gx", "gy", "gz", "ax", "ay", "az", "mx", "my", "mz"])
    
    return csv_file

if __name__ == "__main__":
    main()