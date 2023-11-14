import os
import csv
import time 
import datetime
import subprocess
import temperature
# import gps
from pathlib import Path
import get_pdu_data

def main():
    starttime = time.time()
    value = datetime.datetime.fromtimestamp(starttime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')
    filename = f"telemetry_{date}"

    csv_file = create_file(filename) # returns a path to the CSV file we need to write to 

    i = 0
    while(True):
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
            "GPSSNR": None,
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
        except Exception as e:
            UnixTime = None
            print("unix time error: {e}")
        data_dict["UnixTime"] = UnixTime
        
        #GET CPU TEMPERATURE (in celsius)
        try:
            CPUTemp = cpu_temperature()
        except Exception as e:
            CPUTemp = None
            print(f"cpu temp error: {e}")
        data_dict["CPUTemp"] = CPUTemp
        
        #GET MEMORY DATA 
        try:
            UsedRam = mem_data()
        except Exception as e:
            UsedRam = None
            print(f"used ram error: {e}")
        data_dict["UsedRam"] = UsedRam

        # GET STORAGE DATA
        try:
            FreeMemory = storage_data()
        except Exception as e:
            FreeMemory = None
            print(f"free mem error: {e}")
        data_dict["FreeMemory"] = FreeMemory

        # GET BATTERY TEMPS
        try:
            BatteryTemp1 = temperature.sensor_temperature(0x48)
        except Exception as e:
            BatteryTemp1 = None
            print(f"temp sensor 1 error: {e}")
        try: 
            BatteryTemp2 = temperature.sensor_temperature(0x49)
        except Exception as e:
            BatteryTemp2 = None
            print(f"temp sensor 2 error: {e}")

        data_dict["BatteryTemp1"] = BatteryTemp1
        data_dict["BatteryTemp2"] = BatteryTemp2

        # GET GPS DATA
        # lat, lon, vel = gps.gpsdata()
        GPSLat, GPSLatNS, GPSLn, GPSLonEW, GPSAlt, GPSVelocity = [None] * 6
       

        # GET EPS DATA - pass in data_dict to add to it
        try:
            get_pdu_data.get_eps_dict(data_dict)
        except Exception as e:
            print(f"eddy error: {e}")

        # GET IMU DATA - pass in data_dict to add to it
        # get_imu_data.get_imu_dict(data_dict)
        try:
            with open('imu_data/recent_imu.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    data_dict["GyroX"] = row[0]
                    data_dict["GyroY"] = row[1]
                    data_dict["GyroZ"] = row[2]
                    data_dict["AccelX"] = row[3]
                    data_dict["AccelY"] = row[4]
                    data_dict["AccelZ"] = row[5]
                    data_dict["MagX"] = row[6]
                    data_dict["MagY"] = row[7]
                    data_dict["MagZ"] = row[8]
        except Exception as e:
            print(f"imu data error: {e}")


        # GET BME DATA - pass in data_dict to add to it
        # try:
        #     get_bme_data.get_bme_dict(data_dict)
        # except Exception as e:
        #     print(f"bme error: {e}")
        try:
            with open('bme_data/recent_bme.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    data_dict["BMETemp"] = row[0]
                    data_dict["BMEPressure"] = row[1]
                    data_dict["BMEHumidity"] = row[2]
        except Exception as e:
            print(f"bme data error: {e}")

        try:
            with open('mag_data/recent_mag.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    data_dict["Mag1X"] = row[0]
                    data_dict["Mag1Y"] = row[1]
                    data_dict["Mag1Z"] = row[2]
                    data_dict["Mag2X"] = row[3]
                    data_dict["Mag2Y"] = row[4]
                    data_dict["Mag2Z"] = row[5]
        except Exception as e:
            print(f"mag data error: {e}")
                
        # WRITE TO CSV 
        write_line(data_dict, csv_file)

        # ADD DATA TO BEACON EVERY 30 SECONDS 
        # TODO: change timing
        if i % 1 == 0:
            create_beacon_data(data_dict)

        # write watchdog status 
        with open("watcher/telem_watch.txt", mode='w') as file:
            file.write(str(time.time()))

        # data collection runs once every 10 seconds
        # remove the time taken by code to execute 
        #TODO change time
        # time.sleep(10.0 - ((time.time() - starttime) % 10.0))
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))
        i += 1 


def write_line(data_dict, csv_file):
    with open(csv_file, mode='a') as file:
        writer = csv.writer(file)
        new_data = list(data_dict.values())
        writer.writerow(["None" if data is None else data for data in new_data])
    

def cpu_temperature():
    command = "vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"   # only pull out the number from string
    temp_result = float(subprocess.check_output(command, shell=True, universal_newlines=True))
    return temp_result



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
        for data, i in enumerate(new_data):
            csvwriter.writerow([0 if data is None else data * additional_conversions[i]])

if __name__ == "__main__":
    main()
