from PIL import Image
import os

def convert_images_to_bmp(folder_path):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print("The specified folder does not exist.")
        return
    
    # Iterate through all subdirectories and files
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Check if it's an image file
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".tiff")):
                try:
                    img = Image.open(file_path)
                    bmp_path = os.path.splitext(file_path)[0] + ".bmp"
                    img.save(bmp_path, "BMP")
                    os.remove(file_path)  # Remove the original file
                    print(f"Converted and replaced: {file_path} -> {bmp_path}")
                except Exception as e:
                    print(f"Error converting {file_path}: {e}")
    
    print("Conversion complete!")

# Specify the path to your project folder
project_folder = "RPS/data_collection/data/val"
convert_images_to_bmp(project_folder)