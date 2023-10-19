# Open the text file for reading
with open('rawbeacons.txt', 'r') as file:
    # Read the entire file content as a string
    data = file.read()

# Search for the starting index of 'abcd' in the file content
startIndex = data.find('abcd')
currentIndex = startIndex

syncChars = data[startIndex:startIndex+4]
currentIndex = startIndex+4

pID = data[currentIndex:currentIndex+4]
currentIndex = currentIndex+4

sID = data[currentIndex:currentIndex+4]
sID_decimal = int(sID,16)
currentIndex = currentIndex+4

flags = data[currentIndex:currentIndex+2]
flags_decimal = int(flags,16)
currentIndex = currentIndex+2

# stored in wrong -> converted to good endian for byte size
length = data[currentIndex:currentIndex+4] #f500 
length_decimal = length[2:] + length[0:2] # converts to big endian
length_decimal = int(length_decimal, 16) # converts hex to decimal
currentIndex = currentIndex+4

print(length_decimal)

# Fletcher 16 implementation for header checksum
sum1 = 0
sum2 = 0
for i in range(0,18,2):
    sum1 = (sum1 + int(data[i:i+2],16)) % 255
    sum2 = (sum2 + sum1) % 255
headerChecksum_F16_decimal = (sum2 << 8) | sum1

headerChecksum = data[currentIndex:currentIndex+4]
headerChecksum = headerChecksum[2:] + headerChecksum[0:2] # converts to big endian
headerChecksum_decimal = int(headerChecksum,16)
currentIndex = currentIndex+4 # now at end of header checksum / beginning of real data

dataBytes = length_decimal - 17
realData = data[currentIndex:currentIndex+dataBytes*2]

print('current index: ' + str(dataBytes))
currentIndex = currentIndex+dataBytes*2

checksum = data[currentIndex:currentIndex+4]
checksum = checksum[2:] + checksum[0:2] # converts to big endian
checksum_decimal = int(checksum,16)
currentIndex = currentIndex+4

# Fletcher 16 implementation for data checksum
sum1 = 0
sum2 = 0
for i in range(22,22+dataBytes*2,2):
    sum1 = (sum1 + int(data[i:i+2],16)) % 255
    sum2 = (sum2 + sum1) % 255
dataChecksum_F16_decimal = (sum2 << 8) | sum1

HMAC = data[currentIndex:currentIndex+8]
currentIndex = currentIndex+8

print('Sync Characters: ' + syncChars)
print('pID: ' + pID)
print('sID (decimal): ' + str(sID_decimal))
print('flags (decimal): ' + str(flags_decimal))
print('length (bytes): ' + length)
print('Header Checksum (decimal): ' + str(headerChecksum_decimal))
print('Header Checksum (Fletcher-16, decimal): ' + str(headerChecksum_F16_decimal))
print('Data: ' + realData)
print('Data Checksum (decimal): ' + str(checksum_decimal))
print('Data Checksum Fletcher 16 (decimal): ' + str(dataChecksum_F16_decimal))
print('HMAC: ' + HMAC)
print('Full Header: ' + syncChars + pID + sID + flags + str(length) + headerChecksum)
print('Footer: ' + checksum + HMAC)

