"""Run whenever you add or change student photos in Images/.

1. Reads every photo (file name = student ID)
2. Computes the 128-number face encoding for each
3. Saves encodings + IDs to EncodeFile.p
4. Uploads a 216x216 copy of each photo to Firebase Storage (optional)
"""
import os
import pickle
import cv2
import face_recognition
import config
import database
from ui import square_resize

encodings, student_ids = [], []
valid = (".png", ".jpg", ".jpeg")

print("Encoding started ...")
for file_name in sorted(os.listdir(config.IMAGES_FOLDER)):
    student_id, ext = os.path.splitext(file_name)
    if ext.lower() not in valid:
        continue
    img = cv2.imread(os.path.join(config.IMAGES_FOLDER, file_name))
    if img is None:
        print(f"  ! Could not read {file_name}, skipped")
        continue

    found = face_recognition.face_encodings(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # BGR -> RGB
    if not found:
        print(f"  ! No face found in {file_name}, skipped")
        continue
    encodings.append(found[0])
    student_ids.append(student_id)

    if database.storage_enabled():
        ok, png = cv2.imencode(".png", square_resize(img))
        database.upload_photo(student_id, png.tobytes())
    print(f"  + {student_id}")

print("Encoding complete")
with open(config.ENCODE_FILE, "wb") as f:
    pickle.dump([encodings, student_ids], f)
print(f"File saved: {config.ENCODE_FILE} ({len(student_ids)} students)")
