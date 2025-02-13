import os
import shutil
import random
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def split_dataset(source_folder, output_folder, train_ratio=0.8):
    """
    Splits a dataset into training and validation sets while maintaining folder structure.

    Parameters:
        source_folder (str): Path to the original dataset (e.g., "data_set").
        output_folder (str): Path to the output directory (e.g., "models/data").
        train_ratio (float): Proportion of images for training (default: 0.8 for 80% train, 20% val).
    """

    # Define train and validation output directories
    train_folder = os.path.join(output_folder, "train")
    val_folder = os.path.join(output_folder, "val")

    # Ensure output directories exist
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)

    # Loop through each category (rock, paper, scissors)
    for category in os.listdir(source_folder):
        category_path = os.path.join(source_folder, category)
        
        if not os.path.isdir(category_path):  # Skip any non-folder files
            continue

        # Create category subfolders in train/val directories
        train_category_path = os.path.join(train_folder, category)
        val_category_path = os.path.join(val_folder, category)

        os.makedirs(train_category_path, exist_ok=True)
        os.makedirs(val_category_path, exist_ok=True)

        # List all images in the category
        images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
        random.shuffle(images)  # Shuffle to ensure randomness

        # Split the images
        split_index = int(len(images) * train_ratio)
        train_images = images[:split_index]
        val_images = images[split_index:]

        # Move images to respective folders
        for img in train_images:
            shutil.copy(os.path.join(category_path, img), os.path.join(train_category_path, img))

        for img in val_images:
            shutil.copy(os.path.join(category_path, img), os.path.join(val_category_path, img))

        print(f"Processed '{category}': {len(train_images)} training, {len(val_images)} validation.")

    print(f"Dataset split complete! Training data in '{train_folder}', Validation data in '{val_folder}'.")

# Example usage:
source_folder = "RPS/data_collection/data/original_data_set"  # Path to your dataset
output_folder = "RPS/data_collection/data"  # Where to store train/val folders
train_ratio = 0.8  # 80% training, 20% validation

split_dataset(source_folder, output_folder, train_ratio)