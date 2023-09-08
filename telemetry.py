import os


print(os.system('vgencmd measure_temp'))
print(os.system('free -m'))
print(os.system('df -h'))


