import threading 
import telemetry
import mag_run
import imu_run
import time
import sys 

sys.path.append("/home/pi/plutoradio/PlutoRadio/CFLTXRX")

import CFL_TX

def main():
    magnetometer_thread = threading.Thread(target=telemetry.main)
    imu_thread = threading.Thread(target=imu_run.main)
    telemetry_thread = threading.Thread(target=mag_run.main)
    comms_thread = threading.Thread(target=CFL_TX.send)

    magnetometer_thread.start()
    time.sleep(0.5)
    imu_thread.start()
    time.sleep(0.5)
    telemetry_thread.start()
    time.sleep(0.5)
    comms_thread.start()

    magnetometer_thread.join()
    imu_thread.join()
    telemetry_thread.join() 
    comms_thread.join()

if __name__ == "__main__":
    main()
