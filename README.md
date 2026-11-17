# Real-Time Face Attendance System (OpenCV + face_recognition + Firebase)

Recognises students through a webcam, pulls their record and photo from Firebase,
marks attendance, and blocks duplicate marks until a cooldown has passed (30 s demo, configurable to 24 h).

## How it works
`Images/<ID>.png` -> **EncodeGenerator.py** -> `EncodeFile.p` (128-number face encodings + IDs)
`AddDatatoDatabase.py` -> Firebase Realtime DB (`Students/<ID>`)
**main.py** -> webcam -> match face -> fetch record -> update `total_attendance` + `last_attendance_time`

Screens: Active -> Student details + photo -> Marked, or "Already marked" if within the cooldown.

## 1. Open in VS Code
1. Unzip, then **File > Open Folder** and choose `face-attendance`.
2. Install the *Python* extension.
3. Open a terminal (**Ctrl+`**) and create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate          # Windows   (macOS/Linux: source .venv/bin/activate)
   ```
4. **Ctrl+Shift+P > Python: Select Interpreter** and choose the `.venv` one.
   Python 3.10 to 3.12 is recommended.

## 2. Install dependencies (order matters)
dlib is the tricky one:
```
pip install cmake
pip install dlib            # needs a C++ compiler (Windows: Visual Studio "Desktop development with C++")
```
No compiler? On Windows try `pip install dlib-bin` instead.
Then:
```
pip install -r requirements.txt
```

## 3. Firebase setup
1. https://console.firebase.google.com > **Add project**.
2. **Build > Realtime Database > Create database > Test mode**. Copy its URL into `config.py` (`DATABASE_URL`).
3. **Project settings > Service accounts > Python > Generate new private key**.
   Save the file as `serviceAccountKey.json` in the project root. Keep it private. It is already in `.gitignore`.
4. (Optional) **Build > Storage** for photos. Copy the bucket name (without `gs://`) into `STORAGE_BUCKET`.
   If Storage asks for a paid plan, set `USE_FIREBASE_STORAGE = False` in `config.py`. Photos are then read from `Images/`.

## 4. Add students
1. Put one clear, front-facing photo per student in `Images/`, **named by ID** (e.g. `321654.png`).
2. Edit the `data` dict in `AddDatatoDatabase.py` so the IDs match your photos.

## 5. Run (in this order)
```
python generate_resources.py     # once: creates background + mode graphics (or use your own PNGs)
python AddDatatoDatabase.py      # uploads student records
python EncodeGenerator.py        # re-run whenever photos change
python main.py                   # press q to quit
```

## Tweaks (`config.py`)
| Setting | Purpose |
|---|---|
| `MARK_INTERVAL_SECONDS` | 30 for demo, `86400` for once per day |
| `MATCH_TOLERANCE` | lower = stricter matching |
| `CAMERA_INDEX` | try 1 for an external webcam |
| `USE_FIREBASE_STORAGE` | False = read photos locally |

## Troubleshooting
- **`No module named pkg_resources` / face_recognition_models error**: `pip install "setuptools<81"`.
- **Camera does not open**: change `CAMERA_INDEX`; close Zoom/Teams.
- **Permission denied in Firebase**: Test-mode rules expire after 30 days. Re-open the Rules tab and extend them.
- **Slight lag when a face appears**: expected. Data is downloaded synchronously.

## Notes
- Face data is personal data. Get consent before using real people's photos, and tighten Firebase rules before any real deployment.
- Never commit `serviceAccountKey.json`.
