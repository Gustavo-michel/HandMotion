let isTracking = false;
const statusElement = document.getElementById("status-text");
const toggleButton = document.getElementById("toggle-button");
const gestureElement = document.getElementById("gesture-text");

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
    if (isTracking) {
        statusElement.textContent = "Online tracking";
        toggleButton.textContent = "Disable Tracking";
        statusElement.style.color = "#28a745";
    } else {
        statusElement.textContent = "Offline Tracking";
        toggleButton.textContent = "Enable tracking";
        statusElement.style.color = "#7D2C2F";
    }
}

toggleButton.addEventListener("click", function () {
    const action = isTracking ? "stop" : "start";
    
    chrome.runtime.sendNativeMessage("com.my_company.my_application", { action }, function(response) {
        if (chrome.runtime.lastError) {
            console.error("Erro na comunicação nativa:", chrome.runtime.lastError.message);
            return;
        }
        
        console.log(response.status);
        
        if (response.status && response.status.includes("Started")) {
            isTracking = true;
        } else if (response.status && response.status.includes("Stopped")) {
            isTracking = false;
        } else {
            console.error("Status inesperado:", response.status);
        }
        
        chrome.storage.local.set({ isTracking });
        updateUI();
        
        if (isTracking) {
            setInterval(fetchGesture, 1000);
        }
    });
});

function fetchGesture() {
    chrome.runtime.sendNativeMessage("com.my_company.my_application", { action: "status" }, function(response) {
        if (chrome.runtime.lastError) {
            console.error("Erro na comunicação nativa:", chrome.runtime.lastError.message);
            gestureElement.textContent = "Connection error.";
            return;
        }
        
        if (response.status === "Active server") {
            gestureElement.textContent = response.gesture || "None";
        } else {
            gestureElement.textContent = "Error getting gesture.";
        }
    });
}
