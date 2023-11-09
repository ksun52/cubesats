import threading 
import telemetry
import mag_run
import imu_run
import time

def main():
    magnetometer_thread = threading.Thread(target=telemetry.main)
    imu_thread = threading.Thread(target=telemetry.main)
    telemetry_thread = threading.Thread(target=telemetry.main)

    magnetometer_thread.start()
    time.sleep(0.5)
    imu_thread.start()
    time.sleep(0.5)
    telemetry_thread.start()

    magnetometer_thread.join()
    imu_thread.join()
    telemetry_thread.join() 

if __name__ == "__main__":
    main()
