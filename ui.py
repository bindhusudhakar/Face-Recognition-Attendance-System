"""Layout constants and drawing helpers (no heavy dependencies, easy to test)."""
import cv2

FONT = cv2.FONT_HERSHEY_COMPLEX

# Regions on the 1280x720 background
WEBCAM_X, WEBCAM_Y, WEBCAM_W, WEBCAM_H = 55, 162, 640, 480
MODE_X, MODE_Y, MODE_W, MODE_H = 808, 44, 414, 633
PHOTO_X, PHOTO_Y, PHOTO_SIZE = 909, 175, 216


def place_webcam(bg, frame):
    bg[WEBCAM_Y:WEBCAM_Y + WEBCAM_H, WEBCAM_X:WEBCAM_X + WEBCAM_W] = frame


def place_mode(bg, mode_img):
    bg[MODE_Y:MODE_Y + MODE_H, MODE_X:MODE_X + MODE_W] = mode_img


def square_resize(img, size=PHOTO_SIZE):
    """Centre-crop to a square, then resize, so any photo fits the 216x216 slot."""
    h, w = img.shape[:2]
    s = min(h, w)
    y0, x0 = (h - s) // 2, (w - s) // 2
    return cv2.resize(img[y0:y0 + s, x0:x0 + s], (size, size))


def draw_student_info(bg, info, student_id, photo=None):
    white, grey, dark = (255, 255, 255), (100, 100, 100), (50, 50, 50)
    put = lambda text, pos, scale, color: cv2.putText(bg, str(text), pos, FONT, scale, color, 1)

    put(info.get("total_attendance", 0), (861, 125), 1, white)
    put(info.get("major", ""), (1006, 550), 0.5, white)
    put(student_id, (1006, 493), 0.5, white)
    put(info.get("standing", ""), (910, 625), 0.6, grey)
    put(info.get("year", ""), (1025, 625), 0.6, grey)
    put(info.get("starting_year", ""), (1125, 625), 0.6, grey)

    # centre the name inside the panel
    name = str(info.get("name", ""))
    (w, _), _ = cv2.getTextSize(name, FONT, 1, 1)
    put(name, (MODE_X + (MODE_W - w) // 2, 445), 1, dark)

    if photo is not None:
        bg[PHOTO_Y:PHOTO_Y + PHOTO_SIZE, PHOTO_X:PHOTO_X + PHOTO_SIZE] = photo
