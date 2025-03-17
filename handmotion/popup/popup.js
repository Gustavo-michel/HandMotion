let isTracking = false;
let gestureInterval = null;
let mediaStream = null;

const statusElement = document.getElementById("status-text");
const toggleButton = document.getElementById("toggle-button");
const gestureElement = document.getElementById("gesture-text");
const socket = io("http://localhost:5000");

socket.on("processed_frame", data => {
    document.getElementById("camera-feed").src = `data:image/jpeg;base64,${data.frame}`;
});

function startGestureFetching() {
    if (gestureInterval) {
        clearInterval(gestureInterval);
    }
    gestureInterval = setInterval(fetchGesture, 1000);
}

function stopGestureFetching() {
    if (gestureInterval) {
        clearInterval(gestureInterval);
        gestureInterval = null;
    }
}

function updateUI() {
    statusElement.textContent = isTracking ? "Online Tracking" : "Offline Tracking";
    toggleButton.textContent = isTracking ? "Disable Tracking" : "Enable Tracking";
    statusElement.style.color = isTracking ? "#28a745" : "#7D2C2F";
}

// Controls tracking activation
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
        console.log(`Action ${action} sending: ${data.status}`);

        chrome.storage.local.set({ isTracking });
        updateUI();

        if (isTracking) {
            chrome.runtime.sendMessage({ action: "start" });
            startGestureFetching();
        } else {
            chrome.runtime.sendMessage({ action: "stop" });
            stopGestureFetching();
        }
    })
    .catch((error) => console.error("Error to control server:", error));
});


// check server status and gestures
function fetchGesture() {
    fetch("http://localhost:5000/status")   
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "Active server") {
                gestureElement.textContent = `${data.gesture || "None"}`;
            } else {
                gestureElement.textContent = "Error to get gestures.";
            }
        })
        .catch((error) => {
            console.error("error with the server:", error);
            gestureElement.textContent = "Connection error.";

            if (isTracking) {
                isTracking = false;
                chrome.storage.local.set({ isTracking });
                updateUI();
                stopGestureFetching();
                chrome.runtime.sendMessage({ action: "stop" });
            }
        });
}

// keeps the last state of the popup
chrome.storage.local.get(['isTracking'], function(result) {
    if (result.isTracking !== undefined) {
        isTracking = result.isTracking;
        updateUI();
    }

    if (isTracking) {
        startGestureFetching();
    }
});