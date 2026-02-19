import os
import shutil
import random

SOURCE_DIR = r"C:\Users\peela\.cache\kagglehub\datasets\jessicali9530\stanford-dogs-dataset\versions\2\Images"
TARGET_DIR = "dataset"

SPLIT_RATIO = 0.8  # 80% train, 20% test

os.makedirs(TARGET_DIR + "/train", exist_ok=True)
os.makedirs(TARGET_DIR + "/test", exist_ok=True)

for breed in os.listdir(SOURCE_DIR):
    breed_path = os.path.join(SOURCE_DIR, breed)

    if not os.path.isdir(breed_path):
        continue

    images = [f for f in os.listdir(breed_path)
              if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if len(images) < 10:
        continue  # skip tiny classes

    random.shuffle(images)
    split = int(len(images) * SPLIT_RATIO)

    train_imgs = images[:split]
    test_imgs = images[split:]

    os.makedirs(f"{TARGET_DIR}/train/{breed}", exist_ok=True)
    os.makedirs(f"{TARGET_DIR}/test/{breed}", exist_ok=True)

    for img in train_imgs:
        shutil.copy(
            os.path.join(breed_path, img),
            f"{TARGET_DIR}/train/{breed}/{img}"
        )

    for img in test_imgs:
        shutil.copy(
            os.path.join(breed_path, img),
            f"{TARGET_DIR}/test/{breed}/{img}"
        )

print("✅ Dataset successfully split into train and test")
