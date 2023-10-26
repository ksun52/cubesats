import picamera
import time

# Set the filename for the video file and image file
video_file = 'output_video.h264'
image_file = 'output_image.jpg'

# Set the duration of the video capture in seconds
video_duration = 30

# Initialize the camera
with picamera.PiCamera() as camera:
    # Start recording video to the specified file
    camera.start_recording(video_file)
    
    # Record video for the specified duration
    camera.wait_recording(video_duration)
    
    # Stop recording
    camera.stop_recording()
    
    print(f'Video captured and saved to {video_file}')
    
    # Capture a still image and save it to the specified file
    camera.capture(image_file)
    
    print(f'Image captured and saved to {image_file}')
