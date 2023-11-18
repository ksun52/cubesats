import picamera
import time
import datetime
import utils
from pathlib import Path

"""
Record a 30 second video and then take a thumbnail picture
"""
def camera_run():
  try:
    starttime = time.time()
    value = datetime.datetime.fromtimestamp(starttime)
    date = value.strftime('%Y-%m-%d_%H:%M:%S')

    LOGGER = utils.create_logger(logger_name="cam_logger", logfolder="cam", logfile_name=f"cam_logger_{date}")


    # resolution and framerate given by team mike 
    camera = picamera.PiCamera(resolution=(4056, 3040), framerate=30.1)

    LOGGER.info("Started up camera")

    time.sleep(2)

    filenum = 0
    while True:
        timestamp = time.time()
        

        # capture a thumbnail - resize to smaller 
        thumbnailfile = create_media_file("thumbnails", timestamp, ".jpg")
        camera.resolution=(1664, 1248)
        camera.capture(thumbnailfile, resize=(320,240))
        LOGGER.info("thumbnail pic at low resolution captured")

        # set a full res photo for saving onto storage 
        
        # fullres_file = create_media_file("fullres_pics", timestamp, ".jpg")
        # camera.resolution=(4056, 3040)
        # camera.capture(fullres_file)
        # LOGGER.info("full resolution pic captured")

        # NOW RECORD VIDEO
        videofile = create_media_file("videos", timestamp, ".h264")
        camera.resolution=(1920, 1080)
        camera.start_recording(videofile)
        LOGGER.info("video starting")
        camera.wait_recording(10)

        # write status for watchdog
        with open(f'watcher/cam_watch.txt', 'w') as file:
          file.write(str(time.time()))
        LOGGER.info("write status to watchdog 1")

        camera.wait_recording(10)

        # write status for watchdog
        with open(f'watcher/cam_watch.txt', 'w') as file:
          file.write(str(time.time()))
        
        LOGGER.info("write status to watchdog 2")

        camera.wait_recording(10)

        # write status for watchdog
        with open(f'watcher/cam_watch.txt', 'w') as file:
          file.write(str(time.time()))
        
        LOGGER.info("write status to watchdog 3")

        camera.stop_recording()
        LOGGER.info("video ending")

        filenum += 1
  except Exception as e:
    LOGGER.info(f"camera error: {e}")

def create_media_file(folder, timestamp, extension):
    # ex: f"thumbnails/{str(int(timestamp))}.jpg"

    filepath = Path(folder, f"{int(timestamp)}{extension}")
    counter = 1

    if not filepath.exists():
      return f"{folder}/{timestamp}{extension}"

    while filepath.exists():
        filepath = Path(folder, f"{int(timestamp)}_{counter}" , extension)
        counter += 1
    
    return f"{folder}/{timestamp}_{counter}{extension}"

def take_thumbnail():
  starttime = time.time()
  value = datetime.datetime.fromtimestamp(starttime)
  date = value.strftime('%Y-%m-%d_%H:%M:%S')
  camera = picamera.PiCamera(resolution=(4056, 3040), framerate=30.1)

  # capture a thumbnail - resize to smaller 
  thumbnailfile = create_media_file("fullres_pics", starttime, ".jpg")
  # camera.resolution=(1664, 1248)
  camera.capture(thumbnailfile)

    
        


if __name__ == "__main__":
  camera_run()
  # take_thumbnail()
