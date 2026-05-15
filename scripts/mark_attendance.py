from flask import Flask, request, render_template, jsonify
import os
from pathlib import Path
import pandas as pd
import pickle
import face_recognition
import numpy as np
from PIL import Image
from datetime import datetime

app = Flask(__name__)

# Paths
CLASSROOM_DIR = Path("C:/Users/deepi/OneDrive/Desktop/SmartAttendanceSystem/classroom_photos")
CLASSROOM_DIR.mkdir(exist_ok=True)
EMB_DIR = Path("C:/Users/deepi/OneDrive/Desktop/SmartAttendanceSystem/embeddings")
DATA_CSV = Path("C:/Users/deepi/OneDrive/Desktop/SmartAttendanceSystem/dataset/students.csv")
REPORT_DIR = Path("C:/Users/deepi/OneDrive/Desktop/SmartAttendanceSystem/reports")
REPORT_DIR.mkdir(exist_ok=True)

# Load embeddings
with open(EMB_DIR / "centroids.pkl", "rb") as f:
    embeddings = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'classroomImage' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['classroomImage']
    file_path = CLASSROOM_DIR / file.filename
    file.save(file_path)
    print("Saved uploaded file at:", file_path)

    # Load student CSV
    df = pd.read_csv(DATA_CSV)
    df["Status"] = "Absent"

    try:
        # Open image safely with PIL and convert to RGB
        pil_image = Image.open(file_path).convert('RGB')
        pil_image.save(file_path)  # overwrite to ensure compatible format
        img = face_recognition.load_image_file(file_path)
    except Exception as e:
        print("Error loading image:", e)
        return jsonify({"error": "Cannot read uploaded image"}), 500

    # Detect faces
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    # Compare each face with embeddings
    for face_encoding in face_encodings:
        for roll_no, emb in embeddings.items():
            distance = np.linalg.norm(face_encoding - emb)
            if distance < 0.5:
                df.loc[df["RollNo"] == roll_no, "Status"] = "Present"

    # Save attendance to Excel with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    excel_path = REPORT_DIR / f"attendance_{timestamp}.xlsx"
    df.to_excel(excel_path, index=False, engine="openpyxl")
    print("Attendance saved to:", excel_path)

    # Return JSON results
    result = df[["Name", "RollNo", "Status"]].to_dict(orient="records")
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
print("Attendance saved to:", excel_path)
