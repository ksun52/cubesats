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
    filename = f"telemetry_{date}.csv"

    csv_file = create_file(filename) # returns a path to the CSV file we need to write to 

    i = 0
    while(True):
        # TIME
        timestamp = time.time()
        
        #GET CPU TEMPERATURE (in celsius)
        try:
            cpu_temp = cpu_temperature()
        except:
            cpu_temp = None
        

        #GET MEMORY DATA 
        try:
            total_mem, free_mem = mem_data()
        except:
            total_mem, free_mem = None, None

        # GET STORAGE DATA
        try:
            total_storage, free_storage = storage_data()
        except:
            total_storage, free_storage = None

        # GET SENSOR TEMP
        try:
            sensor_temp = temperature.sensor_temp()
        except:
            sensor_temp = None

        # GET GPS DATA
        # lat, lon, vel = gps.gpsdata()
        lat, lon, vel = None, None, None

        # GET EPS DATA    monica added all of this, might cause error
        eps_telem_list = get_pdu_data.eps_data_organization()

        # WRITE TO CSV 
        data_line = [timestamp, cpu_temp, total_mem, free_mem, total_storage, free_storage, sensor_temp, lat, lon, vel]
        data_line = data_line + eps_telem_list
        write_line(data_line, csv_file)

        # data collection runs once every 10 seconds
        # remove the time taken by code to execute 
        time.sleep(4.0 - ((time.time() - starttime) % 4.0))

        i += 1 


def write_line(new_data, csv_file):
    with open(csv_file, mode='a') as file:
       writer = csv.writer(file)
    #    writer.writerow(new_data)
       writer.writerow(["None" if data is None else data for data in new_data])
    


def cpu_temperature():
    command = "vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"   # only pull out the number from string
    temp_result = float(subprocess.check_output(command, shell=True, universal_newlines=True))
    return temp_result



def mem_data():
    command = "free -m"
    result = subprocess.check_output(command, shell=True, universal_newlines=True)
    # parse out the necessary data
    data = strip_shell_result(result)
    total_mem = float(data[1])
    free_mem = float(data[3])
    #print(Total_Mem)
    #print(Free_Mem)

    return total_mem, free_mem


"""
TO DO - just use df and free and figure out what unit those are in (that is just the raw data)
"""
def storage_data():
    command = 'df -h'
    result = subprocess.check_output(command, shell=True, universal_newlines=True)
    data = strip_shell_result(result)
    total_storage = data[1]
    free_storage = data[3]
    #print(total_storage)
    #print(free_storage)

    return total_storage, free_storage


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
        csvwriter.writerow(["time", "temp_result", "total_mem", "free_mem", "total_storage", "free_storage", "vol_vbatt_raw",
                            "curr_vbatt_raw", "vol_3v3", "curr_3v3", "vol_5v0", "curr_5v0", "volt_vbatt", "curr_vbatt", "reg_temp_3v3_C", "reg_temp_3v3_F", "reg_temp_5v0_C", "reg_temp_5v0_F"]) 

    return csv_file

if __name__ == "__main__":
    main()
