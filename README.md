Godseye: Real-Time Violence/Fire/Crash Detection System 🚨🔥🚗
Godseye is an AI-powered system for real-time detection of critical events such as violence, fire, and car crashes. Built on the CLIP model, the system processes live webcam feeds, uploaded images, and videos to identify potentially dangerous situations and sends instant alerts via Telegram.

📌 Features
Live Webcam Detection: Analyze live video feeds for detecting critical events.
Image/Video Upload: Upload photos or videos to detect incidents with high accuracy.
AI-Powered Detection: Utilizes the CLIP model for advanced visual understanding.
Telegram Alerts: Instantly notify users with detailed alerts about detected incidents.
Scalable API: Backend API designed for seamless integration with other systems.
🛠️ Technology Stack
Python: Core programming language.
Flask: Backend framework for RESTful APIs.
CLIP Model: Cutting-edge AI model for visual and textual recognition.
OpenCV & Pillow: For video/image preprocessing and handling.
Telegram Bot API: For alert notifications.
YAML: Configuration management with settings.yaml.
🚀 How It Works
Webcam Detection:

Captures frames from the webcam and analyzes them in real-time.
Detects critical events and sends Telegram alerts.
Image/Video Upload:

Accepts images or videos for batch processing.
Uses the CLIP model to predict events and generate summaries.
Notification System:

Sends Telegram alerts for detected incidents, including event type and confidence score.
📂 Folder Structure
bash
Copy code
GODSEYE/
├── frontend/               # Placeholder for future frontend integration
├── .env                    # Environment variables for sensitive data
├── .gitignore              # Files and directories to exclude from version control
├── app.py                  # Entry point for the backend application
├── backend.py              # Core backend logic
├── model.py                # CLIP model integration and predictions
├── utils.py                # Utility functions for various tasks
├── settings.yaml           # Configuration settings
├── requirements.txt        # Python dependencies
└── README.md               # Project description
🔧 Setup Instructions
Clone the repository:
bash
Copy code
git clone [https://github.com/ThatGuy/godseye.git](https://github.com/ThatGuyChandan/GodsEye.git)
Navigate to the project directory:
bash
Copy code
cd godseye
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Add the necessary environment variables in the .env file:
makefile
Copy code
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
Update settings.yaml with relevant configurations.
Run the application:
bash
Copy code
python app.py
Access the application at http://127.0.0.1:5000.
🧪 Key API Endpoints
GET /: Check if the backend is running.
POST /predict-image: Upload an image for event detection.
POST /predict-video: Upload a video for event detection.
POST /predict-webcam: Analyze live webcam feed.
🌟 Future Enhancements
Add a user-friendly frontend for better interaction.
Support mobile push notifications in addition to Telegram.
Integrate location tracking for geospatial incident reporting.
Deploy on cloud platforms for scalability.
