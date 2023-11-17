#42.2936° N, -83.7122°

# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, sqrt, log10, pi
import csv

def distance(lat,lon):

	fxb_lat = 42.2936
	fxb_lon = -83.7122	
	
	# The math module contains a function named
	# radians which converts from degrees to radians.
	fxb_lon = radians(fxb_lon)
	fxb_lat = radians(fxb_lat)
	lat = radians(lat)
	lon = radians(lon)
	
	
	# Haversine formula 
	dlon = lon - fxb_lon
	dlat = lat - fxb_lat
	a = sin(dlat / 2)**2 + cos(fxb_lat) * cos(lat) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a)) 
	
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	
	# calculate the result
	return(c * r)
	
def getSNR(lat, lon):
	freq = 437000000 # Hz
	tx_power = -23 # dBW
	line_loss = -2 # dB
	tx_gain = 1 # dB
	rx_gain = 18.9 # dBic
	atmos_loss = -.00001 # dB
	pointing_loss = -3 # dB
	noise_temp = 390 # K
	rate = 9600 # bps
	k = 1.38*(10**(-23)) # J/K
	e = 3*(10**8) # m/s
	
	space_loss = 20*log10(e/(4*pi)) - 20*log10(distance(lat,lon)*freq)
	snr = tx_power+line_loss+tx_gain+space_loss+atmos_loss+rx_gain+pointing_loss+228.6 - 10*log10(noise_temp)-10*log10(rate)
	return snr
	
