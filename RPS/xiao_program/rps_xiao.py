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

# Do classification
while True:
    frame = cam.capture()
    if frame:
        # Ensure the frame is in the correct format
        input_data = array.array('B', frame)
        print(len(input_data))
        model.run(input_data, probabilities)
        out = argmax(probabilities)
        print(out)
    else:
        print("Failed to capture frame.")
    
    time.sleep(0.5)