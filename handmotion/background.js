const serverUrl = "http://localhost:5000";
let isTrackingActive = false;
let videoStream = null;

// Função para gerenciar a conexão com o servidor Python
async function toggleTracking(activate) {
  if (activate) {
    try {
      const response = await fetch(`${serverUrl}/status`);
      if (!response.ok) throw new Error("Servidor Python não está ativo");
      console.log("Rastreamento ativado e servidor Python conectado.");
      startVideoStream();
      isTrackingActive = true;
    } catch (error) {
      console.error("Erro ao conectar ao servidor Python:", error);
      isTrackingActive = false;
    }
  } else {
    stopVideoStream();
    console.log("Rastreamento desativado.");
    isTrackingActive = false;
  }
}

// Função para iniciar o stream de vídeo
function startVideoStream() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      videoStream = stream;
      const videoTrack = stream.getVideoTracks()[0];
      const imageCapture = new ImageCapture(videoTrack);

      // Enviar quadros de vídeo para as páginas
      const captureFrame = () => {
        if (isTrackingActive) {
          imageCapture.grabFrame().then((imageBitmap) => {
            const canvas = new OffscreenCanvas(imageBitmap.width, imageBitmap.height);
            const ctx = canvas.getContext("2d");
            ctx.drawImage(imageBitmap, 0, 0);
            const frame = canvas.toDataURL("image/png");

            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
              if (tabs[0]) {
                chrome.scripting.executeScript({
                  target: { tabId: tabs[0].id },
                  func: (frame, gesture) => {
                    const videoContainer = document.getElementById("video-container");
                    if (!videoContainer) {
                      const newDiv = document.createElement("div");
                      newDiv.id = "video-container";
                      newDiv.style = "position: fixed; bottom: 10px; right: 10px; width: 300px; height: auto; background-color: black;";
                      const img = document.createElement("img");
                      img.src = frame;
                      img.style = "width: 100%; height: auto;";
                      newDiv.appendChild(img);
                      document.body.appendChild(newDiv);
                    } else {
                      videoContainer.querySelector("img").src = frame;
                    }

                    console.log(`Gesto detectado: ${gesture}`);
                  },
                  args: [frame, "Nenhum gesto detectado ainda"],
                });
              }
            });
          });
          setTimeout(captureFrame, 100); // Captura a cada 100 ms
        }
      };

      captureFrame();
    })
    .catch((error) => console.error("Erro ao acessar a câmera:", error));
}

// Função para parar o stream de vídeo
function stopVideoStream() {
  if (videoStream) {
    videoStream.getTracks().forEach((track) => track.stop());
    videoStream = null;
  }
}

// Lida com a mensagem do popup para inciar o tracking
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
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
                alert(`Gesto detectado: ${gesture}`);
              },
              args: [gesture],
            });
          }
        });
      })
      .catch((error) => console.error("Erro ao obter gesto do servidor:", error));
  }
}, 1000);
