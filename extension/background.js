async function ensureOffscreenDocument() {
    if (await chrome.offscreen.hasDocument()) {
        console.log("Offscreen document already exists.");
        return;
    }

    await chrome.offscreen.createDocument({
        url: "offscreen/offscreen.html",
        reasons: ["USER_MEDIA"], 
        justification: "Webcam video capture for gesture analysis."
    });

    console.log("Offscreen document created successfully.");
}

// Listener messages from popup
chrome.runtime.onMessage.addListener((message) => {
    if (message.action === 'start') {
        ensureOffscreenDocument().then(() => {
            console.log("Sending message to start capture.");
            chrome.runtime.sendMessage({ action: 'startCapture' });
        });
    } else if (message.action === 'stop') {
        console.log("Sending message to stop capture.");
        chrome.runtime.sendMessage({ action: 'stopCapture' });
    }
});
