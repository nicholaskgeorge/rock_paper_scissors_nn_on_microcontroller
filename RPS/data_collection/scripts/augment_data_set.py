import os
import shutil
import cv2
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def augment_images(src_folder, dest_folder):
    # Create destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)
    
    # Define mapping for sign labels
    label_mapping = {"paper": 0, "rock": 1, "scissors": 2}
    # Initialize new index
    new_index = 0
    
    # Process each image in the source folder
    for filename in sorted(os.listdir(src_folder)):
        if not filename.endswith(".png"):
            continue
        
        # Extract sign type from filename
        parts = filename.split("_")
        sign = parts[0]
        
        if sign not in label_mapping:
            continue
        
        # Load image
        img_path = os.path.join(src_folder, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue
        
        # Define base filename with new index
        base_name = f"frame_{label_mapping[sign]}_{new_index}.png"
        new_index += 1
        
        # Copy original image
        shutil.copy(img_path, os.path.join(dest_folder, base_name))
        
        # Augmentations
        transformations = {
            "flip": cv2.flip(img, 1),
            "rot90": cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
            "rot180": cv2.rotate(img, cv2.ROTATE_180),
            "rot270": cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        }
        
        for key, transformed_img in transformations.items():
            new_filename = f"frame_{label_mapping[sign]}_{new_index}.png"
            new_index += 1
            cv2.imwrite(os.path.join(dest_folder, new_filename), transformed_img)
            
            # Flip each rotated image
            flipped_img = cv2.flip(transformed_img, 1)
            flipped_filename = f"frame_{label_mapping[sign]}_{new_index}.png"
            new_index += 1
            cv2.imwrite(os.path.join(dest_folder, flipped_filename), flipped_img)
    
    print(f"Dataset augmentation complete. New images saved in {dest_folder}")

# Example usage
original = "RPS/data_collection/data/original_data_set/scissors"
destination = "RPS/data_collection/data/augmented_training_data_set/scissors"
augment_images(original, destination)
