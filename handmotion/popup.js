let isTracking = false;
let gestureInterval = null;
let mediaStream = null;

const statusElement = document.getElementById("status-text");
const toggleButton = document.getElementById("toggle-button");
const gestureElement = document.getElementById("gesture-text");
const video = document.getElementById('camera-feed');


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

function updateUI() {
    statusElement.textContent = isTracking ? "Online Tracking" : "Offline Tracking";
    toggleButton.textContent = isTracking ? "Disable Tracking" : "Enable Tracking";
    statusElement.style.color = isTracking ? "#28a745" : "#7D2C2F";
}

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
        console.log(`Ação ${action} enviada: ${data.status}`);

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
    .catch((error) => console.error("Erro ao controlar o servidor:", error));
});


// check server status and gestures
function fetchGesture() {
    fetch("http://localhost:5000/status")
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "Active server") {
                gestureElement.textContent = `${data.gesture || "Nenhum"}`;
            } else {
                gestureElement.textContent = "Erro ao obter gesto.";
            }
        })
        .catch((error) => {
            console.error("Erro com o servidor:", error);
            gestureElement.textContent = "Erro de conexão.";

            if (isTracking) {
                isTracking = false;
                chrome.storage.local.set({ isTracking });
                updateUI();
                stopGestureFetching();
            }
        });
}