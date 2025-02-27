import camera
from camera import Camera, GrabMode, PixelFormat, FrameSize
import network
import time
import socket
import array
import emlearn_cnn_fp32
from microbmp import MicroBMP

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

@micropython.native
def average2d(inp, rowstride : int, x : int, y : int, size : int):
    acc : int = 0
    for r in range(y, y+size):
        for c in range(x, x+size):
            acc += inp[(r*rowstride)+c]

    avg = acc // (size*size)
    return avg


@micropython.native
def downscale(inp, out, in_size : int, out_size : int):
    assert len(inp) == in_size*in_size
    assert len(out) == out_size*out_size
    assert (in_size % out_size) == 0, (in_size, out_size)
    factor : int = in_size // out_size

    for row in range(out_size):
        for col in range(out_size):
            o : int = (row * out_size) + col
            out[o] = average2d(inp, in_size, col*factor, row*factor, factor)

    return out

def argmax(arr):
    idx_max = 0
    value_max = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > value_max:
            value_max = arr[i]
            idx_max = i

    return idx_max


def save_image(path, arr, width, height):

    # https://github.com/jacklinquan/micropython-microbmp
    # wget https://raw.githubusercontent.com/jacklinquan/micropython-microbmp/refs/heads/main/microbmp.py        

    if len(arr) != (width*height):
        raise ValueError("Unexpected size")

    out = MicroBMP(width, height, 8)
    for r in range(height):
        for c in range(width):
            i = (r*width)+c
            out.parray[i] = arr[i]

    out.save(path)
    
def setup_camera():
    DATA_PINS = [
        34,
        13,
        14,
        35,
        39,
        12,
        15,
        36,
    ]

    camera = Camera(
        data_pins=[15, 17, 18, 16, 14, 12, 11, 48],
        vsync_pin=38,
        href_pin=47,
        sda_pin=40,
        scl_pin=39,
        pclk_pin=13,
        xclk_pin=10,
        xclk_freq=20000000,
        powerdown_pin=-1,
        reset_pin=-1,
        pixel_format=PixelFormat.GRAYSCALE,
        frame_size=FrameSize.R96X96,
        jpeg_quality=15,
        fb_count=2,
        grab_mode=GrabMode.LATEST
    )
    return camera



# Load model
MODEL_NAME = 'rps2.tmdl'

#cam = camera.Camera(**CAMERA_PARAMETERS)
#cam.init()
#cam.set_bmp_out(True)  # This will produce uncompressed images suitable for preprocessing

cam = setup_camera()
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

process_size = 32
width = 96
height = 96
scaled = array.array('B', (0 for _ in range(process_size*process_size)))

# Do classification
while True:
    frame = cam.capture()
    if frame:
        path = f'img.bmp'
        buf =  bytes(frame)
        save_image(path, buf, 96, 96)
        
        buf = downscale(buf, scaled, width, process_size)
        
        model.run(buf, probabilities)
        out = argmax(probabilities)
        
        print(f"Current hand symbols is {classes[out]}") 
        
    else:
        print("Failed to capture frame.")