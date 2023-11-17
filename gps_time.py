import serial

from ublox_gps import UbloxGps

port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
gps = UbloxGps(port)

print("Listening for UBX Messages")
try:
    while True:
        try:
            gps_time = gps.date_time()
            print("{}/{}/{}".format(gps_time.day, gps_time.month,
                                        gps_time.year))
            print("UTC Time {}:{}:{}".format(gps_time.hour, gps_time.min,
                                        gps_time.sec))
            print("Valid date:{}\nValid Time:{}".format(gps_time.valid.validDate, 
                                                            gps_time.valid.validTime))
        except Exception as e:
            print(err)

finally:
    port.close()


if __name__ == '__main__':
    run()