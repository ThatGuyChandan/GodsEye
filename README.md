# Violence Detection System

## Overview
This project is a full-stack violence and anomaly detection system using deep learning (CLIP) for image/video/webcam analysis. It features:
- **Backend:** Python Flask API for predictions and Telegram alerts (with live location)
- **Frontend:** React app for uploading images/videos and live webcam predictions
- **Alerting:** Sends Telegram alerts (with live location) for dangerous scenarios
- **Modern UI/UX:** Tabbed interface for easy switching between Upload and Live Webcam screens

---

## Features
- Detects violence, fire, car crash, street violence, and more in images, videos, and live webcam
- Multi-label output: returns all relevant scenarios above a confidence threshold
- Sends Telegram alerts (with live location) for dangerous events
- Cooldown logic to avoid alert spamming
- Modern React frontend with tabbed navigation and beautiful design

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
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=your_region
S3_BUCKET_NAME=your_bucket_name
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
- **Tabbed UI:** Easily switch between "Upload" (for image/video) and "Live Webcam" screens using the modern tab switcher at the top.
- **Image/Video Upload:** Upload an image or video for violence/anomaly detection. The backend returns all detected scenarios above the confidence threshold.
- **Live Webcam:** Start the webcam for real-time predictions. The frontend sends frames (and your live location) to the backend every second.
- **Telegram Alerts:** If a dangerous scenario is detected (e.g., fire, fight, car crash), the backend sends a Telegram alert (with your live location if available). Alerts for the same event are rate-limited (default: 1 per minute).
- **Multi-label:** The system can detect and report multiple scenarios in a single frame (e.g., both "fire" and "car crash").
- **Cloud Storage:** All uploads are stored temporarily in AWS S3 for analysis and deleted after use.

---

## Customization
- **Add/Remove Labels:** Edit `backend/settings.yaml` under `label-settings: labels:`
- **Adjust Threshold:** Change `prediction-threshold` in `settings.yaml` for sensitivity
- **Cooldown:** Change `COOLDOWN_SECONDS` in `backend.py` for alert frequency
- **UI/UX:** The frontend is built with React and can be easily customized for branding, dark mode, etc.

---

## Example Usage
- Upload an image of a burning car: get labels like `fire`, `car crash`, and receive a Telegram alert with your location.
- Use the webcam: get live predictions and alerts only when a new event is detected.
- Switch between Upload and Live Webcam screens with a single click.

---

## Requirements
- Python 3.9+
- Node.js 16+
- Telegram bot and chat ID for alerts
- AWS S3 bucket and credentials

---

## License
MIT 
