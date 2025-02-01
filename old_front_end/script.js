/*document.getElementById("fileInput").addEventListener("change", function () {
    let file = this.files[0];
    if (file) {
        document.getElementById("fileName").textContent = "Fichier sélectionné : " + file.name;
    }
});

document.getElementById("uploadBtn").addEventListener("click", function () {
    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) {
        document.getElementById("uploadStatus").textContent = "Veuillez sélectionner un fichier !";
        return;
    }

    let formData = new FormData();
    formData.append("file", file);
});*/

/* Requete vers API */
async function sendMessageToAI() {
    const userMessage = document.getElementById('user-input').value;

    try {
        const payload = JSON.stringify({ message: userMessage });

        const response = await fetch('https://6n9kl3vvv8.execute-api.us-west-2.amazonaws.com/dev', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: payload
        });

        const data = await response.json();

        if (data.body) {
            const parsedBody = JSON.parse(data.body);
            document.getElementById('ai-response').innerText = parsedBody.reply || parsedBody.error;
        } else {
            document.getElementById('ai-response').innerText = 'Aucune réponse reçue.';
        }
    } catch (error) {
        document.getElementById('ai-response').innerText = 'Une erreur est survenue. Veuillez réessayer.';
    }
}
