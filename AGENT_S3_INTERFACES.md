# 🎨 Agent S3 - Interfaces Utilisateur

Ce document présente les **2 interfaces** disponibles pour utiliser Agent S3:
1. **Extension Chrome** (contrôle du navigateur)
2. **Application Desktop** (contrôle complet du PC)

---

## 📌 Vue d'Ensemble

| Feature | Extension Chrome | Desktop App |
|---------|-----------------|-------------|
| **Type** | Extension navigateur | Application native |
| **Scope** | Chrome uniquement | Tout l'ordinateur |
| **Installation** | Chrome → Charger extension | Exe téléchargeable |
| **Persistence** | Side panel Chrome | System tray Windows |
| **Shortcuts** | ❌ | ✅ Ctrl+Shift+A global |
| **Startup** | ❌ | ✅ Lance avec Windows |
| **Distribution** | Fichiers sources | Agent-S3-Setup.exe |
| **UI** | shadcn/ui design | shadcn/ui design |

---

## 1️⃣ Extension Chrome

### Localisation
```
extension/
├── manifest.json       # Configuration Chrome extension
├── background.js       # Service worker (side panel)
├── popup.html          # Interface utilisateur
├── popup.js            # Logique (WebSocket)
└── styles.css          # Design shadcn/ui
```

### Installation

1. Ouvrir Chrome
2. Aller sur `chrome://extensions/`
3. Activer "Mode développeur"
4. Cliquer "Charger l'extension non empaquetée"
5. Sélectionner le dossier `extension/`

### Utilisation

- Cliquer sur l'icône Agent S3 dans la barre d'outils
- L'extension s'ouvre en **side panel** (reste ouverte)
- Contrôle du **navigateur Chrome** uniquement

### Fonctionnalités

✅ Navigation web automatisée
✅ LinkedIn automation (like, comment, connect)
✅ Form filling
✅ Scraping et extraction de données
✅ Contrôle d'onglets

❌ Ne peut PAS contrôler en dehors de Chrome

### Documentation

- [extension/README.md](./extension/README.md) - Documentation complète

---

## 2️⃣ Application Desktop (Recommandé)

### Localisation
```
desktop-app/
├── main.js             # Main process (system tray, shortcuts)
├── preload.js          # Bridge sécurisé
├── renderer/           # Interface utilisateur
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── assets/
│   └── icon.png        # Icône de l'app
├── package.json        # Config npm + build
└── docs...
```

### Installation Rapide

```bash
cd desktop-app
npm install
npm start
```

Ou double-clic sur `desktop-app/launch.bat`

### Créer l'Installateur

```bash
cd desktop-app
npm run build:win
```

Résultat: `dist/Agent-S3-Setup.exe` (~150-200 MB)

### Utilisation

- **Lancement**: Double-clic sur l'icône ou `Ctrl+Shift+A`
- **System Tray**: Icône près de l'horloge Windows
- **Shortcuts**: `Ctrl+Shift+A` pour toggle la fenêtre
- **Settings**: Clic sur ⚙️ en haut à droite

### Fonctionnalités

✅ **Contrôle complet du PC** (pas limité au navigateur)
✅ LinkedIn automation
✅ Navigation web (tous les navigateurs)
✅ Contrôle d'applications
✅ Screenshots système
✅ Automatisation de fichiers
✅ System tray toujours disponible
✅ Raccourci clavier global
✅ Lance au démarrage (optionnel)

### Configuration

Dans Settings (⚙️):
- **URL de l'API**: `http://localhost:8000` (backend)
- **Activer la réflexion**: Affiche le raisonnement
- **Toujours au-dessus**: Fenêtre flottante
- **Lancer au démarrage**: Auto-start avec Windows
- **Démarrer minimisé**: Lance dans le tray

### Distribution

Partage simplement `dist/Agent-S3-Setup.exe`:
- L'utilisateur fait double-clic
- Installation automatique
- Pas besoin de Node.js, Python, etc.

### Documentation

- [desktop-app/START_HERE.md](./desktop-app/START_HERE.md) - 🚀 Démarrage ultra-rapide
- [desktop-app/README.md](./desktop-app/README.md) - Documentation complète
- [desktop-app/INSTALL.md](./desktop-app/INSTALL.md) - Guide d'installation
- [desktop-app/QUICKSTART.md](./desktop-app/QUICKSTART.md) - 3 étapes

---

## 🎯 Quelle Interface Choisir?

### Choisis l'Extension Chrome si:
- ✅ Tu veux automatiser **uniquement le navigateur**
- ✅ Tu ne veux pas installer d'application
- ✅ Tu fais principalement du **web scraping/automation**

### Choisis l'App Desktop si:
- ✅ Tu veux contrôler **tout ton ordinateur**
- ✅ Tu veux un **raccourci global** (`Ctrl+Shift+A`)
- ✅ Tu veux lancer l'agent **au démarrage**
- ✅ Tu veux **distribuer facilement** l'app (.exe)
- ✅ Tu veux automatiser **LinkedIn + autres apps**

