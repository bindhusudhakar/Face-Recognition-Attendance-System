"""Central settings shared by every script in the project."""

# --- Where student data lives ---------------------------------------------
# False = local JSON file (works instantly, no account needed)
# True  = Firebase Realtime Database (fill in the Firebase section below)
USE_FIREBASE = False
LOCAL_DB_FILE = "students.json"

# --- Firebase (only used when USE_FIREBASE = True) ------------------------
SERVICE_ACCOUNT_KEY = "serviceAccountKey.json"          # downloaded from Firebase (never commit it)
DATABASE_URL = "https://YOUR-PROJECT-default-rtdb.firebaseio.com/"   # Realtime Database URL
STORAGE_BUCKET = "YOUR-PROJECT.firebasestorage.app"     # e.g. my-app.appspot.com
DB_ROOT = "Students"                                    # top-level node in the database
# Storage may need a paid plan on new projects. False = photos are read from Images/
USE_FIREBASE_STORAGE = False

# --- Attendance logic -----------------------------------------------------
MARK_INTERVAL_SECONDS = 30     # demo value. Use 24 * 60 * 60 for once-per-day attendance
MATCH_TOLERANCE = 0.5          # lower = stricter face matching (face_recognition default is 0.6)
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# --- Camera / display -----------------------------------------------------
CAMERA_INDEX = 0               # try 1 if you have an external webcam
INFO_FRAMES = 10               # frames to show student details
TOTAL_FRAMES = 20              # frames before returning to the "Active" screen

# --- Files ----------------------------------------------------------------
IMAGES_FOLDER = "Images"
ENCODE_FILE = "EncodeFile.p"
