import os
import csv
import time 
import datetime
import subprocess
import temperature
# import gps
from pathlib import Path
import get_pdu_data
import magnetometer

def main():
    starttime = time.time()
    value = datetime.datetime.fromtimestamp(starttime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')
    filename = f"telemetry_{date}.csv"

    csv_file = create_file(filename) # returns a path to the CSV file we need to write to 

    i = 0
    while(True):
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
        except:
            UnixTime = None
        data_dict["UnixTime"] = UnixTime
        
        #GET CPU TEMPERATURE (in celsius)
        try:
            CPUTemp = cpu_temperature()
        except:
            CPUTemp = None
        data_dict["CPUTemp"] = CPUTemp
        
        #GET MEMORY DATA 
        try:
            UsedRam = mem_data()
        except:
            UsedRam = None
        data_dict["UsedRam"] = UsedRam

        # GET STORAGE DATA
        try:
            FreeMemory = storage_data()
        except:
            FreeMemory = None
        data_dict["FreeMemory"] = FreeMemory

        # GET BATTERY TEMPS
        try:
            BatteryTemp1 = temperature.sensor_temp(0x48)
        except:
            BatteryTemp1 = None
        try: 
            BatteryTemp2 = temperature.sensor_temp(0x49)
        except:
            BatteryTemp2 = None

        data_dict["BatteryTemp1"] = BatteryTemp1
        data_dict["BatteryTemp2"] = BatteryTemp2

        # GET GPS DATA
        # lat, lon, vel = gps.gpsdata()
        GPSLat, GPSLatNS, GPSLn, GPSLonEW, GPSAlt, GPSVelocity = [None] * 6
       

        # GET EPS DATA - pass in data_dict to add to it
        get_pdu_data.get_eps_dict(data_dict)

        # GET MAGNETOMETER DATA
        try:
            Mag1X, Mag1Y, Mag1Z = magnetometer.get_mag_data(0x21)
        except:
            Mag1X, Mag1Y, Mag1Z = [None] * 3
        try:
            Mag2X, Mag2Y, Mag2Z = magnetometer.get_mag_data(0x23)
        except:
            Mag2X, Mag2Y, Mag2Z = [None] * 3
        data_dict["Mag1X"] = Mag1X
        data_dict["Mag1Y"] = Mag1Y
        data_dict["Mag1Z"] = Mag1Z
        data_dict["Mag2X"] = Mag2X
        data_dict["Mag2Y"] = Mag2Y
        data_dict["Mag2Z"] = Mag2Z
        
        # WRITE TO CSV 
        write_line(data_dict, csv_file)

        # data collection runs once every 10 seconds
        # remove the time taken by code to execute 
        time.sleep(4.0 - ((time.time() - starttime) % 4.0))

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

def get_BME_temp():
    try:
        sensor_temp1 = temperature.sensor_temp(0x48)
    except:
        sensor_temp1 = None
    try: 
        sensor_temp2 = temperature.sensor_temp(0x49)
    except:
        sensor_temp2 = None

    BMEtemp = 0
    num_valid = 0
    if sensor_temp1 is not None:
        BMEtemp += sensor_temp1
        num_valid += 1
    if sensor_temp2 is not None: 
        BMEtemp += sensor_temp1
        num_valid += 1
    BMEtemp = None if num_valid == 0 else BMEtemp/num_valid
    
    return BMEtemp




# used for memory and storage data
def strip_shell_result(shell_result):
    """Strips whitespace and returns list for shell output"""
    lines = shell_result.strip().split('\n')
    data = lines[1].split()
    return data


def create_file(filename):
    csv_file = Path("telemetry", filename)
    counter = 1
    
    while csv_file.exists():
        new_name = f"{filename}_({counter})"
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

if __name__ == "__main__":
    main()
