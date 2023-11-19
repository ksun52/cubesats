#!/bin/bash

# File to store the boot timestamp
timestamp_file="/home/pi/team-papa/logs/powercycle.log"

# Get the current date and time
boot_timestamp=$(date "+%Y-%m-%d %H:%M:%S")

# Write the timestamp to the file
echo "Rpi Boot Timestamp: $boot_timestamp" >> "$timestamp_file"
