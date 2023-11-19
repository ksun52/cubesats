import subprocess
import time
import signal
import pdb
import datetime
import math
import csv
import utils


def watch_the_dog():

    starttime = time.time()
    startup_time = starttime
    value = datetime.datetime.fromtimestamp(starttime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')

    LOGGER = utils.create_logger(logger_name="watchdog_watcher_logger", logfolder="dog_watcher", logfile_name=f"dog_watch_logger_{date}")

    subprocess.Popen(["python3", f"/home/pi/team-papa/watchdog.py"])
    LOGGER.info("Started watchdog")
    time.sleep(5)

    while True:
        LOGGER.info("checking if watchdog is running")
        try:
            if check_watchdog_process(LOGGER) == False:
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/watchdog.py"])

                subprocess.call(["pkill", "-15", "-f", f"python2 /home/pi/plutoradio/PlutoRadio/gr-mxlgs/apps/CFLh.py"])
                time.sleep(1)
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/imu_run.py"])
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/mag_run.py"])
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/bme_run.py"])
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/gps_run.py"])
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/camera.py"])


                subprocess.Popen(["python3", f"/home/pi/team-papa/watchdog.py"])

                
                LOGGER.info(f"restarted watchdog watcher process")

        except Exception as e:
            LOGGER.info(f"Failure with watchdog watcher: {e}")

        time.sleep(15)
            
            
def check_watchdog_process(logger):
    try:
        # Run pgrep command to check for Python 2 processes
        subprocess.run(['pgrep', '-f', f'/home/pi/team-papa/watchdog.py'], check=True)
        logger.info("Watchdog process found.")
        return True
    except subprocess.CalledProcessError:
        logger.info("No watchdog process found.")
        return False



if __name__ == "__main__":
    watch_the_dog()