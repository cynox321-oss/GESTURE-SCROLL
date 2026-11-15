"""
Gesture Scroll — control your computer's scroll with hand gestures via webcam.

  Open palm (5 fingers)  ->  scroll UP
  Fist (0 fingers)       ->  scroll DOWN

Neon skeleton is drawn over your hand in real time.

Install:
    pip install opencv-python mediapipe==0.10.21 pyautogui numpy

Run:
    python scroll.py
Press ESC or Q to quit.
"""

import time
from collections import deque

import cv2
import numpy as np
import mediapipe as mp
import pyautogui

# ------------------------------- CONFIG -------------------------------
CAM_INDEX       = 0        # webcam index (try 1 or 2 if 0 fails)
SCROLL_AMOUNT   = 220      # "pixels" per scroll step -> bigger = faster
SCROLL_COOLDOWN = 0.12     # seconds between scroll steps
MAX_HANDS       = 1

# --- gesture detection tuning ---
STABLE_FRAMES   = 5        # gesture must be held this many frames before acting
THUMB_RATIO     = 0.60     # thumb tip distance to index-MCP, as fraction of palm width
THUMB_STRAIGHT  = 150      # min thumb IP angle (deg) to be considered "extended"
FINGER_STRAIGHT = 150      # min PIP angle (deg) for a finger to be "extended"
# ----------------------------------------------------------------------

# Neon colors (BGR)
NEON_PINK  = (255, 40, 200)
NEON_CYAN  = (255, 255, 0)
NEON_GREEN = (80, 255, 120)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

mp_hands = mp.solutions.hands

# Skeleton chains (indices into the 21 MediaPipe hand landmarks)
FINGER_CHAINS = [
    [1, 2, 3, 4],            # thumb
    [5, 6, 7, 8],            # index
    [9, 10, 11, 12],         # middle
    [13, 14, 15, 16],        # ring
    [17, 18, 19, 20],        # pinky
]
PALM_CHAIN = [0, 5, 9, 13, 17, 0]


# ----------------------------------------------------------------------
# Math helpers
# ----------------------------------------------------------------------
def _dist(a, b):
    return float(np.hypot(a[0] - b[0], a[1] - b[1]))


def _angle(a, b, c):
    """Angle at point b (degrees)."""
    v1 = np.array(a, dtype=float) - np.array(b, dtype=float)
    v2 = np.array(c, dtype=float) - np.array(b, dtype=float)
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 < 1e-6 or n2 < 1e-6:
        return 0.0
    cos = float(np.dot(v1, v2) / (n1 * n2))
    return float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))


# ----------------------------------------------------------------------
# Gesture recognition
# ----------------------------------------------------------------------
def fingers_up(hand_landmarks, w, h):
    """
    Return ([thumb, index, middle, ring, pinky] booleans, pixel points).
    Rotation-invariant: uses joint angles + distances, not screen direction.
    """
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

    wrist      = pts[0]
    index_mcp  = pts[5]
    pinky_mcp  = pts[17]
    palm_width = _dist(index_mcp, pinky_mcp) + 1e-6

    # --- Thumb ---
    thumb_tip = pts[4]
    thumb_ip  = pts[3]
    thumb_mcp = pts[2]
    far_enough = _dist(thumb_tip, index_mcp) > THUMB_RATIO * palm_width
    straight   = _angle(thumb_mcp, thumb_ip, thumb_tip) > THUMB_STRAIGHT
    thumb_ext  = far_enough and straight

    state = [thumb_ext]

    # --- Index / Middle / Ring / Pinky ---
    for mcp, pip, dip, tip in ((5, 6, 7, 8),
                               (9, 10, 11, 12),
                               (13, 14, 15, 16),
                               (17, 18, 19, 20)):
        mcp_p = pts[mcp]
        pip_p = pts[pip]
        tip_p = pts[tip]

        straight    = _angle(mcp_p, pip_p, tip_p) > FINGER_STRAIGHT
        reaches_out = _dist(tip_p, wrist) > _dist(pip_p, wrist)
        state.append(straight and reaches_out)

    return state, pts


def classify(state, finger_count):
    """
    Return 'up', 'down' or None based on the gesture.

      UP   ->  open palm (5 fingers extended)
      DOWN ->  fist (0 fingers extended)
    """
    if finger_count == 5:
        return "up"
    if finger_count == 0:
        return "down"
    return None


