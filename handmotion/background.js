const serverUrl = "http://localhost:5000";
let isTrackingActive = false;

// Gerenciar a conexão com o servidor Python
async function toggleTracking(activate) {
  if (activate) {
    try {
      const response = await fetch(`${serverUrl}/status`);
      if (!response.ok) throw new Error("Servidor Python não está ativo");
      console.log("Rastreamento ativado e servidor Python conectado.");
      isTrackingActive = true;
    } catch (error) {
      console.error("Erro ao conectar ao servidor Python:", error);
      isTrackingActive = false;
    }
  } else {
    console.log("Rastreamento desativado.");
    isTrackingActive = false;
  }
}

// Lida com mensagens do popup para iniciar o tracking
chrome.runtime.onMessage.addListener((message, sendResponse) => {
  if (message.type === "start_tracking") {
    toggleTracking(true);
    sendResponse({ status: "Tracking iniciado" });
  } else if (message.type === "stop_tracking") {
    toggleTracking(false);
    sendResponse({ status: "Tracking parado" });
  }
});

// Conexão com o servidor para rastreamento de gestos
setInterval(() => {
  if (isTrackingActive) {
    fetch(`${serverUrl}/gesture`)
      .then((response) => response.json())
      .then((data) => {
        const gesture = data.gesture;
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs[0]) {
            chrome.scripting.executeScript({
              target: { tabId: tabs[0].id },
              func: (gesture) => {
                console.log(`Gesto detectado: ${gesture}`);
              },
              args: [gesture],
            });
          }
        });
      })
      .catch((error) => console.error("Erro ao obter gesto do servidor:", error));
  }
}, 0.5);
