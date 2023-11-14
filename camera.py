import picamera
import time


"""
Record a 30 second video and then take a thumbnail picture
"""
def camera_run():
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
        print("thumbnail pic captured")

        # set a full res photo for saving onto storage 
        # full resolution: 2592×1944
        camera.resolution = (2592, 1944)
        fullres_file = f"fullres_pics/{filenum}_{str(int(timestamp))}.jpg"
        camera.capture(fullres_file)
        print("full resolution pic captured")
        camera.resolution = (1664, 1248)  # change resolution back 

        # NOW RECORD VIDEO
        videofile = f"videos/{filenum}_{str(int(timestamp))}.h264"
        
        camera.start_recording(videofile)
        print("video starting")
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
        print("video ending")

        filenum += 1     



if __name__ == "__main__":
  camera_run()
