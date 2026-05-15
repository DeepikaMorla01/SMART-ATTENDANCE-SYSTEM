import cv2
import os

student_name = "Deepu"
save_path = f"dataset/{student_name}"
os.makedirs(save_path, exist_ok=True)

cam = cv2.VideoCapture(0)

count = 0
while True:
    ret, frame = cam.read()
    if not ret:
        break
    cv2.imshow("Capture - Press s to save, q to quit", frame)

    key = cv2.waitKey(1)
    if key == ord("s"):  # Press 's' to save
        count += 1
        file_name = os.path.join(save_path, f"{student_name}_{count}.jpg")
        cv2.imwrite(file_name, frame)
        print(f"Saved: {file_name}")
    elif key == ord("q"):  # Press 'q' to quit
        break

cam.release()
cv2.destroyAllWindows()
