import cv2
from deepface import DeepFace
import os
import csv

# Dataset folder
dataset_path = "dataset"
students = {os.path.splitext(f)[0]: os.path.join(dataset_path, f)
            for f in os.listdir(dataset_path) if f.endswith((".jpg", ".png", ".jpeg"))}

# Classroom image
classroom_img = "classroom.jpg"

# Detect faces in classroom image
faces = DeepFace.extract_faces(img_path=classroom_img, enforce_detection=False)

attendance = []

for i, face in enumerate(faces):
    face_img = face["face"]  # cropped face

    recognized = False
    for name, img_path in students.items():
        try:
            result = DeepFace.verify(face_img, img_path, enforce_detection=False)
            if result["verified"]:  # Face matches
                attendance.append(name)
                print(f"✅ {name} is present")
                recognized = True
                break
        except Exception as e:
            print(f"Error comparing {name}: {e}")

    if not recognized:
        print(f"⚠️ Unknown student {i+1}")

# Save attendance to CSV
with open("attendance.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Status"])
    for name in students.keys():
        status = "Present" if name in attendance else "Absent"
        writer.writerow([name, status])

print("📄 Attendance saved to attendance.csv")
