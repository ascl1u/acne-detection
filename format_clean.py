import os
import random
from shutil import move

# Directories
base_dir = "acne"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")

# Subdirectories for splits
splits = ["train", "valid", "test"]

# Split ratios for new images
split_ratios = {"train": 0.7, "valid": 0.2, "test": 0.1}

# Ensure split directories exist
for split in splits:
    os.makedirs(os.path.join(images_dir, split), exist_ok=True)
    os.makedirs(os.path.join(labels_dir, split), exist_ok=True)

# Gather all images in the main images directory (new images to be split)
new_images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))]

# Shuffle the new images for randomness
random.shuffle(new_images)

# Calculate split sizes for new images
total_new_images = len(new_images)
train_cutoff = int(total_new_images * split_ratios["train"])
valid_cutoff = train_cutoff + int(total_new_images * split_ratios["valid"])

# Assign new images to splits
split_new_images = {
    "train": new_images[:train_cutoff],
    "valid": new_images[train_cutoff:valid_cutoff],
    "test": new_images[valid_cutoff:]
}

# Move new images to their respective directories and create empty labels
for split, images in split_new_images.items():
    split_image_dir = os.path.join(images_dir, split)
    split_label_dir = os.path.join(labels_dir, split)

    for image in images:
        # Move the image to the respective split directory
        src_image_path = os.path.join(images_dir, image)
        dst_image_path = os.path.join(split_image_dir, image)
        move(src_image_path, dst_image_path)

        # Create an empty annotation file for the image
        label_file = os.path.splitext(image)[0] + ".txt"
        label_file_path = os.path.join(split_label_dir, label_file)
        open(label_file_path, 'w').close()  # Create an empty file

print("New images successfully split and annotation files created.")