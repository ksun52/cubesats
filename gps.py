import serial

from ublox_gps import UbloxGps

def gpsdata():

    port = serial.Serial('/dev/ttyS0', baudrate=38400, timeout=5) #Baud could be 115200 instead
    gps = UbloxGps(port)

    try:
        print("Listening for UBX Messages")
        while True:
            try:
                geo = gps.geo_coords()
                print(geo)
                print("Longitude: ", geo.lon) 
                print("Latitude: ", geo.lat)
            except (ValueError, IOError) as err:
                print("we are here")
                print(err)
    finally:
        print("closing")
        port.close()

def gps_test():

    port = serial.Serial('/dev/tty1', baudrate=38400, timeout=1) #Baud could be 115200 instead
    gps = UbloxGps(port)

    try:
        print("Listening for UBX Messages")
   
        try:
            while gps.geo_coords(wait_time=1000) == None:
                print("no lock")
            geo = gps.geo_coords()
            print(geo)
            print("Longitude: ", geo.lon) 
            print("Latitude: ", geo.lat)
        except (ValueError, IOError) as err:
            print("we are here")
            print(err)
    finally:
        print("closing")
        port.close()


if __name__ == '__main__':
    gps_test()