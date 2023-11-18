#!/usr/bin/env python3

import subprocess
import time
import signal
import pdb
import datetime
import math
import csv
import utils

def watch_programs():
    starttime = time.time()
    startup_time = starttime
    value = datetime.datetime.fromtimestamp(starttime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')

    LOGGER = utils.create_logger(logger_name="dog_logger", logfolder="dog", logfile_name=f"dog_logger_{date}")


    mode = "flight"
    time_since_start = time.time()
    time_since_below_400m = 0 
    
    imu_last = run(runner="imu_run", watcher="imu_watch", logger=LOGGER)
    mag_last = run(runner="mag_run", watcher="mag_watch", logger=LOGGER)
    bme_last = run(runner="bme_run", watcher="bme_watch", logger=LOGGER)
    gps_last = run(runner="gps_run", watcher="gps_watch", logger=LOGGER)
    
    time.sleep(3)

    telem_last = run(runner="telemetry", watcher="telem_watch", logger=LOGGER)
    cam_last = run(runner="camera", watcher="cam_watch", logger=LOGGER)

    # start up CFLh process 
    subprocess.Popen(["python2", f"/home/pi/plutoradio/PlutoRadio/gr-mxlgs/apps/CFLh.py"])
    LOGGER.info(f"started new CFLh.py process")
    
    # start up CFL_TX process after 0.5 sec
    time.sleep(0.5)
    subprocess.Popen(["python3", f"/home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
    LOGGER.info(f"started new CFL_TX.py process")
    
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

            cfltx_last = checktime(watcher="cfltx_watch", logger=LOGGER)

        except Exception as e:
            LOGGER.info(f"error reading watchdog status: {e}")

        try:
            imu_last = check_restart(last_known_time=imu_last, runner="imu_run", watcher="imu_watch", logger=LOGGER)
            mag_last = check_restart(last_known_time=mag_last, runner="mag_run", watcher="mag_watch", logger=LOGGER)
            bme_last = check_restart(last_known_time=bme_last, runner="bme_run", watcher="bme_watch", logger=LOGGER)
            gps_last = check_restart(last_known_time=gps_last, runner="gps_run", watcher="gps_watch", logger=LOGGER)
            telem_last = check_restart(last_known_time=telem_last, runner="telemetry", watcher="telem_watch", logger=LOGGER)
            cam_last = check_restart(last_known_time=cam_last, runner="camera", watcher="cam_watch", logger=LOGGER)


            # check restart on CFLh 
            if check_python2_process(logger = LOGGER) == False:
                logger.info(f"Restart on CFLh.py needed")
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
                subprocess.call(["pkill", "-15", "-f", f"python2 /home/pi/plutoradio/PlutoRadio/gr-mxlgs/apps/CFLh.py"])
                
                logger.info(f"Killed both CFL_TX and CFLh")

                subprocess.Popen(["python2", f"/home/pi/plutoradio/PlutoRadio/gr-mxlgs/apps/CFLh.py"])
                time.sleep(0.5)
                subprocess.Popen(["python3", f"/home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
                LOGGER.info(f"started new CFL_TX.py process")
            
            time.sleep(0.5)
            # check restart on CFL_TX 
            if check_TX_process(logger = LOGGER) == False:
                logger.info(f"Restart on CFL_TX.py needed")
                subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
                
                logger.info(f"Killed CFL_TX.py")

                subprocess.Popen(["python3", f"/home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
                LOGGER.info(f"started new CFL_TX.py process")

        except Exception as e:
            LOGGER.info(f"error checking restart status: {e}")
            pdb.set_trace()
	
	try:
            altitude = 0
            pressure, temp = read_bme(LOGGER)
            if (pressure != -404):
                # altitude = 44330 * (1 - (pressure/101325)^(1/5.255))
                altitude = 44330 * (1 - math.pow((pressure / 101325), 1 / 5.255))
                # print(altitude)
            if altitude < 400 and time.time() - startup_time > 1800:  # Check if it's been 30 minutes since startup
                time_since_below_400m += (time.time() - starttime) # how long the altitude has been below 400m continuously
                if time_since_below_400m >= 600:  # Check if it's been 10 minutes (600 seconds)
                    LOGGER.info("Altitude below 400m for 10 minutes. Entering landed mode.")
                    mode = "landed"
            else:
                time_since_below_400m = 0  # Reset time since below 400m if altitude is above 400m  
                if mode == "landed":
                    LOGGER.info("Altitude above 400m. Exiting landed mode.")
                    mode = "flight"
         except Exception as e:
            LOGGER.info(f"error with altitude stuff: {e}")

        time.sleep((10 - (time.time() - starttime)) % 10)


def run(runner, watcher, logger):
    curtime = time.time()
    subprocess.Popen(["python3", f"/home/pi/team-papa/{runner}.py"])
    with open(f'watcher/{watcher}.txt', 'w') as file:
        file.write(str(curtime))
    logger.info(f"started new {runner} process")
    return curtime

# def run_cflh(watcher, logger):
#     curtime = time.time()
#     subprocess.Popen(["python2", f"/home/pi/plutoradio/PlutoRadio/gr-mxlgs/apps/CFLh.py"])
#     with open(f'watcher/{watcher}.txt', 'w') as file:
#         file.write(str(curtime))
#     logger.info(f"started new CFLh.py process")
#     return curtime

# def run_cfltx(watcher, logger):
#     curtime = time.time()
#     subprocess.Popen(["python3", f"/home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
#     with open(f'watcher/{watcher}.txt', 'w') as file:
#         file.write(str(curtime))
#     logger.info(f"started new CFL_TX.py process")
#     return curtime

def checktime(watcher, logger):
    logger.info(f"Checking status on {watcher}")
    with open(f'watcher/{watcher}.txt', 'r') as file:
        return float(file.read().strip())

def check_restart(last_known_time, runner, watcher, logger):
    if time.time() - last_known_time > 20:
        logger.info(f"Restart on {runner} needed")
        subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/team-papa/{runner}.py"])
        return run(runner, watcher, logger=logger)
    else:
        return last_known_time

# def check_restart_cflh(last_known_time_cflh, last_known_time_cfltx, watcher, logger):
#     if time.time() - last_known_time_cflh > 20:
#         logger.info(f"Restart on CFLh.py needed")
#         subprocess.call(["pkill", "-15", "-f", f"python3 /home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
#         subprocess.call(["pkill", "-15", "-f", f"python2 /home/pi/plutoradio/PlutoRadio/gr-mxlgs/apps/CFLh.py"])
#         logger.info(f"Killed both CFL_TX and CFLh")
#         last_known_time_cflh = run_cflh(watcher="cflh_watch", logger=LOGGER)
#         time.sleep(0.5)
#         last_known_time_cfltx = run_cfltx(watcher="cfltx_watch", logger=LOGGER)
#         return last_known_time_cflh, last_known_time_cfltx
#     else:
#         return last_known_time_cflh, last_known_time_cfltx

# def check_restart_cfltx(last_known_time_cfltx, watcher, logger):
#     if time.time() - last_known_time_cfltx > 20:
#         logger.info(f"Restart on CFL_TX.py needed")
#         subprocess.call(["pkill", "-15", "-f", f"/home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py"])
#         logger.info(f"Killed CFL_TX only")
#         return run_cfltx(watcher="cfltx_watch", logger=LOGGER)
#     else:
#         return last_known_time_cfltx

def check_python2_process(logger):
    try:
        # Run pgrep command to check for Python 2 processes
        subprocess.run(['pgrep', '-f', 'python2'], check=True)
        logger.info("Cflh.py process found.")
        return True
    except subprocess.CalledProcessError:
        logger.info("No Cflh.py process found.")
        return False

def check_TX_process(logger):
    try:
        # Run pgrep command to check for CFL_TX processes
        subprocess.run(['pgrep', '-f', f'python3 /home/pi/plutoradio/PlutoRadio/CFLTXRX/CFL_TX.py'], check=True)
        logger.info("CFL_TX.py process found.")
        return True
    except subprocess.CalledProcessError:
        logger.info("No CFL_TX.py process found.")
        return False

def read_bme(logger):
    pressure = 0
    temp = 0
    try:
        with open('bme_data/recent_bme.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                temp = float(row[0])
                pressure = float(row[1])
        logger.info("got bme info for watchdog")

        return pressure, temp

    except Exception as e:
        logger.info(f"bme data error: {e}")

        return -404, -404

if __name__ == "__main__":
    watch_programs()

# to kill stale programs:
# ps aux to check for PID 
# pkill -f python3
