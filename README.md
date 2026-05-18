# Driver Drowsiness Detection System

A production-ready Python application for real-time driver drowsiness monitoring using computer vision and facial landmark analysis.

## Features

- Real-time webcam processing
- Eye aspect ratio (EAR) based drowsiness detection
- Facial landmark detection using OpenCV LBF landmark model
- Audio alarm plus on-screen warning
- Smooth performance with optimized frame handling

## Installation

1. Create a virtual environment

```bash
python -m venv venv
```

2. Activate the environment

```bash
venv\Scripts\activate
```

3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

Run the system with a single command:

```bash
python main.py
```

The application downloads the required OpenCV landmark model automatically on first run.

Press `Esc` to exit the live preview.

## Architecture

- `main.py` - entry point and real-time video loop
- `detector/eye_detector.py` - EAR computation and drowsiness state logic
- `alert/alarm.py` - audible alarm module with cross-platform fallback
- `utils/visuals.py` - status overlay and warning rendering

## Interview Talking Points

- Uses OpenCV face landmark detection with the LBF model for reliable eye tracking
- Maintains low latency by processing a single face stream and lightweight EAR math
- Integrates audio and visual alerts for robust safety feedback
- Designed for fast prototype demonstration and real-world validation

## Requirements

- Python 3.9+
- OpenCV Contrib
- NumPy
- Windows systems use built-in `winsound` for alarm audio
