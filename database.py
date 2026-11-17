"""Storage layer. One interface, two backends: a local JSON file or Firebase."""
import json
import os

import config

_firebase_ready = False


def _init_firebase():
    global _firebase_ready
    if _firebase_ready:
        return
    import firebase_admin
    from firebase_admin import credentials

    options = {"databaseURL": config.DATABASE_URL}
    if config.USE_FIREBASE_STORAGE:
        options["storageBucket"] = config.STORAGE_BUCKET
    firebase_admin.initialize_app(credentials.Certificate(config.SERVICE_ACCOUNT_KEY), options)
    _firebase_ready = True


def _load_local():
    if not os.path.exists(config.LOCAL_DB_FILE):
        return {}
    with open(config.LOCAL_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_local(data):
    with open(config.LOCAL_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_student(student_id):
    """Return the student's record (dict) or None."""
    student_id = str(student_id)
    if config.USE_FIREBASE:
        _init_firebase()
        from firebase_admin import db
        return db.reference(f"{config.DB_ROOT}/{student_id}").get()
    return _load_local().get(student_id)


def set_student(student_id, record):
    """Create or replace a student's record."""
    student_id = str(student_id)
    if config.USE_FIREBASE:
        _init_firebase()
        from firebase_admin import db
        db.reference(config.DB_ROOT).child(student_id).set(record)
    else:
        data = _load_local()
        data[student_id] = record
        _save_local(data)


def update_student(student_id, fields):
    """Change only the given fields of a student's record."""
    student_id = str(student_id)
    if config.USE_FIREBASE:
        _init_firebase()
        from firebase_admin import db
        db.reference(f"{config.DB_ROOT}/{student_id}").update(fields)
    else:
        data = _load_local()
        data.setdefault(student_id, {}).update(fields)
        _save_local(data)


def storage_enabled():
    return config.USE_FIREBASE and config.USE_FIREBASE_STORAGE


def upload_photo(student_id, png_bytes):
    _init_firebase()
    from firebase_admin import storage
    storage.bucket().blob(f"Images/{student_id}.png").upload_from_string(png_bytes, content_type="image/png")


def download_photo(student_id):
    """Return PNG bytes from Firebase Storage, or None."""
    _init_firebase()
    from firebase_admin import storage
    blob = storage.bucket().get_blob(f"Images/{student_id}.png")
    return blob.download_as_bytes() if blob is not None else None
