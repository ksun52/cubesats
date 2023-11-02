import picamera
import time


"""
Record a 30 second video and then take a thumbnail picture
"""
def camera_run():
    # TODO set proper camera resolution and framerate 
    camera = PiCamera(resolution =(1024, 768), framerate=10)
    
    time.sleep(2)
    
    while True:
        timestamp = time.time()
        filenum = 1
        
        thumbnailfile = f"thumbnails/{filenum}_{str(int(timestamp))}.jpg"
        camera.capture(thumbnailfile)

        videofile = f"videos/{filenum}_{str(int(timestamp))}.h264"
        camera.start_recording(videofile)
        camera.wait_recording(10)
        camera.stop_recording()

        filenum += 1
        



if __name__ == "__main__":
    camera_run()