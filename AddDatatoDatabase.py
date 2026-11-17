"""Run once (and again whenever you edit a student): saves student records.

Local mode  -> writes students.json
Firebase    -> writes to your Realtime Database
"""
import config
import database

# Key = student ID. It must match the photo file name in Images/ (e.g. Images/1001.png).
# These are samples. Replace them with real students.
data = {
    "1001": {
        "name": "Your Name",
        "major": "Data Science",
        "starting_year": 2022,
        "total_attendance": 0,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-01-01 00:00:00",
    },
    "1002": {
        "name": "Student Two",
        "major": "Economics",
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B",
        "year": 1,
        "last_attendance_time": "2022-01-01 00:00:00",
    },
    "1003": {
        "name": "Student Three",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2022-01-01 00:00:00",
    },
}

for student_id, record in data.items():
    database.set_student(student_id, record)
    print(f"Saved {student_id}: {record['name']}")

where = "Firebase" if config.USE_FIREBASE else config.LOCAL_DB_FILE
print(f"Done. Records stored in: {where}")
