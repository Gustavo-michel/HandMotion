document.addEventListener("DOMContentLoaded", function() {
    let video = document.getElementById('video');
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');
    let isCapturing = false;

    function startCapture() {
        if (isCapturing) return;
        isCapturing = true;

        navigator.mediaDevices.getUserMedia({ video: true })
          .then((stream) => {
              video.srcObject = stream;
              video.play();

              setInterval(() => {
                  if (!isCapturing) return;
                  canvas.width = video.videoWidth;
                  canvas.height = video.videoHeight;
                  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                  canvas.toBlob((blob) => {
                      let formData = new FormData();
                      formData.append("frame", blob, "frame.jpg");

                      fetch("http://localhost:5000/upload", {
                          method: "POST",
                          body: formData
                      })
                      .then(response => response.text())
                      .then(data => console.log("Frame sent:", data))
                      .catch(error => console.error("Error sending frame:", error));
                  }, "image/jpeg", 0.8);
              }, 100);
          })
          .catch(error => {
              console.error("Error accessing webcam:", error);
          });
    }

    function stopCapture() {
        isCapturing = false;
        video.srcObject?.getTracks().forEach(track => track.stop());
        console.log("Captura de vídeo parada.");
    }

    // 🚀 Listener para receber mensagens do Background Script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === "startCapture") {
            console.log("Recebido startCapture no Offscreen.");
            startCapture();
        } else if (message.action === "stopCapture") {
            console.log("Recebido stopCapture no Offscreen.");
            stopCapture();
        }
    });

    console.log("Offscreen document carregado e aguardando mensagens.");
});
