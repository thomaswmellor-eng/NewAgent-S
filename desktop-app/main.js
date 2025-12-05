/**
 * Flemme - Main Process
 * Electron main process with system tray and global shortcuts
 */

const { app, BrowserWindow, Tray, Menu, globalShortcut, screen, dialog } = require('electron');
const path = require('path');
const Store = require('electron-store');
const { spawn } = require('child_process');

// Configuration store
const store = new Store();

let mainWindow = null;
let tray = null;
let backendProcess = null;

// Configuration par défaut
const defaultConfig = {
    apiUrl: 'http://localhost:8000',
    enableReflection: true,
    windowWidth: 400,
    windowHeight: 600,
    alwaysOnTop: true,
    startMinimized: false,
    launchOnStartup: false
};

// Charger la config
function getConfig() {
    return { ...defaultConfig, ...store.get('config', {}) };
}

// Sauvegarder la config
function saveConfig(config) {
    store.set('config', config);
}

// Créer la fenêtre principale
function createWindow() {
    const config = getConfig();
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    mainWindow = new BrowserWindow({
        width: config.windowWidth,
        height: config.windowHeight,
        x: width - config.windowWidth - 20, // Position à droite de l'écran
        y: 20,
        frame: true,
        transparent: false,
        backgroundColor: '#000000',
        alwaysOnTop: config.alwaysOnTop,
        skipTaskbar: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        },
        icon: path.join(__dirname, 'assets', 'icon.png')
    });

    // Charger l'interface
    mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

    // Ouvrir DevTools en développement
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }

    // Événements de la fenêtre
    mainWindow.on('close', (event) => {
        if (!app.isQuitting) {
            event.preventDefault();
            mainWindow.hide();
        }
        return false;
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // Ne pas afficher si startMinimized
    if (config.startMinimized) {
        mainWindow.hide();
    }
}

// Créer le system tray
function createTray() {
    const iconPath = path.join(__dirname, 'assets', 'icon.png');
    tray = new Tray(iconPath);

    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Afficher Flemme',
            click: () => {
                if (mainWindow) {
                    mainWindow.show();
                    mainWindow.focus();
                } else {
                    createWindow();
                }
            }
        },
        {
            label: 'Masquer',
            click: () => {
                if (mainWindow) {
                    mainWindow.hide();
                }
            }
        },
        { type: 'separator' },
        {
            label: 'Toujours au-dessus',
            type: 'checkbox',
            checked: getConfig().alwaysOnTop,
            click: (menuItem) => {
                const config = getConfig();
                config.alwaysOnTop = menuItem.checked;
                saveConfig(config);
                if (mainWindow) {
                    mainWindow.setAlwaysOnTop(menuItem.checked);
                }
            }
        },
        { type: 'separator' },
        {
            label: 'Paramètres',
            click: () => {
                if (mainWindow) {
                    mainWindow.show();
                    mainWindow.focus();
                    mainWindow.webContents.send('open-settings');
                }
            }
        },
        { type: 'separator' },
        {
            label: 'Quitter',
            click: () => {
                app.isQuitting = true;
                app.quit();
            }
        }
    ]);

    tray.setToolTip('Flemme - AI Assistant');
    tray.setContextMenu(contextMenu);

    // Double-clic sur l'icône pour afficher/masquer
    tray.on('double-click', () => {
        if (mainWindow) {
            if (mainWindow.isVisible()) {
                mainWindow.hide();
            } else {
                mainWindow.show();
                mainWindow.focus();
            }
        }
    });
}

// Configurer le lancement au démarrage
function setLoginItemSettings() {
    const config = getConfig();
    app.setLoginItemSettings({
        openAtLogin: config.launchOnStartup,
        openAsHidden: config.startMinimized
    });
}

// Démarrer le backend bundlé
function startBackend() {
    // Déterminer le chemin du backend selon l'environnement
    let backendPath;

    if (app.isPackaged) {
        // En production: backend dans resources/backend/
        backendPath = path.join(process.resourcesPath, 'backend', 'flemme-backend', 'flemme-backend.exe');
    } else {
        // En développement: backend dans ../backend/dist/
        backendPath = path.join(__dirname, '..', 'backend', 'dist', 'flemme-backend', 'flemme-backend.exe');
    }

    console.log('🚀 Démarrage du backend:', backendPath);

    try {
        backendProcess = spawn(backendPath, [], {
            stdio: ['ignore', 'pipe', 'pipe'],
            detached: false,
            windowsHide: true  // Cache la console Windows
        });

        // Log stdout pour debug
        backendProcess.stdout.on('data', (data) => {
            console.log('Backend:', data.toString());
        });

        // Log stderr pour debug
        backendProcess.stderr.on('data', (data) => {
            console.error('Backend Error:', data.toString());
        });

        backendProcess.on('error', (err) => {
            console.error('❌ Erreur backend:', err);
            dialog.showErrorBox(
                'Erreur de démarrage',
                `Le backend n'a pas pu démarrer:\n${err.message}\n\nChemin: ${backendPath}`
            );
        });

        backendProcess.on('exit', (code, signal) => {
            if (code !== 0 && code !== null) {
                console.error(`❌ Backend s'est arrêté avec le code ${code}`);
            }
        });

        console.log('✅ Backend démarré avec PID:', backendProcess.pid);

    } catch (error) {
        console.error('❌ Impossible de démarrer le backend:', error);
        dialog.showErrorBox(
            'Erreur de démarrage',
            `Impossible de démarrer le backend:\n${error.message}`
        );
    }
}

// Arrêter le backend
function stopBackend() {
    if (backendProcess) {
        console.log('🛑 Arrêt du backend...');
        backendProcess.kill();
        backendProcess = null;
    }
}

// Initialisation de l'app
app.whenReady().then(() => {
    // Démarrer le backend d'abord
    startBackend();

    // Attendre 3 secondes que le backend démarre
    setTimeout(() => {
        createWindow();
        createTray();
        setLoginItemSettings();
    }, 3000);

    // Raccourci clavier global: Ctrl+Shift+A
    const registered = globalShortcut.register('CommandOrControl+Shift+A', () => {
        if (mainWindow) {
            if (mainWindow.isVisible()) {
                mainWindow.hide();
            } else {
                mainWindow.show();
                mainWindow.focus();
            }
        }
    });

    if (!registered) {
        console.error('❌ Échec de l\'enregistrement du raccourci global');
    }

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// Quitter quand toutes les fenêtres sont fermées (sauf sur macOS)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Libérer les raccourcis globaux à la fermeture
app.on('will-quit', () => {
    globalShortcut.unregisterAll();
    stopBackend();
});

// Arrêter le backend avant de quitter
app.on('before-quit', () => {
    stopBackend();
});

// IPC handlers pour la communication avec le renderer
const { ipcMain } = require('electron');

ipcMain.handle('get-config', () => {
    return getConfig();
});

ipcMain.handle('save-config', (event, config) => {
    saveConfig(config);
    setLoginItemSettings();
    return true;
});

ipcMain.handle('minimize-to-tray', () => {
    if (mainWindow) {
        mainWindow.hide();
    }
});

ipcMain.handle('set-always-on-top', (event, flag) => {
    if (mainWindow) {
        mainWindow.setAlwaysOnTop(flag);
    }
});

console.log('✅ Flemme lancé');
