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
        statusElement.style.color = "#ff5722";
    }
}

toggleButton.addEventListener("click", function () {
    const action = isTracking ? "stop" : "start";
    
    fetch("http://localhost:5000/control", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ action }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data.status);

        if (data.status.includes("iniciado")) {
            isTracking = true;
        } else if (data.status.includes("parado")) {
            isTracking = false;
        } else {
            console.error(data.status);
        }

        chrome.storage.local.set({ isTracking });
        updateUI();

        if (isTracking) {
            setInterval(fetchGesture, 1000);
        }
    })
    .catch((error) => console.error("Erro ao controlar o servidor:", error));
});

function fetchGesture() {
    fetch("http://localhost:5000/status")
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "Servidor ativo") {
                gestureElement.textContent = `${data.gesture || "None"}`;
            } else {
                gestureElement.textContent = "Erro ao obter o gesto.";
            }
        })
        .catch((error) => {
            console.error("Erro ao buscar o gesto:", error);
            gestureElement.textContent = "Erro de conexão.";
        });
}
