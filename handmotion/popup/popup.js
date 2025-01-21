let isTracking = false;
const statusElement = document.getElementById("status-text");
const toggleButton = document.getElementById("toggle-button");
const gestureElement = document.getElementById("gesture-text"); 

chrome.storage.local.get(['isTracking'], function(result) {
    if (result.isTracking !== undefined) {
        isTracking = result.isTracking;

        if (isTracking) {
            statusElement.textContent = "Rastreamento Ativo";
            toggleButton.textContent = "Desativar Rastreamento";
        } else {
            statusElement.textContent = "Aguardando...";
            toggleButton.textContent = "Ativar Rastreamento";
        }
    }

    if (isTracking) {
        setInterval(fetchGesture, 1000);
    }
});

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
            statusElement.textContent = "Rastreamento Ativo";
            this.textContent = "Desativar Rastreamento";
            statusElement.style.color = "#28a745";
        } else if (data.status.includes("parado")) {
            isTracking = false;
            statusElement.textContent = "Rastreamento Desativado...";
            statusElement.style.color = "#ff5722";
            this.textContent = "Ativar Rastreamento";
        } else {
            console.error(data.status);
        }

        chrome.storage.local.set({ isTracking });
    })
    .catch((error) => console.error("Erro ao controlar o servidor:", error));
});

function fetchGesture() {
    fetch("http://localhost:5000/status")
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "Servidor ativo") {
                gestureElement.textContent = `Gesto atual: ${data.gesture || "Nenhum"}`;
            } else {
                gestureElement.textContent = "Erro ao obter o gesto.";
            }
        })
        .catch((error) => {
            console.error("Erro ao buscar o gesto:", error);
            gestureElement.textContent = "Erro de conexão.";
        });
}