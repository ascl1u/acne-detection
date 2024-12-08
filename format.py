import os
import pandas as pd

# Define class mapping
CLASS_MAP = {"acne": 0, "pimple": 1, "spot": 2}

# Paths
base_path = r"C:\Users\aliu2\OneDrive\Desktop\acne"
folders = ["train", "valid", "test"]

def convert_to_yolo(csv_path, image_dir, output_dir):
    # Validate CSV file
    print(f"Checking for annotation file: {csv_path}")
    if not os.path.exists(csv_path):
        print(f"Error: Annotation file not found at {csv_path}")
        return

    try:
        # Read the CSV file with headers
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        print(f"Error: Annotation file at {csv_path} is empty")
        return

    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Group annotations by filename
    grouped = df.groupby("filename")
    num_annotations = 0

    for filename, group in grouped:
        # Prepare YOLO annotations for a single image
        yolo_lines = []
        for _, row in group.iterrows():
            img_width = row["width"]
            img_height = row["height"]
            class_label = row["class"]
            xmin = row["xmin"]
            ymin = row["ymin"]
            xmax = row["xmax"]
            ymax = row["ymax"]

            # Check if class_label exists in CLASS_MAP
            if class_label not in CLASS_MAP:
                print(f"Error: Unrecognized class label '{class_label}' in row {row}")
                continue  # Skip this row

            # Convert to YOLO format
            class_id = CLASS_MAP[class_label]
            x_center = ((xmin + xmax) / 2) / img_width
            y_center = ((ymin + ymax) / 2) / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height

            # Add YOLO annotation line
            yolo_line = f"{class_id} {x_center} {y_center} {width} {height}\n"
            yolo_lines.append(yolo_line)

        # Write all annotations for this image to a single .txt file
        txt_filename = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
        try:
            with open(txt_filename, "w") as f:
                f.writelines(yolo_lines)
            num_annotations += len(yolo_lines)
        except IOError as e:
            print(f"Error writing to {txt_filename}: {e}")

    print(f"Processed {num_annotations} annotations from {csv_path}")

# Process each folder
for folder in folders:
    csv_path = os.path.join(base_path, folder, "_annotations.csv")  # Updated to match the correct file name
    image_dir = os.path.join(base_path, folder)
    output_dir = os.path.join(base_path, "labels", folder)

    print(f"\nProcessing {folder} folder...")
    print(f"Images directory: {image_dir}")
    print(f"Labels directory: {output_dir}")
    convert_to_yolo(csv_path, image_dir, output_dir)
    print(f"Completed processing {folder} folder.")