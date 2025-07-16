<<<<<<< HEAD
# Violence Detection System

## Overview
This project is a full-stack violence and anomaly detection system using deep learning (CLIP) for image/video/webcam analysis. It features:
- **Backend:** Python Flask API for predictions and Telegram alerts (with live location)
- **Frontend:** React app for uploading images/videos and live webcam predictions
- **Alerting:** Sends Telegram alerts (with live location) for dangerous scenarios

---

## Features
- Detects violence, fire, car crash, street violence, and more in images, videos, and live webcam
- Multi-label output: returns all relevant scenarios above a confidence threshold
- Sends Telegram alerts (with live location) for dangerous events
- Cooldown logic to avoid alert spamming
- Modern React frontend for easy use

---

## Project Structure
```
godsEye/
  backend/
    backend.py           # Flask API
    model.py             # CLIP-based model logic
    settings.yaml        # Model and label configuration
    requirements.txt     # Python dependencies
    venv/                # Python virtual environment
  frontend/
    ...                  # React app (src/, public/, etc.)
  README.md
```

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <repo-url>
cd godsEye
```

### 2. Backend Setup
#### a. Create and Activate Virtual Environment (Python 3.9 recommended)
```sh
cd backend
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### b. Install Dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

#### c. Configure Environment Variables
Create a `.env` file in `backend/` with:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

#### d. Run the Backend Server
```sh
FLASK_APP=backend.py flask run --host=0.0.0.0 --port=5000
```

---

### 3. Frontend Setup
```sh
cd ../frontend
npm install
npm start
```
- The React app will run on [http://localhost:3000](http://localhost:3000)

---

## How It Works
- **Image/Video Upload:** Upload an image or video for violence/anomaly detection. The backend returns all detected scenarios above the confidence threshold.
- **Live Webcam:** Start the webcam for real-time predictions. The frontend sends frames (and your live location) to the backend every second.
- **Telegram Alerts:** If a dangerous scenario is detected (e.g., fire, fight, car crash), the backend sends a Telegram alert (with your live location if available). Alerts for the same event are rate-limited (default: 1 per minute).
- **Multi-label:** The system can detect and report multiple scenarios in a single frame (e.g., both "fire" and "car crash").

---

## Customization
- **Add/Remove Labels:** Edit `backend/settings.yaml` under `label-settings: labels:`
- **Adjust Threshold:** Change `prediction-threshold` in `settings.yaml` for sensitivity
- **Cooldown:** Change `COOLDOWN_SECONDS` in `backend.py` for alert frequency

---

## Example Usage
- Upload an image of a burning car: get labels like `fire`, `car crash`, and receive a Telegram alert with your location.
- Use the webcam: get live predictions and alerts only when a new event is detected.

---

## Requirements
- Python 3.9+
- Node.js 16+
- Telegram bot and chat ID for alerts

---

## License
MIT 
=======
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
>>>>>>> 6336fc7485a2ddba94207ee6fce08425b60191da
