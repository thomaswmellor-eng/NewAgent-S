# 🚀 START HERE - Agent S3 Desktop

## Lancement Ultra-Rapide

### Windows

Double-cliquez sur **`launch.bat`** et c'est tout! 🎉

Ou en ligne de commande:
```bash
npm install
npm start
```

### macOS / Linux

```bash
npm install
npm start
```

---

## Qu'est-ce que c'est?

Agent S3 Desktop est une **application native** (comme NordVPN, Discord, Slack) qui:

✅ Contrôle **tout ton ordinateur** (pas juste Chrome)
✅ Tourne en **arrière-plan** (system tray)
✅ Se lance avec **raccourci global** (`Ctrl+Shift+A`)
✅ Interface **moderne** (shadcn/ui design)
✅ **LinkedIn automation** intégrée

---

## Première Utilisation

### 1. Installer Node.js (si pas déjà fait)

Téléchargez: https://nodejs.org/ (version LTS)

### 2. Lancer l'app

```bash
# Option 1: Double-clic
launch.bat

# Option 2: Commande
cd desktop-app
npm install
npm start
```

### 3. Tester

Dans l'app, tapez:
```
Va sur google.com
```

**Ça y est, ça marche!** 🎉

---

## Créer l'Installateur .exe

Pour distribuer l'app:

```bash
npm run build:win
```

Résultat: `dist/Agent-S3-Setup.exe` (distributable)

---

## Fonctionnalités

### System Tray
- Icône près de l'horloge
- Click droit → menu
- Double-clic → toggle fenêtre

### Raccourcis
- **Ctrl+Shift+A**: Afficher/masquer
- **Ctrl+R**: Recharger (dev)
- **Ctrl+Shift+I**: DevTools (dev)

### Configuration
- URL de l'API backend
- Activer la réflexion
- Toujours au-dessus
- Lancer au démarrage
- Démarrer minimisé

---

## Structure

```
desktop-app/
├── launch.bat          ← LANCE MOI!
├── setup.bat           ← Installe les dépendances
├── main.js             ← Main process (system tray)
├── preload.js          ← Bridge sécurisé
├── renderer/           ← Interface utilisateur
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── assets/
│   ├── icon.png        ← Icône 512x512
│   └── icon-tray.png   ← Icône tray 256x256
└── docs/
    ├── README.md       ← Documentation complète
    ├── INSTALL.md      ← Guide d'installation
    └── QUICKSTART.md   ← Démarrage rapide
```

---

## Exemples de Commandes

### Navigation Web
```
"Va sur linkedin.com"
"Ouvre google.com et cherche Python tutorials"
"Va sur github.com/anthropics"
```

### LinkedIn Automation
```
"Like 5 posts sur LinkedIn"
"Connecte-toi avec 10 développeurs Python"
"Commente 3 posts sur l'IA"
"Cherche des CTOs dans le secteur tech"
```

### Actions Système
```
"Prends un screenshot"
"Ouvre le bloc-notes"
"Cherche des fichiers Python dans Documents"
```

---

## Différences vs Extension Chrome

| Feature | Extension | Desktop App |
|---------|-----------|-------------|
| Scope | Chrome only | Tout le PC |
| Installation | Web Store | .exe |
| Persistence | Side panel | System tray |
| Shortcuts | ❌ | ✅ Ctrl+Shift+A |
| Startup | ❌ | ✅ Launch au démarrage |
| Distribution | Web Store | Partage .exe |

---

## FAQ

### ❓ Quelle différence avec l'extension Chrome?

L'extension Chrome ne peut contrôler que le navigateur.
L'app desktop contrôle **tout ton PC**.

### ❓ Est-ce que je peux distribuer l'app?

Oui! Build l'exe avec `npm run build:win` et partage-le.
L'utilisateur fait juste double-clic, pas besoin de Node.js.

### ❓ Quelle est la taille de l'exe?

~150-200 MB (contient Chromium)

### ❓ L'app se lance au démarrage?

C'est optionnel. Configure-le dans Settings.

### ❓ Comment changer l'icône?

1. Édite `assets/icon.svg` avec ton design
2. Lance `python create_icon.py`
3. Convertis en .ico sur https://convertio.co/png-ico/

### ❓ Le backend doit tourner?

Oui! L'app se connecte à `http://localhost:8000`.
Lance le backend avec: `python backend/main.py`

---

## Troubleshooting

### "npm not found"
→ Installe Node.js: https://nodejs.org/

### L'app ne se connecte pas
→ Vérifie que le backend tourne sur `localhost:8000`

### Le raccourci ne fonctionne pas
→ Une autre app utilise `Ctrl+Shift+A`. Change-le dans `main.js`

### Build échoue
→ `npm install --global windows-build-tools`

---

## Prochaines Étapes

1. ✅ Lance l'app: `launch.bat` ou `npm start`
2. ✅ Teste une commande: "Va sur google.com"
3. ✅ Configure dans Settings
4. ✅ Build l'exe: `npm run build:win`
5. ✅ Partage l'app!

---

## Documentation

- [README.md](./README.md) - Documentation complète
- [INSTALL.md](./INSTALL.md) - Guide d'installation détaillé
- [QUICKSTART.md](./QUICKSTART.md) - Démarrage en 3 étapes
- [assets/README.md](./assets/README.md) - Guide icônes

---

**Enjoy! 🚀**

Questions? Lis [README.md](./README.md) ou check le code!
