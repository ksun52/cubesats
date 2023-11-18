import RV8803
import serial
from ublox_gps import UbloxGps
import utils
import time
import datetime
import subprocess



starttime = time.time()
value = datetime.datetime.fromtimestamp(starttime)
date = value.strftime('%Y-%m-%d_%H:%M:%S')

LOGGER = utils.create_logger(logger_name="rtc_logger", logfolder="rtc", logfile_name=f"rtc_logger_{date}")

LOGGER.info("Starting Process to Sync RTC and Pi Time with GPS")

port = serial.Serial('/dev/tty1', baudrate=38400, timeout=1)
gps = UbloxGps(port)
LOGGER.info("Listening for UBX Messages from GPS")

rtc = RV8803.RV_8803()

while True:
    try:
        LOGGER.info("Trying to get GPS time")
        gps_time = gps.date_time()

        if gps_time != None:
            rtc.setSeconds(gps_time.sec)
            rtc.setMinutes(gps_time.min)
            rtc.setHours(gps_time.hour)

            rtc.setDate(gps_time.day)
            rtc.setMonth(gps_time.month)
            rtc.setYear(gps_time.year)
            LOGGER.info("GPS Time Received, RTC Time Set")            
            break
        
    except Exception as e:
        LOGGER.info(f"GPS error: {e}")
    
port.close()


LOGGER.info("Received RTC Time")
date_string = f"{int(rtc.getYear()):04d}{int(rtc.getMonth()):02d}{int(rtc.getDate()):02d}{int(rtc.getHours()):02d}{int(rtc.getMinutes()):02d}.{int(rtc.getSeconds()):02d}"

try:
    # Run the date command to set the system time
    LOGGER.info("Setting Pi Time")
    subprocess.run(["sudo", "date", date_string])
except Exception as e:
    LOGGER.info(f"Error Setting Pi Time: {e}")

LOGGER.info("Pi Time Successfully Set")


