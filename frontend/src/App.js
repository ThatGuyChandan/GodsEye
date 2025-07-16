import React, { useRef, useState } from 'react';
import './App.css';

const BACKEND_URL = 'http://localhost:5000';

function App() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);
  const [webcamActive, setWebcamActive] = useState(false);
  const [webcamPrediction, setWebcamPrediction] = useState('');
  const [location, setLocation] = useState({ latitude: null, longitude: null });
  const videoRef = useRef(null);
  const webcamStreamRef = useRef(null);
  const webcamIntervalRef = useRef(null);

  // Get location on mount
  React.useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        (error) => {
          setLocation({ latitude: null, longitude: null });
        }
      );
    }
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPrediction('');
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setPrediction('');
    const formData = new FormData();
    formData.append('file', file);
    const endpoint = file.type.startsWith('video/') ? '/predict-video' : '/predict-image';
    try {
      const res = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: 'POST',
        body: formData,
      });
      const result = await res.json();
      if (endpoint === '/predict-video') {
        const summary = result.summary || [];
        if (summary.length > 0) {
          setPrediction(
            summary
              .map((entry) => `${entry.label}: ${(entry.percentage * 100).toFixed(2)}%`)
              .join('\n')
          );
        } else {
          setPrediction('No significant predictions detected.');
        }
      } else if (result.labels && Array.isArray(result.labels)) {
        if (result.labels.length > 0) {
          setPrediction(
            result.labels
              .sort((a, b) => b.confidence - a.confidence)
              .map((l) => `${l.label} (Confidence: ${l.confidence.toFixed(2)})`)
              .join('\n')
          );
        } else {
          setPrediction('Prediction: Unknown');
        }
      } else {
        setPrediction(`Prediction: ${result.label || 'Unknown'} (Confidence: ${result.confidence?.toFixed(2)})`);
      }
    } catch (err) {
      setPrediction('Error during prediction.');
    }
    setLoading(false);
  };

  const startWebcam = async () => {
    const video = videoRef.current;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      webcamStreamRef.current = stream;
      video.srcObject = stream;
      setWebcamActive(true);
      video.onloadedmetadata = () => {
        video.play();
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        webcamIntervalRef.current = setInterval(() => {
          if (!webcamStreamRef.current) return;
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
          canvas.toBlob(async (blob) => {
            if (!blob) return;
            try {
              const formData = new FormData();
              formData.append('frame', blob, 'frame.jpg');
              if (location.latitude && location.longitude) {
                formData.append('latitude', location.latitude);
                formData.append('longitude', location.longitude);
              }
              const response = await fetch(`${BACKEND_URL}/predict-webcam`, {
                method: 'POST',
                body: formData,
              });
              const result = await response.json();
              if (result.labels && Array.isArray(result.labels)) {
                if (result.labels.length > 0) {
                  setWebcamPrediction(
                    result.labels
                      .sort((a, b) => b.confidence - a.confidence)
                      .map((l) => `${l.label} (Confidence: ${l.confidence.toFixed(2)})`)
                      .join('\n')
                  );
                } else {
                  setWebcamPrediction('Prediction: Unknown');
                }
              } else {
                setWebcamPrediction(`Prediction: ${result.label || 'Unknown'} (Confidence: ${result.confidence?.toFixed(2)})`);
              }
            } catch (error) {
              setWebcamPrediction('Error during prediction.');
            }
          }, 'image/jpeg');
        }, 1000);
      };
    } catch (error) {
      setWebcamPrediction('Could not access the webcam. Please check permissions.');
    }
  };

  const stopWebcam = () => {
    setWebcamActive(false);
    setWebcamPrediction('Webcam stopped.');
    if (webcamStreamRef.current) {
      webcamStreamRef.current.getTracks().forEach((track) => track.stop());
      webcamStreamRef.current = null;
    }
    if (webcamIntervalRef.current) {
      clearInterval(webcamIntervalRef.current);
      webcamIntervalRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  return (
    <div className="App">
      <h1>Violence Detection</h1>
      <div className="upload-section">
        <h2>Upload Image or Video</h2>
        <input type="file" accept="image/*,video/*" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? 'Processing...' : 'Upload'}
        </button>
        <pre className="prediction">{prediction}</pre>
      </div>
      <hr />
      <div className="webcam-section">
        <h2>Live Webcam Predictions</h2>
        <video ref={videoRef} width={320} height={240} autoPlay muted style={{ display: webcamActive ? 'block' : 'none' }} />
        <div>
          {!webcamActive ? (
            <button onClick={startWebcam}>Start Webcam</button>
          ) : (
            <button onClick={stopWebcam}>Stop Webcam</button>
          )}
        </div>
        <pre className="prediction">{webcamPrediction}</pre>
      </div>
    </div>
  );
}

export default App;
