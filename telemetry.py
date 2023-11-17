import os
import csv
import time 
import datetime
import subprocess
import temperature
# import gps
from pathlib import Path
import get_pdu_data
import pdb
import logging
import utils
import psutil
import re

def main():
    try:
        # GET STARTTIME 
        starttime = time.time()
        value = datetime.datetime.fromtimestamp(starttime)
        date = value.strftime('%Y-%m-%d_%H:%M:%S')

        LOGGER = utils.create_logger(logger_name="telem_logger", logfolder="telem", logfile_name=f"telem_logger_{date}")

        LOGGER.info("Starting up telemetry program")
        
        filename = f"telemetry_{date}"
        csv_file = create_file(filename) # returns a path to the CSV file we need to write to 
        LOGGER.info("Created telemetry file")

        i = 0
        while(True):
            LOGGER.info("NEW TELEMETRY DATA CYCLE")

            # STORE RAW DATA, BEACON REAL UNITS 
            data_dict = {
                "UnixTime": None,
                "PacketCount": None,
                "GyroX": None,
                "GyroY": None,
                "GyroZ": None,
                "AccelX": None,
                "AccelY": None,
                "AccelZ": None,
                "MagX": None,
                "MagY": None,
                "MagZ": None,
                "BatteryTemp1": None,
                "BatteryTemp2": None,
                "BMETemp": None,
                "BMEPressure": None,
                "BMEHumidity": None,
                "UsedRam": None,
                "FreeMemory": None,
                "CPULoad": None,
                "CPUTemp": None,
                "BattRawVoltage": None,
                "BattRawCurrent": None,
                "V3v3": None,
                "I3v3": None,
                "V5v0": None,
                "I5v0": None,
                "VvBatt": None,
                "IvBatt": None,
                "RegTemp3v3": None,
                "RegTemp5v0": None,
                "GPSLat": None,
                "GPSLatNS": None,
                "GPSLn": None,
                "GPSLonEW": None,
                "GPSAlt": None,
                "GPSVelocity": None,
                "GPSFixQual": None,
                "Mag1X": None,
                "Mag1Y": None,
                "Mag1Z": None,
                "Mag2X": None,
                "Mag2Y": None,
                "Mag2Z": None
            }

            # TIME
            try: 
                UnixTime = time.time()
                LOGGER.info("got unix time")
            except Exception as e:
                UnixTime = None
                LOGGER.info("unix time error: {e}")
            data_dict["UnixTime"] = UnixTime

            
            #GET CPU TEMPERATURE (in celsius)
            try:
                CPUTemp = cpu_temperature()
            except Exception as e:
                CPUTemp = None
                LOGGER.info(f"cpu temp error: {e}")
            data_dict["CPUTemp"] = CPUTemp

            #GET CPU LOAD (in percent)
            try:
                CPULoad = get_cpu_load()
            except Exception as e:
                CPULoad = None
                LOGGER.info(f"cpu load error: {e}")
            data_dict["CPULoad"] = CPULoad
            
            #GET MEMORY DATA 
            try:
                UsedRam = mem_data()
            except Exception as e:
                UsedRam = None
                LOGGER.info(f"used ram error: {e}")
            data_dict["UsedRam"] = UsedRam

            # GET STORAGE DATA
            try:
                FreeMemory = storage_data()
            except Exception as e:
                FreeMemory = None
                LOGGER.info(f"free mem error: {e}")
            data_dict["FreeMemory"] = FreeMemory

            LOGGER.info("got CPU info")

            # GET BATTERY TEMPS
            try:
                BatteryTemp1 = temperature.sensor_temperature(0x48)
                LOGGER.info("got battery1 temperature info")
            except Exception as e:
                BatteryTemp1 = None
                LOGGER.info(f"temp sensor 1 error: {e}")
            try: 
                BatteryTemp2 = temperature.sensor_temperature(0x49)
                LOGGER.info("got battery2 temperature info")
            except Exception as e:
                BatteryTemp2 = None
                LOGGER.info(f"temp sensor 2 error: {e}")

            data_dict["BatteryTemp1"] = BatteryTemp1
            data_dict["BatteryTemp2"] = BatteryTemp2

            

            # GET GPS DATA
            # lat, lon, vel = gps.gpsdata()
            # GPSLat, GPSLatNS, GPSLn, GPSLonEW, GPSAlt, GPSVelocity = [None] * 6
            GPS_SNR = 0
            try:
                with open('gps_data/recent_gps.csv', 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        lat_results = extract_gps_lat(row[1])
                        lon_results = extract_gps_lon(row[2])
                        data_dict["GPSLat"] = lat_results[0]
                        data_dict["GPSLatNS"] = lat_results[1]
                        data_dict["GPSLn"] = lon_results[0]
                        data_dict["GPSLonEW"] = lon_results[1]
                        data_dict["GPSAlt"] = extract_gps_alt(row[5])
                        data_dict["GPSVelocity"] = float(row[3]) if row[3] != '' else 0
                        data_dict["GPSFixQual"] = float(row[4]) if row[4] != '' else 0
                        GPS_SNR = float(row[6]) if row[6] != '' else 0
                LOGGER.info("got gps info")
            except Exception as e:
                LOGGER.info(f"gps data error: {e}")


            # GET EPS DATA - pass in data_dict to add to it
            try:
                get_pdu_data.get_eps_dict(data_dict)
                LOGGER.info("got eddy PDU info")
            except Exception as e:
                LOGGER.info(f"eddy error: {e}")
        

            # GET IMU DATA - pass in data_dict to add to it
            # get_imu_data.get_imu_dict(data_dict)
            try:
                with open('imu_data/recent_imu.csv', 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        data_dict["GyroX"] = float(row[0])
                        data_dict["GyroY"] = float(row[1])
                        data_dict["GyroZ"] = float(row[2])
                        data_dict["AccelX"] = float(row[3])
                        data_dict["AccelY"] = float(row[4])
                        data_dict["AccelZ"] = float(row[5])
                        data_dict["MagX"] = float(row[6])
                        data_dict["MagY"] = float(row[7])
                        data_dict["MagZ"] = float(row[8])
                LOGGER.info("got imu info")
            except Exception as e:
                LOGGER.info(f"imu data error: {e}")
            

            try:
                with open('bme_data/recent_bme.csv', 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        data_dict["BMETemp"] = float(row[0])
                        data_dict["BMEPressure"] = float(row[1])
                        data_dict["BMEHumidity"] = float(row[2])
                LOGGER.info("got bme info")
            except Exception as e:
                LOGGER.info(f"bme data error: {e}")
            

            try:
                with open('mag_data/recent_mag.csv', 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        data_dict["Mag1X"] = float(row[0])
                        data_dict["Mag1Y"] = float(row[1])
                        data_dict["Mag1Z"] = float(row[2])
                        data_dict["Mag2X"] = float(row[3])
                        data_dict["Mag2Y"] = float(row[4])
                        data_dict["Mag2Z"] = float(row[5])

                    LOGGER.info("got magnetometer info")
            except Exception as e:
                LOGGER.info(f"mag data error: {e}")

            
            # WRITE TO CSV 
            write_line(data_dict, csv_file)
            LOGGER.info("wrote data to csv")

            # ADD DATA TO BEACON EVERY 30 SECONDS 
            # TODO: change timing
            try:
                if i % 1 == 0:
                    create_beacon_data(data_dict)
                    LOGGER.info(f"Beaconing data")
            except Exception as e:
                LOGGER.info(f"Error with beaconing: {e}")

            # write watchdog status
            try:
                with open("watcher/telem_watch.txt", mode='w') as file:
                    file.write(str(time.time()))

                LOGGER.info("updated watchdog status")
            except Exception as e:
                LOGGER.info(f"Error with updating watchdog: {e}")


            # data collection runs once every 10 seconds
            # remove the time taken by code to execute 
            #TODO change time
            # time.sleep(10.0 - ((time.time() - starttime) % 10.0))
            time.sleep(5.0 - ((time.time() - starttime) % 5.0))
            i += 1 

    except Exception as e:
        LOGGER.info(f"Error with telemetry: {e}")


def write_line(data_dict, csv_file):
    with open(csv_file, mode='a') as file:
        writer = csv.writer(file)
        new_data = list(data_dict.values())
        writer.writerow(["None" if data is None else data for data in new_data])
    

def cpu_temperature():
    command = "vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"   # only pull out the number from string
    temp_result = float(subprocess.check_output(command, shell=True, universal_newlines=True))
    return temp_result

def get_cpu_load():
    cpu_load = psutil.cpu_percent(interval=1)
    return cpu_load

def mem_data():
    command = "free -b" # returns RAM info in bytes 
    result = subprocess.check_output(command, shell=True, universal_newlines=True)
    # parse out the necessary data
    data = strip_shell_result(result)
    total_mem = float(data[1])
    used_mem = float(data[2])
    # free_mem = float(data[3])

    return round(used_mem/total_mem * 100, 5)

def storage_data():
    command = 'df'  # returns storage info in bytes 
    result = subprocess.check_output(command, shell=True, universal_newlines=True)
    data = strip_shell_result(result)
    # total_storage = data[1]
    free_storage = data[3]
    # used_percentage = data[4]
    
    return free_storage #, total_storage



# used for memory and storage data
def strip_shell_result(shell_result):
    """Strips whitespace and returns list for shell output"""
    lines = shell_result.strip().split('\n')
    data = lines[1].split()
    return data

def extract_gps_lat(lat_info):
    if lat_info == '':
        return 0, -1

    # Define a regular expression pattern to extract degrees, minutes, and hemisphere
    pattern = re.compile(r'(\d{2})(\d{2}\.\d+) ([NS])')

    # Use the regular expression to match the pattern in the input string
    match = pattern.match(lat_info)

    if match:
        # Extract groups from the match
        degrees, minutes, hemisphere = match.groups()

        # Convert degrees and minutes to decimal
        decimal_latitude = float(degrees) + (float(minutes) / 60)

        # Adjust sign based on hemisphere
        if hemisphere.upper() == 'S':
            decimal_longitude *= -1

        hemisphere_digit = 0 if hemisphere == "N" else 1
        return decimal_latitude, hemisphere_digit
    else:
        LOGGER.info("invalid GPS latitude input format")
        return 0, -1

def extract_gps_lat(lon_info):
    if lat_info == '':
        return 0, -1
        
    # Define a regular expression pattern to extract degrees, minutes, and hemisphere
    pattern = re.compile(r'(\d{3})(\d{2}\.\d+) ([EW])')

    # Use the regular expression to match the pattern in the input string
    match = pattern.match(lon_info)

    if match:
        # Extract groups from the match
        degrees, minutes, hemisphere = match.groups()

        # Convert degrees and minutes to decimal
        decimal_longitude = float(degrees) + (float(minutes) / 60)

        # Adjust sign based on hemisphere
        if hemisphere.upper() == 'W':
            decimal_longitude *= -1

        hemisphere_digit = 0 if hemisphere == "E" else 1
        return decimal_longitude
    else:
        LOGGER.info("invalid GPS longitude input format")
        return 0, -1

def extract_gps_alt(alt_string):
    if alt_string == '':
        return 0

    # Define a regular expression pattern to extract a numeric value
    pattern = re.compile(r'([\d.]+)')

    # Use the regular expression to find the numeric value in the input string
    match = pattern.search(input_string)

    if match:
        # Extract the numeric value
        numeric_value = float(match.group())
        return numeric_value
    else:
        LOGGER.info("invalid GPS altitude input format")
        return 0





def create_file(filename):
    csv_file = Path("telemetry", f'{filename}.csv')
    counter = 1
    
    while csv_file.exists():
        new_name = f"{filename}_({counter}).csv"
        csv_file = Path("telemetry", new_name)
        counter += 1

    with open(csv_file, 'w', newline='') as csvfile:
        # Write the header row
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow(["time", "temp_result", "total_mem", "free_mem", "total_storage", "free_storage", "vol_vbatt_raw",
                            # "curr_vbatt_raw", "vol_3v3", "curr_3v3", "vol_5v0", "curr_5v0", "volt_vbatt", "curr_vbatt", "reg_temp_3v3_C", "reg_temp_3v3_F", "reg_temp_5v0_C", "reg_temp_5v0_F"]) 
        
        csvwriter.writerow(
            ["UnixTime", "PacketCount", "GyroX", "GyroY", "GyroZ", "AccelX", "AccelY", "AccelZ", "MagX", "MagY", "MagZ",
            "BatteryTemp1", "BatteryTemp2", "BMETemp", "BMEPressure", "BMEHumidity", "UsedRam", "FreeMemory", "CPULoad",
            "CPUTemp", "BattRawVoltage", "BattRawCurrent", "V3v3", "I3v3", "V5v0", "I5v0", "VvBatt", "IvBatt", "RegTemp3v3","RegTemp5v0",
            "GPSLat", "GPSLatNS", "GPSLn", "GPSLonEW","GPSAlt", "GPSVelocity","GPSSNR","Mag1X","Mag1Y","Mag1Z","Mag2X", "Mag2Y", "Mag2Z" ])
    return csv_file

def create_beacon_data(data_dict):
    curtime = time.time()
    value = datetime.datetime.fromtimestamp(curtime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')

    filename = f'telemetry_{date}'
    csv_file = Path("downlink_telem", "data.csv")

    # CONVERT THE DOWNLINK DATA INTO THE REAL UNITS
    gyr_sensitivity = 16.4  # divide
    acc_sensitivity = 2048 # divide
    imumag_sensitivity = 0.15  # multiply
    realmag_sensitivity = 75 # divide

    additional_conversions = [1] * 43
    additional_conversions[2] = 1/gyr_sensitivity
    additional_conversions[3] = 1/gyr_sensitivity
    additional_conversions[4] = 1/gyr_sensitivity
    
    additional_conversions[5] = 1/acc_sensitivity
    additional_conversions[6] = 1/acc_sensitivity
    additional_conversions[7] = 1/acc_sensitivity

    additional_conversions[8] = imumag_sensitivity
    additional_conversions[9] = imumag_sensitivity
    additional_conversions[10] = imumag_sensitivity

    additional_conversions[37] = 1/realmag_sensitivity
    additional_conversions[38] = 1/realmag_sensitivity
    additional_conversions[39] = 1/realmag_sensitivity
    additional_conversions[40] = 1/realmag_sensitivity
    additional_conversions[41] = 1/realmag_sensitivity
    additional_conversions[42] = 1/realmag_sensitivity

    with open(csv_file, 'w', newline='') as csvfile:
        # Write the header row
        csvwriter = csv.writer(csvfile)
        new_data = list(data_dict.values())
        csvwriter.writerow(["Data"])
        for i, data in enumerate(new_data):
            csvwriter.writerow([0 if data == None else data * additional_conversions[i]])


if __name__ == "__main__":
    main()
