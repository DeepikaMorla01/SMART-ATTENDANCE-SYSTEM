from flask import Flask, render_template, request, jsonify, send_from_directory
import face_recognition
import pickle
import pandas as pd
from pathlib import Path
import datetime

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="templates"
)

# Paths
DATA_DIR = Path('.')
EMBEDDINGS_FILE = DATA_DIR / 'embeddings/centroids.pkl'
DOWNLOADS_DIR = DATA_DIR / 'templates/downloads'
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Load students CSV
df = pd.read_csv(DATA_DIR / 'students.csv')

# Load embeddings
with open(EMBEDDINGS_FILE, 'rb') as f:
    embeddings = pickle.load(f)

# Function to mark attendance
def mark_attendance(file_path):
    unknown_img = face_recognition.load_image_file(file_path)
    unknown_encodings = face_recognition.face_encodings(unknown_img)

    attendance = [{"rollNo": row['ROLL NO'], "name": row['NAME'], "status": "Absent"} for idx, row in df.iterrows()]

    for unknown_face in unknown_encodings:
        for idx, row in df.iterrows():
            roll_no = row['ROLL NO']
            known_face = embeddings.get(roll_no)
            if known_face is not None:
                match = face_recognition.compare_faces([known_face], unknown_face, tolerance=0.5)
                if match[0]:
                    attendance[idx]['status'] = 'Present'

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    output_file = DOWNLOADS_DIR / f"attendance_{today}.xlsx"
    pd.DataFrame(attendance).to_excel(output_file, index=False)

    return attendance, str(output_file)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/students')
def students():
    return render_template('students.html', students=df.to_dict(orient='records'))

@app.route('/attendance')
def attendance_page():
    total = len(df)
    return render_template('attendance.html', total=0, present=0, absent=0, students=[])

@app.route('/dashboard')
def dashboard():
    total = len(df)
    attendance_files = sorted(DOWNLOADS_DIR.glob("attendance_*.xlsx"), reverse=True)

    if attendance_files:
        latest_file = attendance_files[0]
        df_attendance = pd.read_excel(latest_file)
        present = len(df_attendance[df_attendance['status'] == 'Present'])
        absent = len(df_attendance[df_attendance['status'] == 'Absent'])
    else:
        present = 0
        absent = total

    return render_template('dashboard.html', total=total, present=present, absent=absent)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance_route():
    if 'classroomImage' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['classroomImage']
    file_path = DOWNLOADS_DIR / file.filename
    file.save(file_path)

    attendance, download_path = mark_attendance(file_path)
    return jsonify({"attendance": attendance, "download_path": download_path})

# Serve CSS/JS
@app.route('/templates/<path:filename>')
def custom_static(filename):
    return send_from_directory('templates', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
