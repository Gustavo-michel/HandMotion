const serverUrl = "http://localhost:5000";
let isTrackingActive = false;

async function checkServerStatus() {
    try {
        const response = await fetch(`${serverUrl}/status`);
        if (response.ok) {
            console.log("Active Python server.");
            return true;
        }
        throw new Error("Failed to access the server.");
    } catch (error) {
        console.error("Connection error:", error.message);
        return false;
    }
}
