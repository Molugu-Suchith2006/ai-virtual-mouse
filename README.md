# Stella: AI-Powered Virtual Mouse

## Overview
Stella is a foundational computer vision application that enables seamless, touchless control of a system's cursor using real-time hand gesture recognition. By mapping 3D spatial hand coordinates to 2D screen resolution, the system translates physical movements into actionable digital commands.

## Core Technologies
* **Python 3.x:** Core application logic.
* **OpenCV:** Real-time video frame processing and rendering.
* **MediaPipe:** High-fidelity hand landmark detection and spatial tracking.
* **PyAutoGUI:** System-level cursor control and click simulation.

## Key Features
* **Real-Time Hand Tracking:** Utilizes MediaPipe's robust hand-tracking pipeline to identify specific 3D landmarks on the user's hand with minimal latency.
* **Spatial Coordinate Mapping:** Algorithmically scales the localized hand coordinates from the webcam feed to the system's native screen resolution.
* **Gesture Recognition:** Translates specific landmark proximities into executable system actions like left-clicks, establishing a touchless HCI (Human-Computer Interaction) interface.

## Repository Contents
* `stella1.py`: The main execution script containing the video capture loop, MediaPipe integration, and spatial mapping logic.
