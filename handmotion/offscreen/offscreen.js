const socket = io("http://localhost:5000");

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
                      blob.arrayBuffer().then(buffer => {
                          socket.emit("frame", buffer);
                      });
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
    }
  
    chrome.runtime.onMessage.addListener((message) => {
        if (message.action === "startCapture") {
            startCapture();
        } else if (message.action === "stopCapture") {
            stopCapture();
        }
    });
});
