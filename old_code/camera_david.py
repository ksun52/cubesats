import cv2

# Initialize the webcam (usually camera index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open the webcam.")
else:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if ret:
        # Define the file name for the captured photo
        file_name = "captured_photo.jpg"

        # Save the captured frame as an image file
        cv2.imwrite(file_name, frame)

        # Release the webcam
        cap.release()

        print(f"Photo captured and saved as {file_name}")
    else:
        print("Error: Could not read a frame from the webcam.")

# Close all OpenCV windows
cv2.destroyAllWindows()
