import subprocess


# GET CPU TEMPERATURE 
command = 'vgencmd measure_temp'

# GET MEMORY DATA 
command = 'free -m'
result = subprocess.check_output(command, shell=True, universal_newlines=True)
lines = result.strip().split('\n')
data = lines[1].split()
Total_Mem = float(data[1])
Free_Mem = float(data[3])

# GET STORAGE DATA
command = 'df -h'
result = subprocess.check_output(command, shell=True, universal_newlines=True)
lines = result.strip().split('\n')
data = lines[1].split()
Total_Storage = data[1]
Free_Storage = data[3]

# WRITE TO CSV 
