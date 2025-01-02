# Godseye: Real-Time Violence/Fire/Crash Detection System 🚨🔥🚗

**Godseye** is an AI-powered system for real-time detection of critical events such as **violence**, **fire**, and **car crashes**. Built on the **CLIP model**, the system processes live webcam feeds, uploaded images, and videos to identify potentially dangerous situations and sends instant alerts via **Telegram**.

---

## 📌 Features
- **Live Webcam Detection**: Analyze live video feeds for detecting critical events.
- **Image/Video Upload**: Upload photos or videos to detect incidents with high accuracy.
- **AI-Powered Detection**: Utilizes the **CLIP model** for advanced visual understanding.
- **Telegram Alerts**: Instantly notify users with detailed alerts about detected incidents.
- **Scalable API**: Backend API designed for seamless integration with other systems.

---

## 🛠️ Technology Stack
- **Python**: Core programming language.
- **Flask**: Backend framework for RESTful APIs.
- **CLIP Model**: Cutting-edge AI model for visual and textual recognition.
- **OpenCV & Pillow**: For video/image preprocessing and handling.
- **Telegram Bot API**: For alert notifications.
- **YAML**: Configuration management with `settings.yaml`.

---

## 🚀 How It Works
1. **Webcam Detection**:
   - Captures frames from the webcam and analyzes them in real-time.
   - Detects critical events and sends Telegram alerts.

2. **Image/Video Upload**:
   - Accepts images or videos for batch processing.
   - Uses the CLIP model to predict events and generate summaries.

3. **Notification System**:
   - Sends **Telegram alerts** for detected incidents, including event type and confidence score.

---
