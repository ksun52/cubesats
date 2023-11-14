# rough code just for initial testing and structure for gps telem -- monica

# Given string for lat, lon, speed
input_string_lat_lon_speed = "$GNRMC,202532.00,A,4217.60566,N,08342.70251,W,8.792,36.52,141123,,,A,V*21"

# Split the string by commas
split_parts = input_string_lat_lon_speed.split(',')

# Extract the required parts
lon = split_parts[3] + ' ' + split_parts[4]
lat = split_parts[5] + ' ' + split_parts[6]
speed_knots = float(split_parts[7])
speed_kmh = speed_knots * 1.852  # Convert knots to km/h

# Print the combined parts
print("Longitude:", lon)
print("Latitude:", lat)
print("Speed:", speed_kmh)


# Given string for altitude, fix quality
input_string_fix_alt = "$GNGGA,202444.00,4217.59039,N,08342.71497,W,1,10,1.98,273.5,M,-34.7,M,,*7C"
split_parts_2 = input_string_fix_alt.split(',')

# Extract the required parts
fix_quality = split_parts_2[6]
altitude = split_parts_2[9] + ' ' + split_parts_2[10]

# Print the combined parts
print("Fix Quality:", fix_quality)
print("Altitude:", altitude)

# Given string for snr
input_string_snr = "$GPGSV,3,2,09,26,68,062,25,27,17,157,19,28,24,081,24,29,12,039,14,1*69"
split_parts_3 = input_string_snr.split(',')

# Extract the required parts
snr = split_parts_3[7]

# Print the combined parts
print("SNR:", snr)


