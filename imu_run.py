import numpy as np
import datetime
import time
from pathlib import Path
import csv 
import qwiic_icm20948
import utils


def main():
    try:
        starttime = time.time()
        value = datetime.datetime.fromtimestamp(starttime)
        date = value.strftime('%Y-%m-%d_%H:%M:%S')

        LOGGER = utils.create_logger(logger_name="imu_logger", logfolder="imu", logfile_name=f"imu_logger_{date}")

        IMU = qwiic_icm20948.QwiicIcm20948()
        IMU.begin()
        LOGGER.info("Starting up IMU")

        # set range to max 
        IMU.setFullScaleRangeAccel(qwiic_icm20948.gpm16)
        IMU.setFullScaleRangeGyro(qwiic_icm20948.dps2000)
        acc_sensitivity = 2048 # divide
        gyr_sensitivity = 16.4  # divide
        mag_sensitivity = 0.15  # multiply

        LOGGER.info("Set special IMU settings")

        accumulated_imu = []
        recent_imu = []

        update_data_counter = time.time()
        thirty_second_counter = time.time()

        
        filename = f"all_imu_data_{date}"
        csv_file = create_imu_all_file(filename)
        LOGGER.info("Created IMU Data File")

        while True:
            get_Agmt_bytes(IMU)
            extract_time = time.time()

            # get all IMU data 
            # print([IMU.gxRaw, IMU.gyRaw, IMU.gzRaw, IMU.axRaw, IMU.ayRaw, IMU.azRaw, IMU.mxRaw, IMU.myRaw, IMU.mzRaw])
            recent_imu = [  extract_time,
                            to_hex_BE(IMU.gxRaw), 
                            to_hex_BE(IMU.gyRaw), 
                            to_hex_BE(IMU.gzRaw), 
                            to_hex_BE(IMU.axRaw), 
                            to_hex_BE(IMU.ayRaw),
                            to_hex_BE(IMU.azRaw), 
                            to_hex_LE(IMU.mxRaw), 
                            to_hex_LE(IMU.myRaw), 
                            to_hex_LE(IMU.mzRaw)]
            accumulated_imu.append(recent_imu)
            
            # TODO: change time 
            if extract_time - update_data_counter > 1:
                update_data_counter = extract_time

                with open("imu_data/recent_imu.csv", mode='w') as file:
                    writer = csv.writer(file)
                    writer.writerow([0 if data is None else data for data in recent_imu])

                LOGGER.info("Wrote recent results to shared file")

                # write watchdog status 
                with open("watcher/imu_watch.txt", mode='w') as file:
                    file.write(str(time.time()))

                LOGGER.info("Updated status to watchdog")

            if extract_time - thirty_second_counter > 30:
                thirty_second_counter = extract_time
                with open(csv_file, mode='a') as file:
                    writer = csv.writer(file)
                    for imu_dataset in accumulated_imu:
                        writer.writerow([0 if data is None else data for data in imu_dataset])

                LOGGER.info("Dumped 30 seconds of IMU data to data file")
            
            if (time.time() - starttime > 300):
                starttime = time.time()
                value = datetime.datetime.fromtimestamp(starttime)
                date = value.strftime('%Y-%m-%d_%H:%M:%S')
                filename = f"all_imu_data_{date}"
                csv_file = create_imu_all_file(filename)
                LOGGER.info("Created Additional IMU Data File")

            time.sleep(0.1 - (extract_time - time.time()) % 0.1)

    except Exception as e:
        LOGGER.info(f"imu error: {e}")


def to_hex_BE(val):
    # data comes in as unsigned
    return val.to_bytes(length=2, byteorder='big', signed=False).hex()

def to_hex_LE(val):
    # data comes in as unsigned
    return val.to_bytes(length=2, byteorder='little', signed=False).hex()


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
        csvwriter.writerow(["UnixTime", "gx", "gy", "gz", "ax", "ay", "az", "mx", "my", "mz"])
    
    return csv_file

# ----------------------------------
	# getAgmt()
	#
	# Reads and updates raw values from accel, gyro, mag and temp of the ICM90248 modul
def get_Agmt_bytes(IMU):

    """ 
        Reads and updates raw values from accel, gyro, mag and temp of the ICM90248 module

        :return: Returns True if I2C readBlock was successful, otherwise False.
        :rtype: bool

    """

    # Read all of the readings starting at AGB0_REG_ACCEL_XOUT_H
    numbytes = 14 + 9 # Read Accel, gyro, temp, and 9 bytes of mag
    IMU.setBank(0)
    buff = IMU._i2c.readBlock(IMU.address, IMU.AGB0_REG_ACCEL_XOUT_H, numbytes)

    IMU.axRaw = ((buff[0] << 8) | (buff[1] & 0xFF))
    IMU.ayRaw = ((buff[2] << 8) | (buff[3] & 0xFF))
    IMU.azRaw = ((buff[4] << 8) | (buff[5] & 0xFF))

    IMU.gxRaw = ((buff[6] << 8) | (buff[7] & 0xFF))
    IMU.gyRaw = ((buff[8] << 8) | (buff[9] & 0xFF))
    IMU.gzRaw = ((buff[10] << 8) | (buff[11] & 0xFF))

    IMU.tmpRaw = ((buff[12] << 8) | (buff[13] & 0xFF))

    IMU.magStat1 = buff[14]
    IMU.mxRaw = ((buff[16] << 8) | (buff[15] & 0xFF)) # Mag data is read little endian
    IMU.myRaw = ((buff[18] << 8) | (buff[17] & 0xFF))
    IMU.mzRaw = ((buff[20] << 8) | (buff[19] & 0xFF))
    IMU.magStat2 = buff[22]

    # check for data read error
    if buff:
        return True
    else:
        return False

if __name__ == "__main__":
    main()