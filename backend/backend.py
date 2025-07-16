from flask import Flask, request, jsonify
from flask_cors import CORS
from model import Model
import cv2
import numpy as np
from PIL import Image
import requests
from dotenv import load_dotenv
import os
import time
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

app = Flask(__name__)
CORS(app, origins=["*"])

# Load environment variables
load_dotenv()

# Initialize model
model = Model(settings_path="./settings.yaml")

# Initialize S3 client and bucket after environment variables are loaded
s3 = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')

alert_cooldown = {}  # {label: last_alert_timestamp}
COOLDOWN_SECONDS = 60

def should_send_alert(label):
    now = time.time()
    last = alert_cooldown.get(label, 0)
    if now - last > COOLDOWN_SECONDS:
        alert_cooldown[label] = now
        return True
    return False

def send_telegram_message(chat_id, message, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Telegram API Error: {e}")
        return None

def send_telegram_location(chat_id, latitude, longitude, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendLocation"
    data = {"chat_id": chat_id, "latitude": latitude, "longitude": longitude}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Telegram API Error (location): {e}")
        return None

# Helper functions for S3

def upload_to_s3(file_stream, filename, content_type):
    s3.upload_fileobj(file_stream, S3_BUCKET, filename, ExtraArgs={'ContentType': content_type})
    return f"s3://{S3_BUCKET}/{filename}"

def download_from_s3(filename, local_path):
    s3.download_file(S3_BUCKET, filename, local_path)

def delete_from_s3(filename):
    s3.delete_object(Bucket=S3_BUCKET, Key=filename)

@app.route("/")
def index():
    return "Violence Detection Backend Running"

@app.route("/predict-image", methods=["POST"])
def predict_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    filename = f"temp/{uuid.uuid4()}_{file.filename}"
    upload_to_s3(file.stream, filename, file.content_type)
    # Download for analysis
    local_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
    download_from_s3(filename, local_path)
    image = Image.open(local_path).convert("RGB")
    np_image = np.array(image)
    prediction = model.predict(image=np_image)
    os.remove(local_path)
    delete_from_s3(filename)
    labels = prediction.get("labels", [])
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    safe_labels = [
        "Unknown", "people walking", "buildings", "road", "cars on a road", "car parking area", "cars", "office environment", "people talking", "group of people"
    ]
    for label_info in labels:
        label = label_info["label"]
        confidence = label_info["confidence"]
        if label not in safe_labels and bot_token and chat_id and should_send_alert(label):
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
    filename = f"temp/{uuid.uuid4()}_{file.filename}"
    upload_to_s3(file.stream, filename, file.content_type)
    local_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
    download_from_s3(filename, local_path)
    cap = cv2.VideoCapture(local_path)
    label_counts = {}
    total_frames = 0
    detected_alerts = set()
    safe_labels = [
        "Unknown", "people walking", "buildings", "road", "cars on a road", "car parking area", "cars", "office environment", "people talking", "group of people"
    ]
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        prediction = model.predict(image=frame)
        labels = prediction.get("labels", [])
        for label_info in labels:
            label = label_info["label"]
            confidence = label_info["confidence"]
            label_counts[label] = label_counts.get(label, 0) + 1
            if label not in safe_labels and label not in detected_alerts:
                detected_alerts.add(label)
    cap.release()
    os.remove(local_path)
    delete_from_s3(filename)
    summary = [
        {"label": label, "percentage": count / total_frames}
        for label, count in label_counts.items()
    ]
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if detected_alerts and bot_token and chat_id:
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
    # Accept both raw and multipart
    if request.content_type and request.content_type.startswith('multipart'):
        file = request.files.get('frame')
        if not file:
            return jsonify({"error": "No frame uploaded"}), 400
        filename = f"temp/{uuid.uuid4()}_{file.filename}"
        upload_to_s3(file.stream, filename, file.content_type)
        local_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
        download_from_s3(filename, local_path)
        image = Image.open(local_path).convert("RGB")
        np_image = np.array(image)
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        os.remove(local_path)
        delete_from_s3(filename)
    else:
        data = request.data
        if not data:
            return jsonify({"error": "No data received"}), 400
        nparr = np.frombuffer(data, np.uint8)
        if nparr.size == 0:
            return jsonify({"error": "Invalid image data received"}), 400
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Failed to decode image"}), 400
        np_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        latitude = None
        longitude = None
    try:
        prediction = model.predict(image=np_image)
    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500
    labels = prediction.get("labels", [])
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    safe_labels = [
        "Unknown", "people walking", "buildings", "road", "cars on a road", "car parking area", "cars", "office environment", "people talking", "group of people"
    ]
    for label_info in labels:
        label = label_info["label"]
        confidence = label_info["confidence"]
        if label not in safe_labels and bot_token and chat_id and should_send_alert(label):
            message = (
                f"ALERT: {label.upper()} detected with confidence {confidence:.2f}. Immediate action required."
            )
            send_telegram_message(chat_id, message, bot_token)
            if latitude and longitude:
                try:
                    lat = float(latitude)
                    lon = float(longitude)
                    send_telegram_location(chat_id, lat, lon, bot_token)
                except Exception as e:
                    print(f"Location error: {e}")
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 