#!/usr/bin/env python3

import subprocess
import time
import signal
import pdb
import datetime

import utils

def watch_programs():
    starttime = time.time()
    value = datetime.datetime.fromtimestamp(starttime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')

    LOGGER = utils.create_logger(logger_name="dog_logger", logfolder="dog", logfile_name=f"dog_logger_{date}")


    mode = "flight"
    
    imu_last = run(runner="imu_run", watcher="imu_watch", logger=LOGGER)
    mag_last = run(runner="mag_run", watcher="mag_watch", logger=LOGGER)
    bme_last = run(runner="bme_run", watcher="bme_watch", logger=LOGGER)
    gps_last = run(runner="gps_run", watcher="gps_watch", logger=LOGGER)

    time.sleep(0.5)

    telem_last = run(runner="telemetry", watcher="telem_watch", logger=LOGGER)
    cam_last = run(runner="camera", watcher="cam_watch", logger=LOGGER)
    

    starttime = time.time()

    while True:
        LOGGER.info("checking processes last updated times")
        try:
            imu_last = checktime(watcher="imu_watch", logger=LOGGER)
            mag_last = checktime(watcher="mag_watch", logger=LOGGER)
            bme_last = checktime(watcher="bme_watch", logger=LOGGER)
            gps_last = checktime(watcher="gps_watch", logger=LOGGER)
            telem_last = checktime(watcher="telem_watch", logger=LOGGER)
            cam_last = checktime(watcher="cam_watch", logger=LOGGER)
        except Exception as e:
            LOGGER.info(f"error reading watchdog status: {e}")

        imu_last = check_restart(last_known_time=imu_last, runner="imu_run", watcher="imu_watch", logger=LOGGER)
        mag_last = check_restart(last_known_time=mag_last, runner="mag_run", watcher="mag_watch", logger=LOGGER)
        bme_last = check_restart(last_known_time=bme_last, runner="bme_run", watcher="bme_watch", logger=LOGGER)
        gps_last = check_restart(last_known_time=gps_last, runner="gps_run", watcher="gps_watch", logger=LOGGER)
        telem_last = check_restart(last_known_time=telem_last, runner="telemetry", watcher="telem_watch", logger=LOGGER)
        cam_last = check_restart(last_known_time=cam_last, runner="camera", watcher="cam_watch", logger=LOGGER)
        
        time.sleep((5 - (time.time() - starttime)) % 5)

def run(runner, watcher, logger):
    curtime = time.time()
    subprocess.Popen(["python3", f"/home/pi/team-papa/{runner}.py"])
    with open(f'watcher/{watcher}.txt', 'w') as file:
        file.write(str(curtime))
    logger.info(f"started new {runner} process")
    return curtime

def checktime(watcher, logger):
    logger.info(f"Checking status on {logger}")
    with open(f'watcher/{watcher}.txt', 'r') as file:
        return float(file.read().strip())

def check_restart(last_known_time, runner, watcher, logger):
    if time.time() - last_known_time > 30:
        logger.info(f"Restart on {runner} needed")
        subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/{runner}.py"])
        return run(runner, watcher, logger=logger)

if __name__ == "__main__":
    watch_programs()

# to kill stale programs:
# ps aux to check for PID 
# pkill -f python3