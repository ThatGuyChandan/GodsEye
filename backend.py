from flask import Flask, request, jsonify
from flask_cors import CORS
from model import Model
import cv2
import numpy as np
from PIL import Image
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:8000", "http://172.20.10.2:5000", "http://<phone-ip>:8000"])

# Load environment variables
load_dotenv()

# Initialize model
model = Model()

def send_telegram_message(chat_id, message, bot_token):
    """
    Sends a message to a Telegram chat using the bot token.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Telegram API Error: {e}")
        return None

@app.route("/")
def index():
    return "Violence Detection Backend Running"

@app.route("/predict-image", methods=["POST"])
def predict_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image = Image.open(file.stream).convert("RGB")
    np_image = np.array(image)
    prediction = model.predict(image=np_image)

    # Extract prediction details
    label = prediction.get("label", "Unknown")
    confidence = prediction.get("confidence", 0)

    # Telegram Bot Configuration
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Send alert if specific labels are detected
    if label in ["violence", "fire", "accident"]:
        message = (
            f"ALERT: {label.upper()} detected with confidence {confidence:.2f}. Immediate action required."
        )
        send_telegram_message(chat_id, message, bot_token)

    return jsonify(prediction)

@app.route("/predict-video", methods=["POST"])
def predict_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    video_path = "./temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(file.read())

    cap = cv2.VideoCapture(video_path)
    label_counts = {}
    total_frames = 0
    detected_alerts = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1
        prediction = model.predict(image=frame)
        label = prediction.get("label", "Unknown")
        confidence = prediction.get("confidence", 0)

        # Track label counts
        label_counts[label] = label_counts.get(label, 0) + 1

        # Track specific alerts
        if label in ["violence", "fire", "accident"] and label not in detected_alerts:
            detected_alerts.add(label)

    cap.release()

    # Calculate percentages for each label
    summary = [
        {"label": label, "percentage": count / total_frames}
        for label, count in label_counts.items()
    ]

    # Telegram Bot Configuration
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Send a Telegram alert if specific labels were detected
    if detected_alerts:
        alerts = ", ".join(detected_alerts)
        summary_message = ", ".join(
            [f"{item['label']}: {item['percentage']:.2%}" for item in summary]
        )
        message = (
            f"ALERT: The video analysis detected the following: {alerts.upper()}.\n"
            f"Total Frames Analyzed: {total_frames}.\n"
            f"Summary: {summary_message}"
        )
        send_telegram_message(chat_id, message, bot_token)

    return jsonify({"summary": summary, "total_frames": total_frames})


@app.route("/predict-webcam", methods=["POST"])
def predict_webcam():
    data = request.data
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    nparr = np.frombuffer(data, np.uint8)
    
    if nparr.size == 0:
        return jsonify({"error": "Invalid image data received"}), 400
    
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return jsonify({"error": "Failed to decode image"}), 400
    
    try:
        prediction = model.predict(image=frame)
    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

    # Extract prediction details
    label = prediction.get("label", "Unknown")
    confidence = prediction.get("confidence", 0)

    # Telegram Bot Configuration
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Send alert if specific labels are detected
    if label in ["violence", "fire", "accident"]:
        message = (
            f"ALERT: {label.upper()} detected with confidence {confidence:.2f}. Immediate action required."
        )
        send_telegram_message(chat_id, message, bot_token)

    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