# ----------------------------------------------------------------------
# Neon drawing
# ----------------------------------------------------------------------
def draw_glow(layer, pts, states):
    for i, chain in enumerate(FINGER_CHAINS):
        color = NEON_GREEN if states[i] else NEON_PINK
        for a, b in zip(chain[:-1], chain[1:]):
            cv2.line(layer, pts[a], pts[b], color, 12, cv2.LINE_AA)

    for a, b in zip(PALM_CHAIN[:-1], PALM_CHAIN[1:]):
        cv2.line(layer, pts[a], pts[b], NEON_CYAN, 12, cv2.LINE_AA)

    for p in pts:
        cv2.circle(layer, p, 10, NEON_CYAN, -1, cv2.LINE_AA)


def draw_crisp(frame, pts, states):
    for i, chain in enumerate(FINGER_CHAINS):
        color = NEON_GREEN if states[i] else NEON_PINK
        for a, b in zip(chain[:-1], chain[1:]):
            cv2.line(frame, pts[a], pts[b], color, 2, cv2.LINE_AA)

    for a, b in zip(PALM_CHAIN[:-1], PALM_CHAIN[1:]):
        cv2.line(frame, pts[a], pts[b], NEON_CYAN, 2, cv2.LINE_AA)

    for p in pts:
        cv2.circle(frame, p, 6, NEON_CYAN, 1, cv2.LINE_AA)
        cv2.circle(frame, p, 2, (255, 255, 255), -1, cv2.LINE_AA)


def draw_hud(frame, finger_count, action, stable):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 60), (10, 10, 10), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    tag = f"Fingers: {finger_count}"
    if not stable and action.endswith("(hold)"):
        tag += "  (hold...)"
    cv2.putText(frame, tag, (18, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, NEON_CYAN, 2, cv2.LINE_AA)

    color = NEON_GREEN if "UP" in action else (NEON_PINK if "DOWN" in action else (200, 200, 200))
    cv2.putText(frame, action, (w - 330, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, color, 2, cv2.LINE_AA)

    cx, cy = w - 40, h // 2
    if "UP" in action:
        cv2.arrowedLine(frame, (cx, cy + 40), (cx, cy - 40), NEON_GREEN, 4, cv2.LINE_AA, tipLength=0.4)
    elif "DOWN" in action:
        cv2.arrowedLine(frame, (cx, cy - 40), (cx, cy + 40), NEON_PINK, 4, cv2.LINE_AA, tipLength=0.4)


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------
def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        print("Could not open webcam. Try changing CAM_INDEX.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    last_scroll = 0.0
    gesture_hist = deque(maxlen=STABLE_FRAMES)

    with mp_hands.Hands(
        max_num_hands=MAX_HANDS,
        model_complexity=0,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    ) as hands:

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            result = hands.process(rgb)

            glow         = np.zeros_like(frame)
            hands_data   = []
            finger_count = 0
            action       = "-"
            stable       = False

            if result.multi_hand_landmarks:
                for hand in result.multi_hand_landmarks:
                    states, pts = fingers_up(hand, w, h)
                    finger_count = sum(states)
                    hands_data.append((pts, states))
                    draw_glow(glow, pts, states)

                    gesture = classify(states, finger_count)
                    gesture_hist.append(gesture)

                    # ---- stability check ----
                    if len(gesture_hist) == STABLE_FRAMES and len(set(gesture_hist)) == 1:
                        stable = True

                    now = time.time()

                    if gesture == "up":
                        action = "SCROLL UP" if stable else "SCROLL UP (hold)"
                        if stable and now - last_scroll > SCROLL_COOLDOWN:
                            pyautogui.scroll(SCROLL_AMOUNT)     # + = up
                            last_scroll = now

                    elif gesture == "down":
                        action = "SCROLL DOWN" if stable else "SCROLL DOWN (hold)"
                        if stable and now - last_scroll > SCROLL_COOLDOWN:
                            pyautogui.scroll(-SCROLL_AMOUNT)    # - = down
                            last_scroll = now

            else:
                # no hand -> reset buffer so the next gesture starts clean
                gesture_hist.clear()

            # ---- bloom pass ----
            glow = cv2.GaussianBlur(glow, (0, 0), 14)
            frame = cv2.addWeighted(frame, 1.0, glow, 1.4, 0)

            # ---- crisp pass ----
            for pts, states in hands_data:
                draw_crisp(frame, pts, states)

            draw_hud(frame, finger_count, action, stable)

            cv2.imshow("Gesture Scroll", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord('q')):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()