import cv2

def check_live_feed(camera_index=0):
    """
    This function checks the current live feed from an external camera.
    
    Parameters:
    - camera_index: Index of the camera to access (default is 0 for the default webcam).
    
    Returns:
    - True if the camera feed is accessible and working, False otherwise.
    """
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera is opened
    if not cap.isOpened():
        print(f"Error: Unable to access camera with index {camera_index}.")
        return False

    print(f"Successfully connected to camera {camera_index}. Showing live feed...")

    # Start capturing the live feed
    while True:
        # Read the current frame
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            print("Error: Failed to capture image from the camera.")
            break

        # Display the captured frame
        cv2.imshow('Live Feed', frame)

        # Wait for the user to press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    return True

# Call the function to check the live feed
if __name__ == "__main__":
    # Use camera 0 by default, or change the index if needed
    check_live_feed(camera_index=0)