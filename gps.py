import serial

from ublox_gps import UbloxGps

def gpsdata():

    port = serial.Serial('/dev/tty1', baudrate=38400, timeout=1) #Baud could be 115200 instead
    gps = UbloxGps(port)

    try:
        print("Listening for UBX Messages")
        try:
            geo = gps.geo_coords()
            print("Longitude: ", geo.lon) 
            print("Latitude: ", geo.lat)
        except (ValueError, IOError) as err:
            print(err)

    finally:
        port.close()


if __name__ == '__main__':
    gpsdata()