# Project Overview

This repository contains the flight‑qualified Python software that flew on a 3U CubeSat balloon payload. Each program runs as an independent Linux process on a Raspberry Pi and is coordinated through a dual‑watchdog scheme and an on‑disk message bus. Together these programs perform command & data handling (CDH), sensor polling, telemetry generation, image capture and S‑band radio downlink using an ADALM‑Pluto SDR. 

The core processes are: 
- Watchdog 1
- Watchdog 2 
- Radio communication program 
- Telemetry program 
- IMU sensor manager
- BME sensor manager 
- Magnetometer sensor manager
- GPS manager 
- Camera manager 

These programs run independently on each other since sensor data collection operates on various frequencies and programs cannot wait for each other's cyle times. 

# Core Processes and Features

## Watchdog 2 -> Watchdog 1 Bootstrap Chain
- `watchdog2.py` is auto-started via `crontab @reboot` on the Raspberry Pi. It spawns `watchdog.py` (Watchdog 1) and checks its heartbeat every 30 seconds. Heartbeats are monitored via text files in `watcher` where monitored processes post their heartbeat times.
- Watchdog 1 launches every other flight process, then loops every 30 seconds to restart any task whose heartbeat text file hasn’t updated in the last 30 seconds.  It also publishes its own heartbeat for Watchdog 2.
- Altitude monitoring: when the reported altitude falls below a configurable threshold for > 30 min, the watchdog commands a landing mode that powers down non‑essential payloads to conserve battery.

## Telemetry Daemon (`telemetry.py`)
- Polls CPU metrics, TMP102 temperature sensors, EddyPDU volt/current every 10 seconds. Combines these metrics with the shared data from independent magnetometer, IMU, BME, GPS sensor programs to create a set of teleemtry data to be downlinked by the communication program. 
- Writes a new telemetry data CSV every 30 min to reduce file‑handle risk and bound RAM growth.

## Communications Service (`comms`)
- Packages telemetry or image fragments into RAP/DAP protocol packets and transmits them to the ground station through the Pluto SDR at a configurable rate.
- Achieved a 40 % end‑to‑end success rate (2126 beacons) during flight despite the antenna shearing off at landing. 

## Sensor Daemons
- The sensors and their corresponding manager programs are 
    - Inertial measurement units (IMU) — `imu_run.py`
    - Barometrc Pressure, Moisture and Environmental sensors (BME) — `bme_run.py`
    - GPS - `gps_run.py`
- Each sensor file follows the same template: 
    - Open a fresh data CSV every 30 min (timestamp‑based, with collision avoidance).
    - Read the device, append to an in‑memory list, and update a latest share‑file for Telemetry.
    - Flush the list to disk via csv file every 30 seconds.
    - Send out a heartbeat every 10 seconds for the watchdog.

## Camera Service (`camera.py`)

- Cycles every ~45 seconds: capture a 320 × 240 thumbnail, a full‑res 4056 × 3040 photo, then a 30 second video (split into 3 × 10 second chunks).
- Thumbnails are queued for downlink; full‑res media is stored locally for post‑flight analysis.
- Heartbeats between video chunks guarantee the watchdog won’t reset the camera mid‑recording.


# Startup Sequence

1. Boot → crontab launches watchdog2.py.

2. Watchdog 2 → Watchdog 1 → all subsystems.

3. Subsystems write heartbeats & data; watchdogs ensure programs can recover after failure. 

4. Upon landing detection, non‑essential tasks (camera, high‑rate sensors) are halted to conserve battery while comms & GPS stay alive for recovery.