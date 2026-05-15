import os
import cv2
import face_recognition
from pathlib import Path
import pandas as pd

# Paths
DATA_DIR = Path('dataset')
ALIGNED_DIR = Path('aligned')  # will store cropped faces
ALIGNED_DIR.mkdir(exist_ok=True)

# Function to detect and crop face
def crop_face_save(img_path, out_dir, prefix):
    img = face_recognition.load_image_file(img_path)
    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        print('No face found in', img_path)
        return []
    saved = []
    for i, (top, right, bottom, left) in enumerate(face_locations):
        crop = img[top:bottom, left:right]
        crop_bgr = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)
        out_path = out_dir / f"{prefix}_{i}.jpg"
        cv2.imwrite(str(out_path), crop_bgr)
        saved.append(str(out_path))
    return saved

# Main preprocessing
if __name__ == '__main__':
    students_csv = DATA_DIR / 'students.csv'
    df = pd.read_csv(students_csv)

    for idx, row in df.iterrows():
        paths = str(row['photo_paths']).split(';')
        for p in paths:
            p = p.strip()
            if not p:
                continue
            if not os.path.exists(p):
                print(f"Image not found: {p}")
                continue
            crop_face_save(p, ALIGNED_DIR, f"{row['RollNo']}")
    
    print('Preprocessing done. Aligned faces saved in "aligned/" folder.')
