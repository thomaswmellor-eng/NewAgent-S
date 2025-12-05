# Agent S3 Desktop

Application desktop native pour contrôler votre ordinateur avec Agent S3.

## Fonctionnalités

✅ **Application Native**
- Fonctionne comme NordVPN, Discord, etc.
- Icône dans le system tray (près de l'horloge)
- Lance au démarrage (optionnel)

✅ **Interface Moderne**
- Design shadcn/ui élégant
- Fenêtre flottante à droite de l'écran
- Toujours au-dessus (optionnel)

✅ **Contrôle Complet**
- Contrôle tout votre PC (pas juste Chrome)
- WebSocket vers le backend Agent S3
- LinkedIn automation, navigation web, etc.

✅ **Raccourcis**
- `Ctrl+Shift+A` : Afficher/masquer la fenêtre
- Double-clic sur tray icon : Toggle fenêtre
- Click droit sur tray : Menu contextuel

## Installation

### Méthode 1: Installer depuis le .exe (Recommandé)

1. Téléchargez `Agent-S3-Setup.exe` depuis les releases
2. Double-cliquez pour installer
3. Lancez Agent S3 depuis le menu démarrer

### Méthode 2: Développement

```bash
cd desktop-app

# Installer les dépendances
npm install

# Lancer en mode développement
npm start

# Builder l'installateur Windows
npm run build:win
```

## Configuration

Cliquez sur l'icône ⚙️ en haut à droite pour configurer:

- **URL de l'API**: `http://localhost:8000` (backend Agent S3)
- **Activer la réflexion**: Affiche le raisonnement de l'agent
- **Toujours au-dessus**: Fenêtre reste au-dessus des autres
- **Lancer au démarrage**: Lance automatiquement avec Windows
- **Démarrer minimisé**: Lance dans le tray sans afficher la fenêtre

## Utilisation

1. **Lancer l'app**: Double-clic sur l'icône ou `Ctrl+Shift+A`
2. **Envoyer une commande**: Tapez dans l'input et appuyez sur Entrée
3. **Minimiser**: Cliquez sur X ou `Ctrl+Shift+A`
4. **Quitter**: Click droit sur tray icon → Quitter

### Exemples de commandes

```
"Va sur linkedin.com et like 5 posts"
"Ouvre Google et cherche Python tutorials"
"Prends un screenshot et analyse-le"
"Connecte-toi avec 10 développeurs sur LinkedIn"
```

## Architecture

```
desktop-app/
├── main.js              # Main process (Electron)
├── preload.js           # Preload script (bridge sécurisé)
├── renderer/
│   ├── index.html       # Interface utilisateur
│   ├── app.js           # Logique renderer
│   └── styles.css       # Styles shadcn/ui
├── assets/
│   └── icon.png         # Icône de l'app
└── package.json         # Configuration npm
```

## Build

### Windows (.exe)

```bash
npm run build:win
```

Génère `dist/Agent-S3-Setup.exe`

### Mac (.dmg)

```bash
npm run build:mac
```

### Linux (.AppImage)

```bash
npm run build:linux
```

## Troubleshooting

### L'app ne se connecte pas au backend

Vérifiez que:
1. Le backend Agent S3 tourne sur `http://localhost:8000`
2. L'URL dans les settings est correcte
3. Pas de firewall qui bloque la connexion

### Le raccourci Ctrl+Shift+A ne fonctionne pas

Le raccourci est peut-être utilisé par une autre app. Modifiez-le dans `main.js`:

```javascript
globalShortcut.register('CommandOrControl+Alt+A', () => {
    // ...
});
```

### La fenêtre ne reste pas au-dessus

Activez "Toujours au-dessus" dans les settings.

## Développement

### Hot Reload

En mode dev (`npm start`), les modifications sont automatiquement prises en compte:
- Modifiez `renderer/*` → Rechargez avec `Ctrl+R`
- Modifiez `main.js` → Relancez l'app

### DevTools

En mode dev, les DevTools s'ouvrent automatiquement. Pour les ouvrir manuellement:
- `Ctrl+Shift+I` ou `F12`

## Licence

MIT
