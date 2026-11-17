"""Creates Resources/background.png and Resources/Modes/1-4.png.

The video ships its own artwork; this script makes matching placeholders so the
project runs out of the box. Replace the PNGs with your own design any time,
as long as the sizes stay 1280x720 (background) and 414x633 (modes).
"""
import os
import cv2
import numpy as np
from ui import FONT, MODE_W, MODE_H, WEBCAM_X, WEBCAM_Y, WEBCAM_W, WEBCAM_H, PHOTO_X, PHOTO_Y, PHOTO_SIZE, MODE_X, MODE_Y

NAVY, NAVY_DARK = (70, 42, 26), (36, 22, 14)
LIGHT, BAND = (247, 244, 240), (70, 45, 30)
BLUE, GREEN, AMBER = (235, 150, 45), (90, 200, 70), (40, 165, 240)
os.makedirs("Resources/Modes", exist_ok=True)


def centered(img, text, cx, y, scale, color, thick=1):
    (w, _), _ = cv2.getTextSize(text, FONT, scale, thick)
    cv2.putText(img, text, (cx - w // 2, y), FONT, scale, color, thick, cv2.LINE_AA)


def panel(header_color):
    p = np.full((MODE_H, MODE_W, 3), LIGHT, np.uint8)
    p[:110] = header_color
    return p


def status_panel(color, title, subtitle, icon):
    p = panel(color)
    centered(p, title, MODE_W // 2, 70, 1.1, (255, 255, 255), 2)
    cx, cy = MODE_W // 2, 330
    cv2.circle(p, (cx, cy), 120, color, 10, cv2.LINE_AA)
    if icon == "face":
        cv2.ellipse(p, (cx, cy), (62, 82), 0, 0, 360, color, 6, cv2.LINE_AA)
        cv2.circle(p, (cx - 24, cy - 14), 6, color, -1)
        cv2.circle(p, (cx + 24, cy - 14), 6, color, -1)
        cv2.ellipse(p, (cx, cy + 22), (24, 14), 0, 10, 170, color, 5, cv2.LINE_AA)
    elif icon == "check":
        cv2.polylines(p, [np.array([[cx - 55, cy], [cx - 15, cy + 45], [cx + 60, cy - 45]])], False, color, 16, cv2.LINE_AA)
    else:
        cv2.line(p, (cx, cy - 55), (cx, cy + 5), color, 16, cv2.LINE_AA)
        cv2.circle(p, (cx, cy + 50), 9, color, -1, cv2.LINE_AA)
    centered(p, subtitle, MODE_W // 2, 540, 0.65, (90, 90, 90))
    return p


def info_panel():
    p = panel(BAND)
    cv2.putText(p, "TOTAL ATTENDANCE", (53, 38), FONT, 0.45, (200, 200, 200), 1, cv2.LINE_AA)
    px, py = PHOTO_X - MODE_X, PHOTO_Y - MODE_Y
    cv2.rectangle(p, (px - 6, py - 6), (px + PHOTO_SIZE + 6, py + PHOTO_SIZE + 6), (215, 210, 205), -1)
    cv2.rectangle(p, (20, 425), (MODE_W - 20, 525), BAND, -1)
    cv2.putText(p, "ID NUMBER", (35, 449), FONT, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
    cv2.putText(p, "MAJOR", (35, 506), FONT, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
    for label, x in (("STANDING", 102), ("YEAR", 217), ("STARTING", 317)):
        cv2.putText(p, label, (x, 604), FONT, 0.4, (130, 130, 130), 1, cv2.LINE_AA)
    return p


modes = [
    status_panel(BLUE, "ACTIVE", "Look at the camera", "face"),
    info_panel(),
    status_panel(GREEN, "MARKED", "Attendance recorded", "check"),
    status_panel(AMBER, "ALREADY MARKED", "Come back later", "alert"),
]
for i, m in enumerate(modes, 1):
    cv2.imwrite(f"Resources/Modes/{i}.png", m)

# background 1280x720 with a vertical gradient
t = np.linspace(0, 1, 720)[:, None, None]
bg = (np.array(NAVY) * (1 - t) + np.array(NAVY_DARK) * t).astype(np.uint8).repeat(1280, axis=1)
cv2.putText(bg, "FACE ATTENDANCE SYSTEM", (55, 85), FONT, 1.3, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(bg, "Real-time recognition + Firebase", (57, 125), FONT, 0.6, (200, 190, 180), 1, cv2.LINE_AA)
cv2.rectangle(bg, (WEBCAM_X - 8, WEBCAM_Y - 8), (WEBCAM_X + WEBCAM_W + 8, WEBCAM_Y + WEBCAM_H + 8), (235, 150, 45), 2)
cv2.rectangle(bg, (MODE_X - 8, MODE_Y - 8), (MODE_X + MODE_W + 8, MODE_Y + MODE_H + 8), (235, 150, 45), 2)
cv2.imwrite("Resources/background.png", bg)
print("Created Resources/background.png and Resources/Modes/1-4.png")
