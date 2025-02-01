/* Changer page selon bouton */
window.addEventListener('DOMContentLoaded', () => {
    // Masquer le chatbot IA au chargement de la page
    document.querySelector('.ai-chatting').classList.add('hidden');

    document.querySelector('.container').classList.remove('hidden');
    document.querySelector('.how-it-works').classList.remove('hidden');
    document.querySelector('.divider').classList.remove('hidden');

    // Activer par défaut le bouton "Plusieurs articles"
    document.getElementById('several-articles').classList.add('active');
});
document.getElementById('several-articles').addEventListener('click', () => {
    document.querySelector('.container').classList.remove('hidden');
    document.querySelector('.how-it-works').classList.remove('hidden');
    document.querySelector('.divider').classList.remove('hidden');
    document.querySelector('.ai-chatting').classList.add('hidden');

    document.getElementById('several-articles').classList.add('active');
    document.getElementById('one-article').classList.remove('active');
});

document.getElementById('one-article').addEventListener('click', () => {
    document.querySelector('.container').classList.add('hidden');
    document.querySelector('.how-it-works').classList.add('hidden');
    document.querySelector('.divider').classList.add('hidden');
    document.querySelector('.ai-chatting').classList.remove('hidden');

    document.getElementById('one-article').classList.add('active');
    document.getElementById('several-articles').classList.remove('active');
});

/* Enlever phrase du chatbot quand on écrit */
const textarea = document.getElementById('user-input');

// Lorsque l'utilisateur clique dans la zone de texte
textarea.addEventListener('focus', () => {
    textarea.placeholder = '';
});
// Lorsque l'utilisateur quitte la zone de texte sans rien écrire
textarea.addEventListener('blur', () => {
    if (textarea.value.trim() === '') {
        textarea.placeholder = "Copiez l'article à analyser ici";
    }
});

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

/* Envoyer PDF a S3 */
document.getElementById('fileInput').addEventListener('change', function () {
    const file = this.files[0];
    const fileNameDisplay = document.getElementById('fileName');

    if (file) {
        fileNameDisplay.textContent = `Fichier sélectionné : ${file.name}`; // Affiche le nom du fichier
    } else {
        fileNameDisplay.textContent = ''; // Efface le texte si aucun fichier sélectionné
    }
});

document.getElementById('fileInput').addEventListener('change', function () {
    const file = this.files[0];
    const fileNameDisplay = document.getElementById('fileName');

    if (file) {
        fileNameDisplay.textContent = `Fichier sélectionné : ${file.name}`; // Affiche le nom du fichier
    } else {
        fileNameDisplay.textContent = ''; // Efface le texte si aucun fichier sélectionné
    }
});

document.getElementById('uploadBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        document.getElementById('uploadStatus').innerText = 'Veuillez sélectionner un fichier PDF.';
        return;
    }

    const reader = new FileReader();
    reader.onload = async function () {
        const base64File = reader.result.split(',')[1];

        try {
            const response = await fetch('https://cdmjon52vg.execute-api.us-west-2.amazonaws.com/dev', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body: base64File, isBase64Encoded: true })
            });

            const data = await response.json();
            document.getElementById('uploadStatus').innerText = data.result || 'Analyse terminée !';
        } catch (error) {
            console.error('Erreur:', error);
            document.getElementById('uploadStatus').innerText = 'Erreur lors de l’envoi du fichier.';
        }
    };

    reader.readAsDataURL(file);
});
