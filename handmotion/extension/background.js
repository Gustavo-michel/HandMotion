const serverUrl = "http://localhost:5000";

async function sendMessageToContentScript(tabId, message) {
  try {
    await chrome.scripting.executeScript({
      target: { tabId: tabId },
      func: (message) => {
        console.log("Message from background:", message);
        alert(`Gesture detected: ${message.gesture}`);
      },
      args: [message],
    });
  } catch (error) {
    console.error("Error sending message:", error);
  }
}

fetch(`${serverUrl}/status`)
  .then((response) => {
    if (!response.ok) throw new Error("Python server not running");
    console.log("Python server is running");
  })
  .catch((error) => console.error("Python server error:", error));

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "gesture_detected") {
    sendMessageToContentScript(sender.tab.id, message);
    sendResponse({ status: "Received" });
  }
});
