import cv2
import os

def resize_images_cv2(input_folder, output_folder, size=(32, 32)):
    """Resizes all images in the input_folder to the specified size using OpenCV and saves them in output_folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)  # Read image using OpenCV
            if img is None:
                print(f"Skipping {filename}, could not read.")
                continue
            img_resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)  # Resize using OpenCV
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img_resized)  # Save the resized image
            print(f"Resized and saved: {output_path}")

if __name__ == "__main__":
    input_folder = "RPS/data_collection/data/val/scissors"
    output_folder = "RPS/data_collection/data/val_32x32/scissors"
    resize_images_cv2(input_folder, output_folder)