import os
import requests
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import time

def fetch_video_stream(save_directory):
    """
    Fetches a continuous stream of images from the microcontroller and processes them as video frames.

    Parameters:
    save_directory (str): The directory where frames will be saved.
    """
    url = "http://172.20.10.3"
    name_of_frames = "rock"
    frame_count = 0

    # Ensure the directory exists
    os.makedirs(save_directory, exist_ok=True)

    try:
        print('Requesting image stream...')
        response = requests.get(url, stream=True, timeout=5)
        response.raise_for_status()

        boundary = b'--frame'
        buffer = b''

        for chunk in response.iter_content(chunk_size=1024):
            buffer += chunk
            while True:
                # Find the boundary
                boundary_index = buffer.find(boundary)
                if boundary_index == -1:
                    break

                # Find the end of the headers
                header_end_index = buffer.find(b'\r\n\r\n', boundary_index)
                if header_end_index == -1:
                    break

                # Extract headers
                headers = buffer[boundary_index + len(boundary):header_end_index].decode('utf-8', errors='ignore')
                content_length = None
                for header in headers.split('\r\n'):
                    if header.lower().startswith('content-length'):
                        content_length = int(header.split(':')[1].strip())
                        break

                if content_length is None:
                    print("Content-Length not found in headers.")
                    buffer = buffer[boundary_index + len(boundary):]
                    continue

                # Calculate the start and end of the image data
                image_start = header_end_index + 4
                image_end = image_start + content_length

                if len(buffer) < image_end:
                    break  # Wait for more data

                # Extract image data
                image_data = buffer[image_start:image_end]
                buffer = buffer[image_end:]

                # Process the image
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
                frame_filename = os.path.join(save_directory, f"{name_of_frames}_frame_{frame_count:03d}.png")
                image.save(frame_filename)
                print(f"Saved: {frame_filename}")

                frame_count += 1

                # Stop when 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    response.close()
                    cv2.destroyAllWindows()
                    return

    except requests.exceptions.RequestException as e:
        print(f"Error fetching frame: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cv2.destroyAllWindows()

# Example usage:
save_directory = "RPS/data_collection/data/original_data_set/rock"
fetch_video_stream(save_directory)