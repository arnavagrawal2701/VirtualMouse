# Virtual Mouse using Hand Pose Estimation

## Overview

This project implements a **virtual mouse** controlled by hand gestures using a webcam.  
It uses **MediaPipe Hands** to detect hand landmarks and maps the position of the index finger to the screen to move the mouse cursor. Additional gestures are used to trigger **left click** and **right click** events.

This project is aligned with **Unit 4 – Motion and Tracking** of the Computer Vision syllabus.

## Features

- Real-time hand tracking using a webcam.
- Cursor movement controlled by the index finger.
- Left click using a thumb–index pinch gesture.
- Right click using a thumb–middle-finger pinch gesture.
- Smooth cursor movement using exponential smoothing.
- Press `q` to exit the application.

## Technologies Used

- Python
- OpenCV (`cv2`)
- MediaPipe
- PyAutoGUI

## Installation

1. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   # source venv/bin/activate  # Linux / macOS
