import numpy as np
import datetime
import time
from pathlib import Path
import csv 

import bme680
import time


def main():
    try:
        sensor = bme680.BME680(0x77)

        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)

        sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        sensor.set_gas_heater_temperature(320)
        sensor.set_gas_heater_duration(150)
        sensor.select_gas_heater_profile(0)

        accumulated_bme = []
        recent_bme = []

        ten_second_counter = time.time() - 11
        thirty_second_counter = time.time()

        starttime = time.time()
        value = datetime.datetime.fromtimestamp(starttime)
        date = value.strftime('%Y-%m-%d_%H:%M:%S')
        filename = f"all_bme_data_{date}"

        csv_file = create_bme_all_file(filename)

        while True:
            sensor.get_sensor_data()
            # get all BME data 
            temp = sensor.data.temperature # celcius
            pressure = sensor.data.pressure * 100 # mbar --> convert to Pascal 
            humidity = sensor.data.humidity # relative hum.
            recent_bme = [temp, pressure, humidity]
            accumulated_bme.append(recent_bme)
            
            # TODO: change time 
            if time.time() - ten_second_counter > 0.5:
                ten_second_counter = time.time()

                with open("bme_data/recent_bme.csv", mode='w') as file:
                    writer = csv.writer(file)
                    writer.writerow([0 if data is None else data for data in recent_bme])

                # write watchdog status 
                with open("watcher/bme_watch.txt", mode='w') as file:
                    file.write(str(time.time()))

            if time.time() - thirty_second_counter > 30:
                thirty_second_counter = time.time()
                with open(csv_file, mode='a') as file:
                    writer = csv.writer(file)
                    for bme_dataset in accumulated_bme:
                        writer.writerow([0 if data is None else data for data in bme_dataset])

            time.sleep(0.1)

    except Exception as e:
        print(f"bme error: {e}")


def create_bme_all_file(filename):
    csv_file = Path("bme_data", f'{filename}.csv')
    counter = 1
    
    while csv_file.exists():
        new_name = f"{filename}_({counter}).csv"
        csv_file = Path("bme_data", new_name)
        counter += 1

    with open(csv_file, 'w', newline='') as csvfile:
        # Write the header row
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(["gx", "gy", "gz", "ax", "ay", "az", "mx", "my", "mz"])
    
    return csv_file

if __name__ == "__main__":
    main()