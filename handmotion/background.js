async function ensureOffscreenDocument() {
    if (await chrome.offscreen.hasDocument()) {
        console.log("Documento offscreen já existe.");
        return;
    }

    await chrome.offscreen.createDocument({
        url: "offscreen/offscreen.html",
        reasons: ["USER_MEDIA"], 
        justification: "Captura de vídeo da webcam para análise de gestos"
    });

    console.log("Offscreen document criado com sucesso.");
}

// Listener messages from popup
chrome.runtime.onMessage.addListener((message) => {
    if (message.action === 'start') {
        ensureOffscreenDocument().then(() => {
            console.log("Enviando mensagem para iniciar captura.");
            chrome.runtime.sendMessage({ action: 'startCapture' });
        });
    } else if (message.action === 'stop') {
        console.log("Enviando mensagem para parar captura.");
        chrome.runtime.sendMessage({ action: 'stopCapture' });
    }
});
