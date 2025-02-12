import os
import requests
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def fetch_video_stream(save_directory):
    """
    Fetches a continuous stream of images from the microcontroller and processes them as video frames.

    Parameters:
    save_directory (str): The directory where frames will be saved.
    """
    url = "http://172.20.10.2"
    frame_count = 0

    # Ensure the directory exists
    os.makedirs(save_directory, exist_ok=True)

    while True:
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            # Read the image from response
            image_data = response.content
            image = Image.open(BytesIO(image_data))

            # Convert to grayscale if needed
            if image.mode != "L":
                image = image.convert("L")

            # Resize to 96x96 if necessary
            if image.size != (96, 96):
                image = image.resize((96, 96))

            # Convert to OpenCV format
            frame = np.array(image)

            # Display the frame
            cv2.imshow("Video Stream", frame)

            # Save the frame
            frame_filename = os.path.join(save_directory, f"frame_{frame_count:03d}.png")
            image.save(frame_filename)
            print(f"Saved: {frame_filename}")

            frame_count += 1

            # Stop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        except requests.exceptions.RequestException as e:
            print(f"Error fetching frame: {e}")

    cv2.destroyAllWindows()

# Example usage:
save_directory = "xiao_setup/data_collection/data_set"
fetch_video_stream(save_directory)