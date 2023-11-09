import picamera
import time


"""
Record a 30 second video and then take a thumbnail picture
"""
def camera_run():
    # TODO set proper camera resolution and framerate 
    camera = picamera.PiCamera(resolution =(1440, 1080), framerate=10)

    time.sleep(2)
    i= 3
    while i>0:
        timestamp = time.time()
        filenum = 1
        
        thumbnailfile = f"thumbnails/{filenum}_{str(int(timestamp))}.jpg"
        camera.capture(thumbnailfile)
        print("thumbnail captured")

        videofile = f"videos/{filenum}_{str(int(timestamp))}.h264"
        camera.start_recording(videofile)
        print("video starting")
        camera.wait_recording(10)
        camera.stop_recording()
        print("video ending")

        filenum += 1
        i -= 1        



if __name__ == "__main__":
  camera_run()
