Real-Time Face Attendance System

A face recognition attendance system built with Python, OpenCV and dlib. It identifies people through a webcam, shows their details and photo on a custom interface, records attendance, and blocks duplicate marks until a set time has passed.

Student data can be stored in a local JSON file (zero setup) or in a Firebase Realtime Database (optional, with cloud photo storage).

<!-- Add a screenshot of the running app here: ![Demo](docs/demo.png) -->
Features
Real-time face detection and recognition from a webcam
Custom graphical interface with four states: Active, Student Info, Marked, Already Marked
Duplicate-attendance protection with a configurable cooldown (30 seconds for demo, 24 hours for real use)
Pluggable storage: local JSON by default, Firebase Realtime Database and Storage optionally
Separate encoding step, so face encodings are generated once and reused
Skips photos with no detectable face instead of crashing
How it works
Images/<ID>.png
      |
      v
EncodeGenerator.py  ->  EncodeFile.p   (128-number face encodings + IDs)

AddDatatoDatabase.py -> students.json  (or Firebase: Students/<ID>)

main.py:  webcam -> detect face -> compare with known encodings
          -> look up student -> check time since last attendance
          -> update total_attendance + last_attendance_time -> show result

Face matching uses the face_recognition library (built on dlib). Each face becomes a 128-dimension encoding, and the closest known encoding within a tolerance is treated as a match.

Tech stack
Area	Tools
Language	Python 3.11
Vision	OpenCV, face_recognition (dlib), cvzone
Storage	JSON file or Firebase Realtime Database + Storage
Editor	VS Code
Project structure
face-attendance/
├── main.py                 # real-time recognition and attendance
├── EncodeGenerator.py      # builds EncodeFile.p from Images/
├── AddDatatoDatabase.py    # saves student records
├── database.py             # storage layer (local JSON or Firebase)
├── ui.py                   # layout constants and drawing helpers
├── generate_resources.py   # creates the background and mode graphics
├── config.py               # all settings in one place
├── requirements.txt
├── Images/                 # student photos, named by ID (e.g. 1001.png)
└── Resources/              # background.png and Modes/1-4.png
Setup
1. Clone and create a virtual environment
bash
git clone https://github.com/YOUR-USERNAME/face-attendance-system.git
cd face-attendance-system
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
2. Install dependencies (order matters)

dlib is the difficult package.

Windows / macOS (easiest):

bash
pip install dlib-bin
pip install face_recognition_models Click Pillow numpy "setuptools<81"
pip install opencv-python cvzone firebase-admin
pip install face_recognition --no-deps

Linux, or building dlib from source:

bash
pip install cmake
pip install dlib
pip install -r requirements.txt

Check the install:

bash
python -c "import face_recognition, cv2, cvzone, firebase_admin; print('ALL OK')"
3. Create the interface graphics
bash
python generate_resources.py

This makes Resources/background.png and Resources/Modes/1-4.png. You can replace them with your own designs if the sizes stay 1280x720 (background) and 414x633 (modes).

Usage
Put one clear, front-facing photo per person in Images/, named by ID (for example 1001.png).
Edit the data dictionary in AddDatatoDatabase.py so the IDs match your photos.
Run, in this order:
bash
python AddDatatoDatabase.py     # save student records
python EncodeGenerator.py       # run again whenever photos change
python main.py                  # press q to quit

On macOS, allow camera access for VS Code or your terminal when prompted (System Settings > Privacy & Security > Camera).

Using Firebase (optional)
Create a project at console.firebase.google.com and add a Realtime Database (test mode for development).
Go to Project settings > Service accounts > Generate new private key and save it as serviceAccountKey.json in the project root.
In config.py, set:
python
USE_FIREBASE = True
DATABASE_URL = "https://your-project-default-rtdb.firebaseio.com/"
Optional: for cloud photo storage, enable Firebase Storage (it may need a paid plan on new projects), set STORAGE_BUCKET, and set USE_FIREBASE_STORAGE = True.
Configuration

All settings are in config.py.

Setting	Purpose	Default
USE_FIREBASE	False = local JSON, True = Firebase	False
MARK_INTERVAL_SECONDS	Cooldown between attendance marks	30 (use 86400 for daily)
MATCH_TOLERANCE	Lower means stricter matching	0.5
CAMERA_INDEX	Webcam to use (try 1 for external)	0
INFO_FRAMES / TOTAL_FRAMES	How long each screen is shown	10 / 20
Troubleshooting
Problem	Fix
EncodeFile.p missing	Run python EncodeGenerator.py first
0 students after encoding	Check that photos are in Images/, named like 1001.png, with a clearly visible face. HEIC files are not supported, so convert them to PNG or JPG
Camera window does not open	Allow camera access in system settings, close Zoom or Teams, try CAMERA_INDEX = 1
pkg_resources error	pip install "setuptools<81"
dlib fails to build on macOS	Use pip install dlib-bin instead
Firebase permission denied	Test-mode rules expire after 30 days. Extend them in the Rules tab
Privacy and security
Face images and encodings are personal data. Get consent before using real people's photos.
Never commit serviceAccountKey.json, students.json, EncodeFile.p or photos. They are already in .gitignore.
Tighten Firebase security rules before any real deployment.
Possible improvements
Attendance report page or CSV export
Web version (Flask or Streamlit)
Asynchronous database calls to remove the small delay when a face appears
Liveness detection to prevent photo spoofing
Admin screen for registering new students
Acknowledgements

Based on the face attendance tutorial by Murtaza's Workshop, which uses the face_recognition library by Adam Geitgey. This version adds a switchable local or Firebase storage layer, automatic photo resizing, error handling and generated interface graphics.

Author
Bindhu
