let isTracking = false;
const videoElement = document.getElementById("camera-feed");

chrome.storage.local.get(['isTracking'], function(result) {
    if (result.isTracking !== undefined) {
        isTracking = result.isTracking;

        if (isTracking) {
            document.getElementById("status-text").textContent = "Rastreamento Ativo";
            document.getElementById("toggle-button").textContent = "Desativar Rastreamento";
        } else {
            document.getElementById("status-text").textContent = "Aguardando...";
            document.getElementById("toggle-button").textContent = "Ativar Rastreamento";
        }
    }
});

document.getElementById("toggle-button").addEventListener("click", function () {
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
            document.getElementById("status-text").textContent = "Rastreamento Ativo";
            this.textContent = "Desativar Rastreamento";
            startCamera();
        } else if (data.status.includes("parado")) {
            isTracking = false;
            document.getElementById("status-text").textContent = "Aguardando gesto...";
            this.textContent = "Ativar Rastreamento";
            stopCamera();
        } else {
            console.error(data.status);
        }

        chrome.storage.local.set({ isTracking });
    })
    .catch((error) => console.error("Erro ao controlar o servidor:", error));
});

// function startCamera() {
//     navigator.mediaDevices
//         .getUserMedia({ video: true })
//         .then((stream) => {
//             videoElement.srcObject = stream;
//         })
//         .catch((error) => {
//             console.error("Erro ao acessar câmera:", error);
//             if (error.name === 'NotFoundError') {
//                 alert("Nenhuma câmera foi encontrada. Verifique se a câmera está conectada.");
//             } else if (error.name === 'NotAllowedError') {
//                 alert("A permissão para acessar a câmera foi negada.");
//             } else {
//                 alert("Erro desconhecido ao acessar a câmera.");
//             }
//         });
// }

// function stopCamera() {
//     const stream = videoElement.srcObject;
//     if (stream) {
//         stream.getTracks().forEach((track) => track.stop());
//         videoElement.srcObject = null;
//     }
// }
