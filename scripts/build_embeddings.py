import os
import pickle
from pathlib import Path
import face_recognition

# Paths
ALIGNED_DIR = Path("aligned")   # cropped faces folder
EMB_DIR = Path("embeddings")    # folder to save embeddings
EMB_DIR.mkdir(exist_ok=True)

# Dictionary to store embeddings for each student
embeddings = {}

# Loop over all images in aligned folder
for img_path in ALIGNED_DIR.glob("*.jpg"):
    # Example filename: CS201_0.jpg
    roll_no = img_path.stem.split("_")[0]  # extract RollNo
    
    # Load image and get face encodings
    img = face_recognition.load_image_file(img_path)
    encs = face_recognition.face_encodings(img)
    
    if len(encs) == 0:
        print(f"No face found in {img_path}, skipping...")
        continue
    
    # Take the first encoding (should be only one face)
    encoding = encs[0]
    
    # Add to dictionary
    if roll_no in embeddings:
        embeddings[roll_no].append(encoding)
    else:
        embeddings[roll_no] = [encoding]

# Average embeddings per student (optional but recommended)
centroids = {}
for roll_no, enc_list in embeddings.items():
    import numpy as np
    centroids[roll_no] = np.mean(enc_list, axis=0)

# Save embeddings to file
with open(EMB_DIR / "centroids.pkl", "wb") as f:
    pickle.dump(centroids, f)

print(f"✅ Embeddings saved to {EMB_DIR / 'centroids.pkl'}")
