# Guide d'Installation - Agent S3 Desktop

## Installation Rapide

### 1. Installer Node.js

Si pas encore installé:
- Téléchargez depuis https://nodejs.org/ (version LTS)
- Installez avec les options par défaut

### 2. Installer les dépendances

```bash
cd desktop-app
npm install
```

Cela va installer:
- Electron (framework desktop)
- electron-builder (pour créer l'installateur)
- electron-store (pour stocker la config)

### 3. Lancer l'application

```bash
npm start
```

L'app se lance immédiatement! 🚀

## Créer l'installateur Windows (.exe)

### Option 1: Build simple

```bash
npm run build:win
```

Cela crée:
- `dist/Agent-S3-Setup.exe` (installateur NSIS)
- Prend 2-3 minutes

### Option 2: Build avec icône personnalisée

1. Convertir l'icône SVG en .ico:
   - Utilisez un outil en ligne: https://convertio.co/svg-ico/
   - Ou: https://cloudconvert.com/svg-to-ico
   - Téléchargez `assets/icon.svg`
   - Convertissez en .ico (512x512)
   - Sauvegardez dans `assets/icon.ico`

2. Build:
```bash
npm run build:win
```

## Tester l'installateur

1. Allez dans `dist/`
2. Double-cliquez sur `Agent-S3-Setup.exe`
3. Suivez les instructions d'installation
4. Agent S3 sera installé dans `C:\Program Files\Agent S3`

## Distribution

### Partager l'app

Partagez simplement `dist/Agent-S3-Setup.exe`:
- Taille: ~150-200 MB (contient Chromium)
- L'utilisateur final fait juste double-clic
- Pas besoin d'installer Node.js ou autres dépendances

### Options d'installation

L'installateur NSIS propose:
- Choix du dossier d'installation
- Créer un raccourci bureau
- Créer un raccourci menu démarrer
- Lancer au démarrage (optionnel)

## Configuration Backend

Avant de lancer l'app desktop, assurez-vous que le backend tourne:

```bash
# Dans le dossier principal Agent-S
python backend/main.py
```

Le backend doit être sur `http://localhost:8000`

## Dépannage

### Erreur "npm not found"

Installez Node.js: https://nodejs.org/

### Erreur "electron-builder not found"

```bash
npm install --save-dev electron-builder
```

### L'app ne se lance pas

1. Vérifiez les logs dans la console
2. Ouvrez DevTools: Ctrl+Shift+I
3. Vérifiez que le backend tourne

### Build échoue sur Windows

Si vous avez une erreur avec electron-builder:

```bash
# Installer les outils de build Windows
npm install --global windows-build-tools
```

Ou utilisez Visual Studio Build Tools.

## Prochaines Étapes

Une fois l'app installée:

1. **Lancez l'app** (icône bureau ou menu démarrer)
2. **Configurez** l'URL du backend dans settings
3. **Testez** avec une commande simple: "Va sur google.com"
4. **Raccourci** Ctrl+Shift+A pour afficher/masquer

Enjoy! 🚀
