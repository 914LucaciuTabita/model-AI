import shutil
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError

# Set the data directory relative to the script's location
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
output_dir = os.path.join(os.path.dirname(__file__), '..', 'mean_balanced_data')

# Delete the existing balanced_data directory
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
    print(f"Deleted existing output directory: {output_dir}")

def count_images_in_materials(data_dir):
    material_folders = os.listdir(data_dir)
    image_counts = {}

    for material in material_folders:
        material_path = os.path.join(data_dir, material)
        if os.path.isdir(material_path):
            image_count = 0
            for root, dirs, files in os.walk(material_path):
                image_count += sum(1 for file in files if file.endswith(('png', 'jpg', 'jpeg')))
            image_counts[material] = image_count

    return image_counts

def copy_and_refactor_images(data_dir, output_dir):
    for material in os.listdir(data_dir):
        material_path = os.path.join(data_dir, material)
        output_material_path = os.path.join(output_dir, material)

        if not os.path.exists(output_material_path):
            os.makedirs(output_material_path)
            print(f"Created material directory: {output_material_path}")

        if os.path.isdir(material_path):
            counter = 0
            for root, dirs, files in os.walk(material_path):
                for file in files:
                    if file.endswith(('png', 'jpg', 'jpeg')):
                        src_path = os.path.join(root, file)
                        new_filename = f"{os.path.splitext(file)[0]}_{counter}{os.path.splitext(file)[1]}"
                        dst_path = os.path.join(output_material_path, new_filename)
                        shutil.copy2(src_path, dst_path)
                        counter += 1
                        print(f"Copied and renamed {src_path} to {dst_path}")

def custom_augmentation(image):
    # Convert to PIL Image
    image = tf.keras.preprocessing.image.array_to_img(image)

    # Apply contrast stretching (enhancement)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(np.random.uniform(0.8, 1.2))

    # Apply Gaussian blur
    image = image.filter(ImageFilter.GaussianBlur(radius=np.random.uniform(0.1, 2.0)))

    # Convert back to numpy array
    image = tf.keras.preprocessing.image.img_to_array(image)
    return image

def balance_dataset(data_dir, output_dir, max_count):
    datagen = ImageDataGenerator(
        rotation_range=15,      # Small rotations
        width_shift_range=0.1,  # Small width shift
        height_shift_range=0.1, # Small height shift
        shear_range=0.1,        # Small shearing
        zoom_range=0.1,         # Small zoom
        horizontal_flip=True,   # Horizontal flip
        fill_mode='nearest',    # Filling mode
        brightness_range=[0.8, 1.2]
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    for material in os.listdir(data_dir):
        material_path = os.path.join(data_dir, material)
        output_material_path = os.path.join(output_dir, material)

        if not os.path.exists(output_material_path):
            os.makedirs(output_material_path)
            print(f"Created material directory: {output_material_path}")

        if os.path.isdir(material_path):
            image_paths = []
            for root, dirs, files in os.walk(material_path):
                for file in files:
                    if file.endswith(('png', 'jpg', 'jpeg')):
                        image_paths.append(os.path.join(root, file))

            current_count = len(image_paths)
            print(f"Processing material '{material}' with {current_count} images...")

            if current_count * 2 <= max_count:
                target_count = current_count * 2
            elif current_count * 4 / 3 <= max_count:
                target_count = int(current_count * 4 / 3)
            else:
                target_count = max_count

            print(f"Target count for material '{material}' is {target_count}")

            if current_count < target_count:
                total_augmented = 0
                for image_path in image_paths:
                    try:
                        image = tf.keras.preprocessing.image.load_img(image_path)
                        image_array = tf.keras.preprocessing.image.img_to_array(image)
                        image_array = np.expand_dims(image_array, axis=0)
                    except UnidentifiedImageError:
                        print(f"Skipping file {image_path}, as it is not a valid image.")
                        continue

                    num_augmentations = (target_count - current_count) // current_count
                    extra_augmentations = (target_count - current_count) % current_count

                    for _ in range(num_augmentations):
                        for batch in datagen.flow(image_array, batch_size=1):
                            augmented_image = custom_augmentation(batch[0])
                            save_path = os.path.join(output_material_path, f'aug_{total_augmented}.jpeg')
                            tf.keras.preprocessing.image.save_img(save_path, augmented_image)
                            total_augmented += 1
                            break

                    if extra_augmentations > 0:
                        for batch in datagen.flow(image_array, batch_size=1):
                            augmented_image = custom_augmentation(batch[0])
                            save_path = os.path.join(output_material_path, f'aug_{total_augmented}.jpeg')
                            tf.keras.preprocessing.image.save_img(save_path, augmented_image)
                            total_augmented += 1
                            extra_augmentations -= 1
                            break

                print(f"Augmented {total_augmented} images for material '{material}'")

# Count the number of images in each material folder
image_counts = count_images_in_materials(data_dir)
max_count = max(image_counts.values())
print(f"Maximum count of images in any material: {max_count}")

# Copy and refactor original images to the balanced_data directory
copy_and_refactor_images(data_dir, output_dir)

# Balance the dataset
balance_dataset(data_dir, output_dir, max_count)
print("Balancing complete.")
