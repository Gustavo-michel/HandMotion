let socket;

chrome.runtime.onInstalled.addListener(() => {
    socket = new WebSocket("ws://localhost:5000");

    socket.onopen = () => {
        console.log("WebSocket connection opened.");
    };

    socket.onmessage = (event) => {
        console.log("Message received: ", event.data);
    };

    socket.onclose = () => {
        console.log("WebSocket connection closed.");
    };

    socket.onerror = (error) => {
        console.error("WebSocket error: ", error);
    };
});

function sendMessageToServer(message) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    } else {
        console.error("WebSocket is not open. Cannot send message.");
    }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "start_tracking") {
        sendMessageToServer("start_tracking");
        sendResponse({ status: "Tracking started" });
    }
});
