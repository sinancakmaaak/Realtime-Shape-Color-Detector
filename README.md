# Real-Time Shape & Color Detector 📷🎨🔺

A lightweight and fast Computer Vision project that processes live camera feeds to detect, identify, and track geometric shapes alongside their primary colors simultaneously in real time. 

Built using **Python** and **OpenCV**.

## ✨ Features
* **Live Shape Tracking:** Detects basic geometric shapes like triangles, rectangles, squares, circles, and polygons using contour approximation.
* **Color Recognition:** Filters and identifies prominent colors (Red, Blue, Green, Yellow, etc.) within the detected regions using the HSV color space.
* **Real-Time Labeling:** Draws bounding boxes and overlays text labels dynamically over the live video stream.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Core Library:** OpenCV (`opencv-python`)
* **Numerical Operations:** NumPy

## 📂 Project Structure
```text
├── main.py          # Main application loop and frame processing
├── requirements.txt # Project dependencies
└── README.md        # Documentation
