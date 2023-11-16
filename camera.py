import picamera
import time
import datetime
import utils

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
    camera = picamera.PiCamera(resolution=(1664, 1248), framerate=30.1)

    time.sleep(2)

    filenum = 0
    while True:
        timestamp = time.time()
        filenum = 1
        
        # capture a thumbnail - resize to smaller 
        thumbnailfile = f"thumbnails/{filenum}_{str(int(timestamp))}.jpg"
        camera.capture(thumbnailfile, resize=(320,240))
        LOGGER.info("thumbnail pic captured")

        # set a full res photo for saving onto storage 
        # full resolution: 2592×1944
        camera.resolution = (2592, 1944)
        fullres_file = f"fullres_pics/{filenum}_{str(int(timestamp))}.jpg"
        camera.capture(fullres_file)
        LOGGER.info("full resolution pic captured")
        camera.resolution = (1664, 1248)  # change resolution back 

        # NOW RECORD VIDEO
        videofile = f"videos/{filenum}_{str(int(timestamp))}.h264"
        
        camera.start_recording(videofile)
        LOGGER.info("video starting")
        camera.wait_recording(2)

        # write status for watchdog
        with open(f'watcher/cam_watch.txt', 'w') as file:
          file.write(str(time.time()))

        camera.wait_recording(2)

        # write status for watchdog
        with open(f'watcher/cam_watch.txt', 'w') as file:
          file.write(str(time.time()))

        camera.wait_recording(2)

        # write status for watchdog
        with open(f'watcher/cam_watch.txt', 'w') as file:
          file.write(str(time.time()))

        camera.stop_recording()
        LOGGER.info("video ending")

        filenum += 1
  except Exception as e:
    LOGGER.info(f"camera error: {e}")



if __name__ == "__main__":
  camera_run()
