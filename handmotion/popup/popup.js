        let isTracking = false;
        
        // Mudança do status ao clicar no botão
        document.getElementById("toggle-button").addEventListener("click", function() {
            isTracking = !isTracking;
            if (isTracking) {
                document.getElementById("status-text").textContent = "Rastreamento Ativo";
                this.textContent = "Desativar Rastreamento";
                // Enviar uma mensagem para ativar o rastreamento (background.js ou outras interações)
                chrome.runtime.sendMessage({ type: "start_tracking" });
            } else {
                document.getElementById("status-text").textContent = "Aguardando gesto...";
                this.textContent = "Ativar Rastreamento";
                // Enviar mensagem para desativar o rastreamento
                chrome.runtime.sendMessage({ type: "stop_tracking" });
            }
        });

        // Ouvir mensagens do background.js e mostrar gestos detectados
        chrome.runtime.onMessage.addListener(function(message) {
            if (message.type === "gesture_detected") {
                alert(`Gesto detectado: ${message.gesture}`);
            }
        });