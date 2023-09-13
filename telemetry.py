import csv
import time 
import subprocess
from temp_test import sensor_temperature

def main():
    starttime = time.time()
    i = 0
    while(i < 10):
        # TIME
        timestamp = time.time()
        
        #GET CPU TEMPERATURE (in celsius)
        cpu_temp = temperature()

        #GET MEMORY DATA 
        total_mem, free_mem = mem_data()

        # GET STORAGE DATA
        total_storage, free_storage = storage_data()

        # GET SENSOR TEMP
        sensor_temp = sensor_temperature()

        # WRITE TO CSV 
        data_line = [timestamp, cpu_temp, total_mem, free_mem, total_storage, free_storage, sensor_temp]
        write_line(data_line)

        # data collection runs once every 10 seconds
        # remove the time taken by code to execute 
        time.sleep(10.0 - ((time.time() - starttime) % 10.0))

        i += 1 


def write_line(new_data):
    #csv_file = "telemetry.csv"
    #with open(csv_file, mode='a') as file:
    #    writer = csv.writer(file)
    #    writer.writerow(new_data)
    print(new_data)


def temperature():
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


if __name__ == "__main__":
    main()
