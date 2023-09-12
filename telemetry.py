import csv
import subprocess

def main():
    # GET CPU TEMPERATURE (in celsius)
    command = "vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"   # only pull out the number from string
    temp_result = float(subprocess.check_output(command, shell=True, universal_newlines=True))

    # GET MEMORY DATA 
    command = "free -m"
    result = subprocess.check_output(command, shell=True, universal_newlines=True)
    # parse out the necessary data
    data = strip_shell_result(result)
    total_mem = float(data[1])
    free_mem = float(data[3])
    #print(Total_Mem)
    #print(Free_Mem)

    # GET STORAGE DATA
    command = 'df -h'
    result = subprocess.check_output(command, shell=True, universal_newlines=True)
    data = strip_shell_result(result)
    total_storage = data[1]
    free_storage = data[3]
    #print(total_storage)
    #print(free_storage)

    # WRITE TO CSV 
    data_line = [temp_result, total_mem, free_mem, total_storage, free_storage]
    csv_file = "telemetry.csv"
    with open(csv_file, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(data_line)


# used for memory and storage data
def strip_shell_result(shell_result):
    """Strips whitespace and returns list for shell output"""
    lines = shell_result.strip().split('\n')
    data = lines[1].split()
    return data


if __name__ == "__main__":
    main()
