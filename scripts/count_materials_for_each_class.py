import os

def count_folders_in_materials(data_dir):
    material_folders = os.listdir(data_dir)
    folder_counts = {}

    for material in material_folders:
        material_path = os.path.join(data_dir, material)
        if os.path.isdir(material_path):
            subfolders = [f for f in os.listdir(material_path) if os.path.isdir(os.path.join(material_path, f))]
            folder_counts[material] = len(subfolders)

    return folder_counts

def print_folder_counts(folder_counts):
    for material, count in folder_counts.items():
        print(f"{material}: {count}")

if __name__ == "__main__":
    data_dir = '/Users/tabitalucaciu/UBB INFO ENGL/YEAR 3/SEM 2/Licenta/pythonProject1 copy/data'  # Change this to your actual data directory
    folder_counts = count_folders_in_materials(data_dir)
    print_folder_counts(folder_counts)
