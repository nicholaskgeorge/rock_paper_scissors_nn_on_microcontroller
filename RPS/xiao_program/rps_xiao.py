import camera
import network
import time
import socket
import array
import emlearn_cnn_fp32

print("running")

PORT = 80

CAMERA_PARAMETERS = {
    "data_pins": [15, 17, 18, 16, 14, 12, 11, 48],
    "vsync_pin": 38,
    "href_pin": 47,
    "sda_pin": 40,
    "scl_pin": 39,
    "pclk_pin": 13,
    "xclk_pin": 10,
    "xclk_freq": 20000000,
    "powerdown_pin": -1,
    "reset_pin": -1,
    "frame_size": camera.FrameSize.R96X96,
    "pixel_format": camera.PixelFormat.GRAYSCALE
}

def argmax(arr):
    idx_max = 0
    value_max = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > value_max:
            value_max = arr[i]
            idx_max = i

    return idx_max

# Load model
MODEL_NAME = 'rps.tmdl'

cam = camera.Camera(**CAMERA_PARAMETERS)
cam.init()
cam.set_bmp_out(True)  # This will produce uncompressed images suitable for preprocessing

frame = cam.capture()

if frame:
    print("Captured frame successfully! Length:", len(frame))
else:
    print("Failed to capture frame.")

model = None
with open(MODEL_NAME, 'rb') as f:
    model_data = array.array('B', f.read())
    model = emlearn_cnn_fp32.new(model_data)

out_length = model.output_dimensions()[0]
probabilities = array.array('f', (-1 for _ in range(out_length)))
classes = {
            0:"paper",
            1:"rock",
            2:"scissors"
          }	

# Do classification
while True:
    frame = cam.capture()
    if frame:
        """
        with open("image.bmp", "wb") as f:
            f.write(frame)
        with open("image.bmp", 'rb') as f:
            img = f.read()
        """
        
        # The pixel data starts at byte offset 1078
        pixel_data_offset = 1078

        # Extract the pixel data
        pixel_data = frame[pixel_data_offset:pixel_data_offset + 9216]

        # Convert the pixel data to an array of unsigned bytes
        pixels = array.array('B', pixel_data)
        
        print(len(f"Length of input = {pixels}"))
        model.run(pixels, probabilities)
        out = argmax(probabilities)
        
        print(f"Current hand symbols is {classes[out]}") 
        
    else:
        print("Failed to capture frame.")
    
    time.sleep(0.1)