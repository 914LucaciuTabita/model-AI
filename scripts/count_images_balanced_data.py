import os

# Set the balanced data directory relative to the script's location
balanced_data_dir = os.path.join(os.path.dirname(__file__), '..', 'mean_balanced_data')

def count_images_in_balanced_data(balanced_data_dir):
    material_folders = os.listdir(balanced_data_dir)
    image_counts = {}

    for material in material_folders:
        material_path = os.path.join(balanced_data_dir, material)
        if os.path.isdir(material_path):
            image_count = 0
            for root, dirs, files in os.walk(material_path):
                image_count += sum(1 for file in files if file.endswith(('png', 'jpg', 'jpeg')))
            image_counts[material] = image_count

    return image_counts

# Count the number of images in each material folder
image_counts = count_images_in_balanced_data(balanced_data_dir)

# Print the results
for material, count in image_counts.items():
    print(f"{material}: {count} images")
