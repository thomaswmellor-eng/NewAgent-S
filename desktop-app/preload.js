/**
 * Agent S3 Desktop - Preload Script
 * Bridge sécurisé entre le main process et le renderer process
 */

const { contextBridge, ipcRenderer } = require('electron');

// Exposer les APIs sécurisées au renderer
contextBridge.exposeInMainWorld('electronAPI', {
    // Configuration
    getConfig: () => ipcRenderer.invoke('get-config'),
    saveConfig: (config) => ipcRenderer.invoke('save-config', config),

    // Fenêtre
    minimizeToTray: () => ipcRenderer.invoke('minimize-to-tray'),
    setAlwaysOnTop: (flag) => ipcRenderer.invoke('set-always-on-top', flag),

    // Événements
    onOpenSettings: (callback) => {
        ipcRenderer.on('open-settings', callback);
    }
});

console.log('✅ Preload script chargé');
