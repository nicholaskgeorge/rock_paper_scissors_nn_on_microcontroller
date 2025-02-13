import os
import requests
from PIL import Image
from io import BytesIO
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fetch_and_save_image(file_path):
    """
    Fetches an image from the microcontroller's server and saves it to the specified file path.

    Parameters:
    file_path (str): The full path, including the filename and extension, where the image will be saved.
    """
    # Replace with the actual IP address of your microcontroller
    url = 'http://172.20.10.2'

    try:
        # Send a GET request to the microcontroller's server
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for request errors

        # Read the image data from the response
        image_data = response.content

        # Open the image using Pillow
        image = Image.open(BytesIO(image_data))

        # Ensure the image is in grayscale mode
        if image.mode != 'L':
            image = image.convert('L')

        # Verify the image size
        if image.size != (96, 96):
            print(f"Unexpected image size: {image.size}. Resizing to (96, 96).")
            image = image.resize((96, 96))

        # Extract the directory from the file path
        save_directory = os.path.dirname(file_path)

        # Create the directory if it doesn't exist
        if save_directory and not os.path.exists(save_directory):
            os.makedirs(save_directory, exist_ok=True)

        # Save the image to the specified file path
        image.save(file_path)
        print(f"Image saved successfully at '{file_path}'.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image: {e}")
    except IOError as e:
        print(f"Error processing the image: {e}")

# Example usage:
save_path = 'xiao_setup/data_colection/data_set/captured_image.png'  # Replace with your desired path
fetch_and_save_image(save_path)