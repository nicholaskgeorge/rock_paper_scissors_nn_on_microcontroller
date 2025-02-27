import time
import socket
import array
import emlearn_cnn_fp32
from microbmp import MicroBMP
from image_preprocessing import resize_96x96_to_32x32,  


def argmax(arr):
    idx_max = 0
    value_max = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > value_max:
            value_max = arr[i]
            idx_max = i

    return idx_max

MODEL_NAME = 'rps2.tmdl'

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

while True:
    frame = ''
    pixels = MicroBMP().load("frame_2_4589.bmp").parray
    pixels = array.array('B', pixels)
    #print(len(f"Length of input = {pixels}"))
    model.run(pixels, probabilities)
    out = argmax(probabilities)
    print(classes[out])