import os
import cv2
import face_recognition
import pandas as pd
from pathlib import Path

DATA_DIR = Path('dataset')
ALIGNED_DIR = Path('aligned')
ALIGNED_DIR.mkdir(exist_ok=True)

def is_frontal_face(img, face_location):
    """Return True if face is frontal based on landmarks symmetry"""
    top, right, bottom, left = face_location
    face_img = img[top:bottom, left:right]
    
    landmarks_list = face_recognition.face_landmarks(face_img)
    if not landmarks_list:
        return False
    
    landmarks = landmarks_list[0]
    
    # Check if both eyes are detected
    if 'left_eye' in landmarks and 'right_eye' in landmarks:
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']
        
        # Calculate eye center positions
        left_eye_center = sum([p[0] for p in left_eye]) / len(left_eye)
        right_eye_center = sum([p[0] for p in right_eye]) / len(right_eye)
        
        # Eyes should be roughly horizontal (difference in x small)
        eye_diff = abs(left_eye_center - right_eye_center)
        if eye_diff > 5:  # adjust threshold if needed
            return True
    return False

def crop_face_save(img_path, out_dir, prefix):
    img = face_recognition.load_image_file(img_path)
    face_locations = face_recognition.face_locations(img)
    
    if not face_locations:
        print('No face found in', img_path)
        return None

    # Only keep frontal faces
    frontal_faces = [f for f in face_locations if is_frontal_face(img, f)]
    if not frontal_faces:
        print('No frontal face in', img_path)
        return None
    
    top, right, bottom, left = frontal_faces[0]  # save first frontal face
    crop = img[top:bottom, left:right]
    crop_bgr = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)
    out_path = out_dir / f"{prefix}.jpg"
    cv2.imwrite(str(out_path), crop_bgr)
    return str(out_path)

if __name__ == '__main__':
    students_csv = DATA_DIR / 'students.csv'
    df = pd.read_csv(students_csv)
    for idx, row in df.iterrows():
        img_path = DATA_DIR / row['PHOTO']
        if os.path.exists(img_path):
            crop_face_save(img_path, ALIGNED_DIR, row['ROLL NO'])
        else:
            print(f"File not found: {img_path}")
    print('Preprocessing done. Aligned frontal faces saved in "aligned/" folder.')
