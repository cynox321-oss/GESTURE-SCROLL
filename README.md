# 🖐️ Gesture Scroll

A real-time **Hand Gesture-Controlled Scrolling System** that lets you control your computer's scrolling using simple hand gestures through your webcam.

Built with Python, OpenCV, MediaPipe, NumPy, and PyAutoGUI, this project detects hand movements, recognizes finger gestures, and translates them into scrolling actions.

It also features a glowing neon hand skeleton visualization for a futuristic experience.

## ✨ Features

- 🖐️ Real-time hand tracking using MediaPipe
- ⬆️ Open palm gesture to scroll up
- ⬇️ Fist gesture to scroll down
- 🧠 Gesture recognition using finger states and joint angles
- ⚡ Gesture stability detection to reduce accidental scrolling
- 💡 Neon glow hand skeleton visualization
- 🎨 Color-coded finger tracking
- 📊 Live gesture information and status display
- 🎥 Real-time webcam processing
- ⚙️ Customizable scrolling speed and gesture sensitivity

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

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

**2. Install dependencies**

```bash
pip install opencv-python mediapipe==0.10.21 pyautogui numpy
```

## 🚀 Usage

Run the application:

```bash
python scroll.py
```

Allow webcam access when prompted.

Position your hand in front of the camera and start controlling your computer's scrolling with gestures.

## 🎮 Gesture Controls

| Hand Gesture | Action |
|---|---|
| 🖐️ Open palm (5 fingers) | Scroll UP |
| ✊ Closed fist (0 fingers) | Scroll DOWN |
| Other gestures | No scrolling |
| `ESC` or `Q` | Exit application |

**Note:** Hold the gesture for a few frames to allow the stability detector to confirm it before scrolling begins.

## 🌈 Neon Visualization

The application renders a custom hand skeleton with:

- Neon cyan palm connections
- Neon pink inactive finger segments
- Neon green extended finger segments
- Glowing landmark points
- Real-time scrolling direction indicators

## ⚙️ Customization

You can modify the configuration variables in `scroll.py`:

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

| Parameter | Description |
|---|---|
| `CAM_INDEX` | Webcam device index |
| `SCROLL_AMOUNT` | Scrolling step size |
| `SCROLL_COOLDOWN` | Delay between scroll actions |
| `STABLE_FRAMES` | Frames required to confirm a gesture |
| `THUMB_RATIO` | Thumb extension sensitivity |
| `THUMB_STRAIGHT` | Thumb joint angle threshold |
| `FINGER_STRAIGHT` | Finger joint angle threshold |

## 📁 Project Structure

```text
GESTURE-SCROLL/
│
├── scroll.py
└── README.md
```

## ⚠️ Requirements & Notes

- A working webcam is required.
- Python must be installed.
- MediaPipe 0.10.21 is used for hand tracking.
- PyAutoGUI needs permission to control scrolling on your computer.
- Gesture recognition can be affected by lighting, camera position, and hand visibility.

**Safety:** Keep the application under supervision while it controls computer input. Stop it with `ESC` or `Q` when finished.

## 👨‍💻 Author

**Karan Kousik**

GitHub: [@cynox321-oss](https://github.com/cynox321-oss)

---

⭐ If you find this project interesting, consider giving it a star!

*Built with Python, computer vision, and futuristic hand gestures.*
