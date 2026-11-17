"""Real-time face attendance. Press 'q' in the window to quit."""
import os
import pickle
from datetime import datetime

import cv2
import cvzone
import face_recognition
import numpy as np

import config
import database
import ui

# ---------- Camera + graphics ----------
cap = cv2.VideoCapture(config.CAMERA_INDEX)
cap.set(3, ui.WEBCAM_W)
cap.set(4, ui.WEBCAM_H)

background = cv2.imread("Resources/background.png")
if background is None:
    raise SystemExit("Resources/background.png missing. Run: python generate_resources.py")
mode_folder = "Resources/Modes"
# index 0 = active, 1 = student info, 2 = marked, 3 = already marked
modes = [cv2.imread(os.path.join(mode_folder, p)) for p in sorted(os.listdir(mode_folder))]

# ---------- Known faces ----------
print("Loading encode file ...")
if not os.path.exists(config.ENCODE_FILE):
    raise SystemExit("EncodeFile.p missing. Run: python EncodeGenerator.py")
with open(config.ENCODE_FILE, "rb") as f:
    known_encodings, student_ids = pickle.load(f)
print(f"Encode file loaded ({len(student_ids)} students)")


# ---------- Helpers ----------
def get_student_photo(student_id):
    """Get the photo (Firebase Storage if enabled, else local Images/) as 216x216."""
    img = None
    if database.storage_enabled():
        data = database.download_photo(student_id)
        if data:
            img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        for ext in (".png", ".jpg", ".jpeg"):
            path = os.path.join(config.IMAGES_FOLDER, student_id + ext)
            if os.path.exists(path):
                img = cv2.imread(path)
                break
    if img is None:
        return np.full((ui.PHOTO_SIZE, ui.PHOTO_SIZE, 3), 180, np.uint8)  # grey placeholder
    return ui.square_resize(img)


def check_in(student_id):
    """Returns (mode_type, student_info, photo). mode 1 = newly marked, 3 = already marked, 0 = no record."""
    info = database.get_student(student_id)
    if info is None:
        print(f"No database record for ID {student_id}")
        return 0, None, None

    photo = get_student_photo(student_id)
    now = datetime.now()
    try:
        last = datetime.strptime(info["last_attendance_time"], config.TIME_FORMAT)
        elapsed = (now - last).total_seconds()
    except (KeyError, ValueError):
        elapsed = float("inf")

    if elapsed > config.MARK_INTERVAL_SECONDS:
        info["total_attendance"] = int(info.get("total_attendance", 0)) + 1
        database.update_student(student_id, {
            "total_attendance": info["total_attendance"],
            "last_attendance_time": now.strftime(config.TIME_FORMAT),
        })
        return 1, info, photo
    return 3, info, photo


# ---------- Main loop ----------
mode_type, counter, student_id = 0, 0, None
student_info, student_photo = None, None

while True:
    ok, img = cap.read()
    if not ok:
        print("Could not read from camera. Check CAMERA_INDEX in config.py")
        break
    img = cv2.resize(img, (ui.WEBCAM_W, ui.WEBCAM_H))

    # shrink + RGB for faster recognition
    small = cv2.cvtColor(cv2.resize(img, (0, 0), None, 0.25, 0.25), cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(small)
    encodings = face_recognition.face_encodings(small, locations)

    frame = background.copy()
    ui.place_webcam(frame, img)
    ui.place_mode(frame, modes[mode_type])

    if locations:
        recognised = False
        for enc, (top, right, bottom, left) in zip(encodings, locations):
            distances = face_recognition.face_distance(known_encodings, enc)
            best = int(np.argmin(distances))
            if distances[best] <= config.MATCH_TOLERANCE:       # lower distance = better match
                top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                bbox = (ui.WEBCAM_X + left, ui.WEBCAM_Y + top, right - left, bottom - top)
                frame = cvzone.cornerRect(frame, bbox, rt=0)
                student_id, recognised = student_ids[best], True
                break

        if recognised and counter == 0:
            cvzone.putTextRect(frame, "Loading", (275, 400))
            cv2.imshow("Face Attendance", frame)
            cv2.waitKey(1)
            counter = 1

        if counter != 0:
            if counter == 1:   # fetch data only on the first frame
                mode_type, student_info, student_photo = check_in(student_id)
                if mode_type == 0:
                    counter = 0
            if counter != 0:
                if mode_type == 1 and counter > config.INFO_FRAMES:
                    mode_type = 2                       # switch to "Marked"
                ui.place_mode(frame, modes[mode_type])
                if mode_type == 1:
                    ui.draw_student_info(frame, student_info, student_id, student_photo)
                counter += 1
                if counter >= config.TOTAL_FRAMES:      # back to idle
                    counter, mode_type = 0, 0
                    student_info = student_photo = None
    else:
        mode_type, counter = 0, 0

    cv2.imshow("Face Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
