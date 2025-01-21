const serverUrl = "http://localhost:5000";
let isTrackingActive = false;

async function checkServerStatus() {
    try {
        const response = await fetch(`${serverUrl}/status`);
        if (response.ok) {
            console.log("Servidor Python ativo.");
            return true;
        }
        throw new Error("Falha ao acessar o servidor.");
    } catch (error) {
        console.error("Erro de conexão:", error.message);
        return false;
    }
}
