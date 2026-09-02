import os
from pathlib import Path
from PIL import Image
import pandas as pd

# ==========================================
# 1. DATASET LOCATION
# ==========================================

DATASET_DIR = Path("../dataset")

# Image formats that we will accept
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# ==========================================
# 2. FIND ALL IMAGES
# ==========================================

def get_images():

    image_data = []

    # Each folder represents one disease/class
    for class_folder in DATASET_DIR.iterdir():

        if not class_folder.is_dir():
            continue

        class_name = class_folder.name

        for image_path in class_folder.rglob("*"):

            if image_path.suffix.lower() in IMAGE_EXTENSIONS:

                image_data.append({
                    "image_path": str(image_path),
                    "class_name": class_name
                })

    return pd.DataFrame(image_data)


# ==========================================
# 3. LOAD DATASET INFORMATION
# ==========================================

df = get_images()

print("\n================================")
print("DATASET INFORMATION")
print("================================")

print("Total images:", len(df))

print("\nNumber of classes:", df["class_name"].nunique())

print("\nClasses:")
for class_name in sorted(df["class_name"].unique()):
    print("-", class_name)


# ==========================================
# 4. COUNT IMAGES PER CLASS
# ==========================================

print("\n================================")
print("IMAGES PER CLASS")
print("================================")

class_counts = df["class_name"].value_counts()

print(class_counts)


# ==========================================
# 5. CHECK CORRUPTED IMAGES
# ==========================================

print("\n================================")
print("CHECKING IMAGES")
print("================================")

bad_images = []

for image_path in df["image_path"]:

    try:

        with Image.open(image_path) as img:

            # Verify that the image can be opened
            img.verify()

    except Exception:

        bad_images.append(image_path)


print("Corrupted images:", len(bad_images))

if len(bad_images) > 0:

    print("\nCorrupted files:")

    for image in bad_images:
        print(image)


# ==========================================
# 6. IMAGE SIZE INFORMATION
# ==========================================

print("\n================================")
print("IMAGE SIZE CHECK")
print("================================")

sizes = {}

for image_path in df["image_path"]:

    try:

        with Image.open(image_path) as img:

            size = img.size

            if size not in sizes:
                sizes[size] = 0

            sizes[size] += 1

    except Exception:
        pass


print("Different image sizes found:")

for size, count in sorted(
    sizes.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(size, "->", count, "images")


# ==========================================
# 7. SAVE DATASET INFORMATION
# ==========================================

df.to_csv("../dataset_information.csv", index=False)

print("\nDataset information saved to:")
print("../dataset_information.csv")