**Recommandation**: 🏆 **Desktop App** pour une expérience complète!

---

## 🔧 Architecture Commune

Les deux interfaces partagent la même architecture:

```
┌─────────────────┐
│  UI (Frontend)  │ ← Extension Chrome OU Desktop App
└────────┬────────┘
         │ WebSocket
         ↓
┌─────────────────┐
│  Backend API    │ ← FastAPI + WebSocket
│  (Port 8000)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Agent S3      │ ← Claude Sonnet 4.5 + Fara-7B
│  (Azure AI)     │
└─────────────────┘
         │
         ↓
┌─────────────────┐
│  Your Computer  │ ← Actions exécutées
└─────────────────┘
```

### Composants

1. **UI Frontend**: Chrome extension OU Electron app
2. **Backend API**: `backend/main.py` (FastAPI + WebSocket)
3. **Agent S3**: Reasoning (Claude) + Grounding (Fara-7B)
4. **Exécution**: Contrôle souris/clavier/écran

---

## 🚀 Démarrage Rapide

### 1. Lancer le Backend

```bash
# À la racine du projet
python backend/main.py
```

Backend démarre sur `http://localhost:8000`

### 2a. Extension Chrome

```bash
# Charger l'extension dans Chrome
chrome://extensions/
→ Mode développeur
→ Charger extension non empaquetée
→ Sélectionner dossier "extension/"
```

### 2b. Desktop App

```bash
cd desktop-app
npm install
npm start
```

Ou double-clic sur `launch.bat`

### 3. Tester

Dans l'interface (extension ou app):
```
Va sur google.com
```

**Ça marche!** 🎉

---

## 📝 LinkedIn Automation

Les deux interfaces supportent l'automation LinkedIn!

### Guides

- [LINKEDIN_GUIDE.md](./LINKEDIN_GUIDE.md) - Guide complet LinkedIn
- [linkedin_profiles.json](./linkedin_profiles.json) - Profils pré-configurés

### Exemples de Commandes

```
"Like 5 posts sur LinkedIn"
"Connecte-toi avec 10 développeurs Python"
"Commente 3 posts sur l'IA"
"Cherche des CTOs en tech et visite leurs profils"
```

---

## 🎨 Design

Les deux interfaces utilisent le même design **shadcn/ui**:

- ⚫ Background noir
- 🔵 Accent bleu (primary)
- 📦 Messages avec cards
- ⌨️ Input avec focus ring
- 🎯 Badges de statut
- ⚡ Animations smooth

### Variables CSS

```css
--background: 0 0% 0%;        /* Noir */
--primary: 217 91% 60%;       /* Bleu */
--foreground: 0 0% 98%;       /* Blanc */
--border: 0 0% 14.9%;         /* Gris foncé */
```

---

## 📦 Build & Distribution

### Extension Chrome

```bash
# Zip le dossier extension/
zip -r agent-s3-extension.zip extension/
```

Distribue le `.zip` ou publie sur Chrome Web Store.

### Desktop App

```bash
cd desktop-app

# Windows
npm run build:win
→ dist/Agent-S3-Setup.exe

# macOS
npm run build:mac
→ dist/Agent-S3.dmg

# Linux
npm run build:linux
→ dist/Agent-S3.AppImage
```

---

## 🔐 Sécurité

⚠️ **Important**: Agent S3 contrôle ton ordinateur!

- ✅ Utilise des APIs Azure sécurisées
- ✅ WebSocket local (localhost:8000)
- ✅ Pas de données envoyées en externe (sauf Azure AI)
- ⚠️ L'agent exécute du code Python
- ⚠️ Vérifie toujours les actions avant de confirmer

### Bonnes Pratiques

1. Lance le backend **localement** uniquement
2. Ne partage PAS tes clés API Azure
3. Vérifie les actions de l'agent
4. Utilise dans un environnement de test d'abord
5. Respecte les limites LinkedIn (anti-spam)

---

## 🤝 Support

- **Issues**: https://github.com/simular-ai/Agent-S/issues
- **Discord**: https://discord.gg/E2XfsK9fPV
- **Docs**: Lis les README dans chaque dossier

---

## 📚 Documentation Complète

### Extension Chrome
- [extension/README.md](./extension/README.md)

### Desktop App
- [desktop-app/START_HERE.md](./desktop-app/START_HERE.md) 🚀
- [desktop-app/README.md](./desktop-app/README.md)
- [desktop-app/INSTALL.md](./desktop-app/INSTALL.md)
- [desktop-app/QUICKSTART.md](./desktop-app/QUICKSTART.md)

### LinkedIn
- [LINKEDIN_GUIDE.md](./LINKEDIN_GUIDE.md)
- [linkedin_profiles.json](./linkedin_profiles.json)

### Backend
- [README.md](./README.md) - README principal Agent S

---

**Prêt à commencer?** 🚀

→ Extension Chrome: Charge dans `chrome://extensions/`
→ Desktop App: `cd desktop-app && npm start`

Enjoy Agent S3! 🤖
