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
currentIndex = currentIndex+4

flags = data[currentIndex:currentIndex+2]
currentIndex = currentIndex+2

# stored in wrong -> converted to good endian
length = data[currentIndex:currentIndex+4] #f500 
length = length[2:] + length[0:2]
length = int(length, 16)
currentIndex = currentIndex+4

headerChecksum = data[currentIndex:currentIndex+4]

dataBytes = length - 17
realData = data[currentIndex:currentIndex+dataBytes*2]
currentIndex = currentIndex+dataBytes*2

checksum = data[currentIndex:currentIndex+4]
currentIndex = currentIndex+4

HMAC = data[currentIndex:currentIndex+8]
currentIndex = currentIndex+8

print('Sync Characters: ' + syncChars)
print('pID: ' + pID)
print('sID: ' + sID)
print('flags: ' + flags)
print('length (bytes): ' + str(length))
print('Header Checksum: ' + headerChecksum)
print('Data: ' + realData)
print('Checksum: ' + checksum)
print('HMAC: ' + HMAC)
print('Full Header: ' + syncChars + pID + sID + flags + str(length) + headerChecksum)
print('Footer: ' + checksum + HMAC)