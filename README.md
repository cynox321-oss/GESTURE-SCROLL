# 🖐️ Gesture Scroll — Control Scrolling with Hand Gestures

Control your computer's scrolling using simple hand gestures and your webcam!

**Gesture Scroll** is a real-time hand gesture recognition system built with Python, OpenCV, and MediaPipe. It detects hand movements through your webcam and translates specific gestures into scrolling actions.

Featuring a futuristic neon hand-tracking visualization, the application provides an interactive way to control scrolling without touching your mouse or keyboard.

## 📸 Screenshots

### Gesture Detection
![Gesture Scroll Screenshot 1](Screenshot%202026-11-17%20214427.png)

### Neon Hand Tracking
![Gesture Scroll Screenshot 2](Screenshot%202026-11-17%20214443.png)

## ✨ Features

- 🖐️ **Real-Time Hand Tracking** — Detects hand landmarks using MediaPipe.
- ⬆️ **Scroll Up** — Use an open-palm gesture.
- ⬇️ **Scroll Down** — Use a closed-fist gesture.
- 🧠 **Gesture Recognition** — Identifies finger states and joint angles.
- ⚡ **Gesture Stability Detection** — Helps prevent accidental scrolling.
- 💡 **Neon Hand Skeleton** — Displays a glowing hand-tracking visualization.
- 🎨 **Color-Coded Finger Tracking** — Different colors indicate finger states.
- 📊 **Live Gesture Information** — Displays gesture status and scrolling direction.
- 🎥 **Webcam Processing** — Tracks hand movements in real time.
- ⚙️ **Customizable Controls** — Adjust scrolling speed and gesture sensitivity.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam access and image processing |
| MediaPipe | Hand landmark detection |
| NumPy | Mathematical calculations |
| PyAutoGUI | Computer scrolling control |
| Time | Scroll cooldown management |

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/cynox321-oss/GESTURE-SCROLL.git
```

### 2. Navigate to the project directory

```bash
cd GESTURE-SCROLL
```

### 3. Install dependencies

```bash
pip install opencv-python mediapipe==0.10.21 pyautogui numpy
```

## 🚀 Usage

Run the application:

```bash
python scroll.py
```

Allow webcam access when prompted.

Position your hand in front of the camera and use the supported gestures to control scrolling.

## 🎮 Gesture Controls

| Hand Gesture | Action |
|---|---|
| 🖐️ Open Palm (5 fingers) | Scroll UP |
| ✊ Closed Fist (0 fingers) | Scroll DOWN |
| Other Gestures | No scrolling |
| `ESC` or `Q` | Exit application |

**Tip:** Hold a gesture for a few frames so the stability detector can confirm it before scrolling begins.

## 🌈 Neon Visualization

Gesture Scroll includes a custom neon-style hand skeleton visualization featuring:

- Neon cyan palm connections.
- Neon pink inactive finger segments.
- Neon green extended finger segments.
- Glowing hand landmark points.
- Real-time scrolling direction indicators.

## ⚙️ Customization

You can modify the configuration variables directly in `scroll.py` to adjust the application's behavior.

### Configuration

```python
CAM_INDEX = 0
SCROLL_AMOUNT = 220
SCROLL_COOLDOWN = 0.12
MAX_HANDS = 1

STABLE_FRAMES = 5
THUMB_RATIO = 0.60
THUMB_STRAIGHT = 150
FINGER_STRAIGHT = 150
```

### Parameter Reference

| Parameter | Description |
|---|---|
| `CAM_INDEX` | Webcam device index |
| `SCROLL_AMOUNT` | Scrolling step size |
| `SCROLL_COOLDOWN` | Delay between scroll actions |
| `MAX_HANDS` | Maximum number of hands tracked |
| `STABLE_FRAMES` | Frames required to confirm a gesture |
| `THUMB_RATIO` | Thumb extension sensitivity |
| `THUMB_STRAIGHT` | Thumb joint angle threshold |
| `FINGER_STRAIGHT` | Finger joint angle threshold |

## 📁 Project Structure

```text
GESTURE-SCROLL/
│
├── scroll.py
├── README.md
│
├── Screenshot 2026-11-17 214427.png
└── Screenshot 2026-11-17 214443.png
```

## ⚠️ Requirements & Notes

- A working webcam is required.
- Python must be installed.
- MediaPipe `0.10.21` is used for hand tracking.
- PyAutoGUI requires permission to control scrolling on your computer.
- Gesture recognition may be affected by lighting, camera position, and hand visibility.
- Keep the application under supervision while it controls computer input.
- Press `ESC` or `Q` to stop the application.

## 👨‍💻 Author

**Karan Kousik**

- GitHub: [@cynox321-oss](https://github.com/cynox321-oss)
- Repository: [GESTURE-SCROLL](https://github.com/cynox321-oss/GESTURE-SCROLL)

---

⭐ If you find this project interesting, consider giving the repository a star!

**Built with Python, computer vision, and futuristic hand gestures.**
