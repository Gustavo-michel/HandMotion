const serverUrl = "http://localhost:5000";
let isTrackingActive = false;

async function checkServerStatus() {
    try {
        const response = await fetch(`${serverUrl}/status`);
        if (!response.ok) throw new Error("Servidor Python não está ativo");
        console.log("Servidor Python está ativo.");
        return true;
    } catch (error) {
        console.error("Erro ao conectar ao servidor Python:", error);
        return false;
    }
}