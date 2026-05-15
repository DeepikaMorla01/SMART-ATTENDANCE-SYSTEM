import os
from deepface import DeepFace

# Path to dataset of student images
dataset_path = "dataset"

# Dictionary to store student image paths
students = {}

# Loop through dataset folder
for filename in os.listdir(dataset_path):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        student_name = os.path.splitext(filename)[0]  # Name without extension
        image_path = os.path.join(dataset_path, filename)
        students[student_name] = image_path

print("✅ Loaded student dataset:")
for name in students:
    print(f"- {name}")
