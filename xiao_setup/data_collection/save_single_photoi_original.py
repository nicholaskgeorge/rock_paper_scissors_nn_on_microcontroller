import requests
from PIL import Image
from io import BytesIO

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

    # Save the image to a file
    image.save('captured_image.png')
    print("Image saved successfully as 'captured_image.png'.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the image: {e}")
except IOError as e:
    print(f"Error processing the image: {e}")