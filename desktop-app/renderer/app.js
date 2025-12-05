/**
 * Flemme - Renderer Process
 * Interface utilisateur avec communication WebSocket
 */

// Configuration (hardcodée - pas de settings UI)
let config = {
    apiUrl: 'http://localhost:8000',
    enableReflection: true,
    ws: null
};

// Éléments DOM
const chatContainer = document.getElementById('chatContainer');
const promptInput = document.getElementById('promptInput');
const sendButton = document.getElementById('sendButton');
const stopButton = document.getElementById('stopButton');
const statusElement = document.getElementById('status');

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    connectWebSocket();
});

// Setup des event listeners
function setupEventListeners() {
    // Envoyer le message
    sendButton.addEventListener('click', sendMessage);

    // Arrêter l'exécution
    stopButton.addEventListener('click', stopExecution);

    promptInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize du textarea
    promptInput.addEventListener('input', () => {
        promptInput.style.height = 'auto';
        promptInput.style.height = promptInput.scrollHeight + 'px';
    });
}

// Connexion WebSocket
function connectWebSocket() {
    updateStatus('connecting', 'Connexion...');

    try {
        const wsUrl = config.apiUrl.replace('http://', 'ws://').replace('https://', 'wss://');
        config.ws = new WebSocket(`${wsUrl}/ws/agent`);

        config.ws.onopen = () => {
            console.log('✅ WebSocket connecté');
            updateStatus('connected', 'Connecté');
        };

        config.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleServerMessage(data);
        };

        config.ws.onerror = (error) => {
            console.error('❌ Erreur WebSocket:', error);
            updateStatus('error', 'Erreur');
            addMessage('error', '❌ Erreur de connexion au serveur');
        };

        config.ws.onclose = () => {
            console.log('🔌 WebSocket déconnecté');
            updateStatus('disconnected', 'Déconnecté');

            // Reconnexion après 2 secondes
            addMessage('system', '🔌 Connexion fermée. Reconnexion automatique...');
            setTimeout(() => {
                connectWebSocket();
            }, 2000);
        };

    } catch (error) {
        console.error('❌ Erreur lors de la connexion:', error);
        updateStatus('error', 'Erreur');
        addMessage('error', '❌ Impossible de se connecter au serveur');
    }
}

// Envoyer un message
function sendMessage() {
    const prompt = promptInput.value.trim();

    if (!prompt) return;

    if (!config.ws || config.ws.readyState !== WebSocket.OPEN) {
        addMessage('error', '❌ Pas de connexion au serveur');
        return;
    }

    // Afficher le message de l'utilisateur
    addMessage('user', prompt);

    // Envoyer au serveur
    config.ws.send(JSON.stringify({
        prompt: prompt,
        enableReflection: config.enableReflection
    }));

    // Clear input
    promptInput.value = '';
    promptInput.style.height = 'auto';

    // Disable send button and show stop button
    sendButton.disabled = true;
    sendButton.classList.add('hidden');
    stopButton.classList.remove('hidden');
}

// Arrêter l'exécution en cours
function stopExecution() {
    if (!config.ws || config.ws.readyState !== WebSocket.OPEN) {
        return;
    }

    // Envoyer la commande stop au serveur
    config.ws.send(JSON.stringify({
        command: 'stop'
    }));

    addMessage('system', '⛔ Demande d\'arrêt envoyée...');

    // Réactiver l'interface
    sendButton.disabled = false;
    sendButton.classList.remove('hidden');
    stopButton.classList.add('hidden');
}

// Gérer les messages du serveur
function handleServerMessage(data) {
    console.log('📨 Message reçu:', data);

    switch (data.type) {
        case 'status':
            addMessage('system', data.message);
            break;

        case 'start':
            addMessage('system', '🚀 Traitement en cours...');
            break;

        case 'thinking':
            addMessage('thinking', data.message);
            break;

        case 'translated':
            // Afficher la traduction du prompt
            addMessage('system', `📝 Prompt original: "${data.original}"`);
            addMessage('success', `✨ Traduit en: "${data.translated}"`);
            break;

        case 'reflection':
            addMessage('agent', `🤔 Réflexion: ${data.content}`);
            break;

        case 'action':
            addMessage('action', `⚡ Action: ${data.content}`);
            break;

        case 'success':
            addMessage('success', data.message);
            sendButton.disabled = false;
            sendButton.classList.remove('hidden');
            stopButton.classList.add('hidden');
            break;

        case 'error':
            addMessage('error', data.message);
            sendButton.disabled = false;
            sendButton.classList.remove('hidden');
            stopButton.classList.add('hidden');
            break;

        case 'stopped':
            addMessage('error', data.message);
            sendButton.disabled = false;
            sendButton.classList.remove('hidden');
            stopButton.classList.add('hidden');
            break;

        default:
            console.warn('Type de message inconnu:', data.type);
    }
}

// Ajouter un message au chat
function addMessage(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Mettre à jour le statut
function updateStatus(status, text) {
    const statusText = statusElement.querySelector('.status-text');
    statusElement.className = `status ${status}`;
    statusText.textContent = text;
}

// Health check périodique
setInterval(() => {
    if (config.ws && config.ws.readyState === WebSocket.OPEN) {
        // Optionnel: ping/pong pour garder la connexion active
    }
}, 30000);

console.log('✅ Renderer process chargé');
