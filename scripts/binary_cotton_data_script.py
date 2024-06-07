import shutil
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import UnidentifiedImageError

# Set the data directory relative to the script's location
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
output_dir = os.path.join(os.path.dirname(__file__), '..', 'binary_cotton_data')
cotton_dir = os.path.join(output_dir, 'Cotton')
non_cotton_dir = os.path.join(output_dir, 'Non-Cotton')

# Define Non-Cotton categories
non_cotton_categories = ['Polyester', 'Satin', 'Silk', 'Terrycloth', 'Viscose', 'Nylon', 'Linen', 'Fleece', 'Denim', 'Crepe']

# Delete the existing binary_cotton_data directory if it exists
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
    print(f"Deleted existing output directory: {output_dir}")

# Create the output directories if they don't exist
os.makedirs(cotton_dir, exist_ok=True)
os.makedirs(non_cotton_dir, exist_ok=True)

# Function to copy images from source to destination with unique names
def copy_images(src_dir, dst_dir, class_name):
    counter = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg')):
                src_path = os.path.join(root, file)
                # Create a unique filename
                new_filename = f"{class_name}_{counter}{os.path.splitext(file)[1]}"
                dst_path = os.path.join(dst_dir, new_filename)
                shutil.copy2(src_path, dst_path)
                counter += 1
                print(f"Copied {src_path} to {dst_path}")

# Copy Cotton images
cotton_src_dir = os.path.join(data_dir, 'Cotton')
copy_images(cotton_src_dir, cotton_dir, 'Cotton')

# Copy Non-Cotton images
for category in non_cotton_categories:
    category_src_dir = os.path.join(data_dir, category)
    copy_images(category_src_dir, non_cotton_dir, category)

print("Binary classification data preparation complete.")
