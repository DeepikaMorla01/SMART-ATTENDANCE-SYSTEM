import face_recognition
import pickle
from pathlib import Path

ALIGNED_DIR = Path("aligned")
EMBEDDINGS_FILE = Path("embeddings/centroids.pkl")
EMBEDDINGS_FILE.parent.mkdir(exist_ok=True)

embeddings = {}

for img_path in ALIGNED_DIR.glob("*.jpg"):
    # Filename format: rollno_name.jpg (e.g., 101_Deepu.jpg)
    file_name = img_path.stem
    parts = file_name.split("_", 1)

    if len(parts) == 2:
        roll_no, name = parts
    else:
        roll_no, name = parts[0], "Unknown"

    img = face_recognition.load_image_file(img_path)
    face_encodings = face_recognition.face_encodings(img)

    if face_encodings:
        embeddings[roll_no] = {
            "name": name,
            "embedding": face_encodings[0]
        }
        print(f"✅ Added {roll_no} - {name}")
    else:
        print(f"⚠️ No face found in {img_path}")

# Save embeddings
with open(EMBEDDINGS_FILE, "wb") as f:
    pickle.dump(embeddings, f)

print("🎉 Embeddings saved to", EMBEDDINGS_FILE)
