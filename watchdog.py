import subprocess
import time
import signal
import pdb

def watch_programs():
    
    imu_last = run("imu_run", "imu_watch")
    mag_last = run("mag_run", "mag_watch")
    time.sleep(0.5)
    telem_last = run("telemetry", "telem_watch")

    starttime = time.time()

    while True:
        print("checking times")
        with open('watcher/imu_watch.txt', 'r') as file:
            imu_last = float(file.read().strip())
        
        with open('watcher/mag_watch.txt', 'r') as file:
            mag_last = float(file.read().strip())

        with open('watcher/telem_watch.txt', 'r') as file:
            telem_last = float(file.read().strip())


        if time.time() - imu_last > 3:
            print("starting new imu process")
            subprocess.call(["pkill", "-15", "-f", "python3 /home/pi/team-papa/imu_run.py"])
            imu_last = run("imu_run", "imu_watch")
        
        if time.time() - mag_last > 3:
            print("starting new mag process")
            subprocess.call(["pkill", "-15", "-f", "python3 /home/pi/team-papa/mag_run.py"])
            mag_last = run("mag_run", "mag_watch")
        
        if time.time() - telem_last > 3:
            print("starting new telemetry process")
            subprocess.call(["pkill", "-15", "-f", "python3 /home/pi/team-papa/telemetry.py"])
            telem_last = run("telemetry", "telem_watch")
        
        time.sleep((1 - (time.time() - starttime)) % 1)

def run(name, watcher):
    curtime = time.time()
    subprocess.Popen(["python3", f"/home/pi/team-papa/{name}.py"])
    with open(f'watcher/{watcher}.txt', 'w') as file:
        file.write(str(curtime))
    
    print("")
    
    return curtime

if __name__ == "__main__":
    watch_programs()

# to kill stale programs:
# ps aux to check for PID 
# pkill -f python3