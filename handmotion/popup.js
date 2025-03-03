let isTracking = false;
const statusElement = document.getElementById("status-text");
const toggleButton = document.getElementById("toggle-button");
const gestureElement = document.getElementById("gesture-text");

// keeps the last state of the popup 
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


        setInterval(fetchGesture, 1000);
    })
    .catch((error) => console.error("Erro ao controlar o servidor:", error));
});


// check server status and gestures
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

