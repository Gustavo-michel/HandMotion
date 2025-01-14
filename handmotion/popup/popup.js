        let isTracking = false;

        
        document.getElementById("toggle-button").addEventListener("click", function() {
            isTracking = !isTracking;
            if (isTracking) {
                document.getElementById("status-text").textContent = "Rastreamento Ativo";
                this.textContent = "Desativar Rastreamento";
                chrome.runtime.sendMessage({ type: "start_tracking" });
            } else {
                document.getElementById("status-text").textContent = "Aguardando gesto...";
                this.textContent = "Ativar Rastreamento";
                chrome.runtime.sendMessage({ type: "stop_tracking" });
            }
        });

        chrome.runtime.onMessage.addListener(function(message) {
            if (message.type === "gesture_detected") {
                alert(`Gesto detectado: ${message.gesture}`);
                document.getElementById("gesture-text").textContent = message.gesture;
            }
        });