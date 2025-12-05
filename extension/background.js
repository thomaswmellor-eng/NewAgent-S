/**
 * Background Service Worker pour Agent S3 Extension
 * Gère la communication en arrière-plan et le side panel
 */

// Installation de l'extension
chrome.runtime.onInstalled.addListener(() => {
    console.log('✅ Agent S3 Extension installée');

    // Définir les paramètres par défaut
    chrome.storage.local.set({
        apiUrl: 'http://localhost:8000',
        enableReflection: true
    });
});

// Ouvrir le side panel quand l'utilisateur clique sur l'icône
chrome.action.onClicked.addListener((tab) => {
    chrome.sidePanel.open({ windowId: tab.windowId });
});

// Gestion des messages depuis le side panel
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'checkHealth') {
        // Vérifier l'état de l'API
        fetch(`${request.apiUrl}/health`)
            .then(response => response.json())
            .then(data => {
                sendResponse({ success: true, data });
            })
            .catch(error => {
                sendResponse({ success: false, error: error.message });
            });
        return true; // Indique qu'on va répondre de manière asynchrone
    }
});

// Notification quand l'action est terminée (optionnel)
chrome.runtime.onConnect.addListener((port) => {
    console.log('✅ Port connecté:', port.name);
});
