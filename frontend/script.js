const backendUrl = "http://localhost:5000";

// Dark Mode Toggle
document
  .getElementById("darkModeToggle")
  .addEventListener("change", function () {
    document.body.classList.toggle("dark-mode", this.checked);
  });

// Image/Video Upload
document.getElementById("uploadButton").addEventListener("click", async () => {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const endpoint = file.type.startsWith("video/")
    ? "/predict-video"
    : "/predict-image";

  // Show loading indicator
  document.getElementById("loading").classList.remove("hidden");

  try {
    const response = await fetch(`${backendUrl}${endpoint}`, {
      method: "POST",
      body: formData,
    });
    const result = await response.json();

    if (endpoint === "/predict-video") {
      // Handle video-specific response
      const summary = result.summary || [];
      if (summary.length > 0) {
        const predictionsText = summary
          .map(
            (entry) => `${entry.label}: ${(entry.percentage * 100).toFixed(2)}%`
          )
          .join("\n");
        document.getElementById("prediction").innerText = predictionsText;
      } else {
        document.getElementById("prediction").innerText =
          "No significant predictions detected.";
      }
    } else {
      // Handle image-specific response
      const predictionText = `Prediction: ${result.label || "Unknown"}`;
      document.getElementById("prediction").innerText = predictionText;
    }
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("prediction").innerText =
      "An error occurred during prediction.";
  } finally {
    // Hide loading indicator
    document.getElementById("loading").classList.add("hidden");
  }
});

// Webcam Live Predictions
let webcamStream = null;
let webcamInterval = null;

document.getElementById("startWebcam").addEventListener("click", async () => {
  const video = document.getElementById("webcam");
  const stopButton = document.getElementById("stopWebcam");
  const startButton = document.getElementById("startWebcam");

  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = webcamStream;

    // Show the Stop button and hide the Start button
    startButton.classList.add("hidden");
    stopButton.classList.remove("hidden");

    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    // Start sending frames for predictions
    webcamInterval = setInterval(async () => {
      if (!webcamStream) return;

      // Set canvas size based on video dimensions
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Get the raw image data from canvas (in JPEG format)
      canvas.toBlob(async (blob) => {
        try {
          const response = await fetch(`${backendUrl}/predict-webcam`, {
            method: "POST",
            body: blob,
            headers: {
              "Content-Type": "application/octet-stream",
            },
          });

          if (!response.ok) {
            throw new Error("Failed to fetch prediction");
          }

          const result = await response.json();
          const predictionText = `Prediction: ${result.label || "Unknown"}`;
          document.getElementById("webcamPrediction").innerText =
            predictionText;
        } catch (error) {
          console.error("Error:", error);
        }
      }, "image/jpeg");
    }, 1000); // Send frames every second
  } catch (error) {
    console.error("Error accessing webcam:", error);
    alert("Could not access the webcam. Please check permissions.");
  }
});

document.getElementById("stopWebcam").addEventListener("click", () => {
  const video = document.getElementById("webcam");
  const stopButton = document.getElementById("stopWebcam");
  const startButton = document.getElementById("startWebcam");

  if (webcamStream) {
    webcamStream.getTracks().forEach((track) => track.stop()); // Stop all webcam tracks
    webcamStream = null;
  }

  if (webcamInterval) {
    clearInterval(webcamInterval); // Stop predictions interval
    webcamInterval = null;
  }

  // Clear webcam video and prediction display
  video.srcObject = null;
  document.getElementById("webcamPrediction").innerText = "Webcam stopped.";

  // Hide the Stop button and show the Start button
  stopButton.classList.add("hidden");
  startButton.classList.remove("hidden");
});
