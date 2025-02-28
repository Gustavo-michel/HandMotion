let isTracking = false;
const statusElement = document.getElementById("status-text");
const toggleButton = document.getElementById("toggle-button");
const gestureElement = document.getElementById("gesture-text"); 
const video = document.createElement("video");
video.setAttribute("autoplay", "");
video.setAttribute("playsinline", "");
document.body.appendChild(video);

const socket = io("http://localhost:5000"); 

socket.on('connect', () => {
    console.log("Socket.IO conectado.");
});

socket.on('disconnect', () => {
    console.log("Socket.IO desconectado.");
});

socket.on('error', (error) => {
    console.error("Erro no Socket.IO:", error);
});

// maintain state
chrome.storage.local.get(['isTracking'], function(result) {
    if (result.isTracking !== undefined) {
        isTracking = result.isTracking;
        updateUI();
    }

    if (isTracking) {
        setInterval(fetchGesture, 1000);
    }
});

function updateUI() {
    statusElement.textContent = isTracking ? "Online Tracking" : "Offline Tracking";
    toggleButton.textContent = isTracking ? "Disable Tracking" : "Enable Tracking";
    statusElement.style.color = isTracking ? "#28a745" : "#7D2C2F";
}

// Control tracker enabled
toggleButton.addEventListener("click", function () {
    isTracking = !isTracking;
    const action = isTracking ? "start" : "stop";

    fetch("http://localhost:5000/control", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ action }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(`Ação ${action} enviada: ${data.status}`);

        chrome.storage.local.set({ isTracking });
        updateUI();


        setInterval(fetchGesture, 1000);
    })
    .catch((error) => console.error("Erro ao controlar o servidor:", error));
});


// Get gesture status
function fetchGesture() {
    fetch("http://localhost:5000/status")
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "Active server") {
                gestureElement.textContent = `${data.gesture || "None"}`;
            } else {
                gestureElement.textContent = "Error getting gesture.";
            }
        })
        .catch((error) => {
            console.error("Error when searching for gesture:", error);
            gestureElement.textContent = "Connection error.";
        });
}

// Get streaming video
navigator.mediaDevices.getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
    startStreaming();
  })
  .catch((err) => console.error("Erro ao acessar a câmera:", err));

function sendToServer(imageData) {
    socket.emit("video", { image: imageData });
}

function startStreaming() {
    const displayCanvas = document.createElement("canvas");
    const displayCtx = displayCanvas.getContext("2d");

    const sendCanvas = document.createElement("canvas");
    const sendCtx = sendCanvas.getContext("2d");

    document.body.appendChild(displayCanvas);

    video.style.display = "none";

    setInterval(() => {
        displayCanvas.width = sendCanvas.width = video.videoWidth;
        displayCanvas.height = sendCanvas.height = video.videoHeight;

        displayCtx.save();
        displayCtx.scale(-1, 1);
        displayCtx.drawImage(video, -displayCanvas.width, 0, displayCanvas.width, displayCanvas.height);
        displayCtx.restore();

        sendCtx.drawImage(video, 0, 0, sendCanvas.width, sendCanvas.height);
        const imageData = sendCanvas.toDataURL("image/jpeg");
        
        if(isTracking){
            sendToServer(imageData);
        }
    }, 100);
}
