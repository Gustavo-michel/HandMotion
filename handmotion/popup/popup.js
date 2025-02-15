let isTracking = false;
const statusElement = document.getElementById("status-text");
const toggleButton = document.getElementById("toggle-button");
const shutdownButton = document.getElementById("shutdown-button");
const gestureElement = document.getElementById("gesture-text");
const cameraFeed = document.getElementById("camera-feed");
let nativePort = null;

function connectNative() {
    if (!nativePort) {
        nativePort = chrome.runtime.connectNative("com.handmotion.native");
        nativePort.onMessage.addListener((message) => {
            if (message.frame) {
                cameraFeed.src = `data:image/jpeg;base64,${message.frame}`;
            }
            if (message.gesture) {
                gestureElement.textContent = message.gesture;
            }
        });
        nativePort.onDisconnect.addListener(() => {
            console.error("Desconectado");
            nativePort = null;
            isTracking = false;
            updateUI();
            chrome.storage.local.set({ isTracking });
        });
    }
}

function disconnectNative() {
    if (nativePort) {
        nativePort.disconnect();
        nativePort = null;
    }
}


function updateUI() {
    statusElement.textContent = isTracking ? "Online Tracking" : "Offline Tracking";
    toggleButton.textContent = isTracking ? "Disable Tracking" : "Enable Tracking";
    statusElement.style.color = isTracking ? "#28a745" : "#7D2C2F";
}

chrome.storage.local.get(['isTracking'], (result) => {
    isTracking = result.isTracking ?? false;
    updateUI();
});

toggleButton.addEventListener("click", () => {
    isTracking = !isTracking;

    if (!nativePort) {
        connectNative();
    }

    if (isTracking) {
        nativePort.postMessage({ action: "start" });
    } else {
        nativePort.postMessage({ action: "stop" });
        disconnectNative();
    }

    chrome.storage.local.set({ isTracking });
    updateUI();
});

