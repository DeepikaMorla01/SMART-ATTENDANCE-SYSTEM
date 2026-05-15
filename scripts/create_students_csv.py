import pandas as pd
from pathlib import Path

# Folder where all student subfolders exist
DATASET_DIR = Path("dataset")

# List all student folders (each folder should be named as student name)
student_folders = [f for f in DATASET_DIR.iterdir() if f.is_dir()]

# Prepare student data
students_data = []

for folder in student_folders:
    # Example: folder.name = "Sita"
    student_name = folder.name
    
    # Generate a roll number automatically (optional: customize if needed)
    roll_no = "CS" + folder.name[:3].upper() + "01"  # simple example
    
    # Department, Class, Section (you can customize if needed)
    department = "CSE"
    class_name = "BTech"
    section = "A"
    
    # Get all JPG images in this folder
    photos = [str(p) for p in folder.glob("*.jpg")]
    photo_paths = ";".join(photos)  # semicolon separated
    
    students_data.append({
        "Name": student_name,
        "RollNo": roll_no,
        "Department": department,
        "Class": class_name,
        "Section": section,
        "photo_paths": photo_paths,
        "Status": "Absent"
    })

# Create DataFrame
df = pd.DataFrame(students_data, columns=["Name","RollNo","Department","Class","Section","photo_paths","Status"])

# Save CSV
csv_path = DATASET_DIR / "students.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")

print(f"✅ CSV file created successfully at: {csv_path}")
