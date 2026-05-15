import cv2
from deepFace import DeepFace
import os
import csv

# Dataset folder
dataset_path = "dataset"
students = {os.path.splitext(f)[0]: os.path.join(dataset_path, f)
            for f in os.listdir(dataset_path) if f.endswith((".jpg", ".png", ".jpeg"))}

# Keep track of marked students
attendance = set()

# Open webcam
cap = cv2.VideoCapture(0)

print("📸 Starting webcam... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Detect faces in the frame
        faces = DeepFace.extract_faces(img_path=frame, enforce_detection=False)

        for face in faces:
            face_img = face["face"]

            for name, img_path in students.items():
                try:
                    result = DeepFace.verify(face_img, img_path, enforce_detection=False)
                    if result["verified"]:
                        attendance.add(name)
                        cv2.putText(frame, f"{name} Present", (50, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        break
                except:
                    pass

    except:
        pass

    # Show webcam feed
    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save attendance to CSV
with open("attendance.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Status"])
    for name in students.keys():
        status = "Present" if name in attendance else "Absent"
        writer.writerow([name, status])

print("📄 Attendance saved to attendance.csv")
