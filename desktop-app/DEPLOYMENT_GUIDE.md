# 📦 Guide de Déploiement - Flemme Desktop App

Guide complet pour créer des installateurs multi-plateformes et les distribuer aux utilisateurs.

---

## 🚨 ATTENTION: Backend URL Configuration

**PROBLÈME CRITIQUE:** L'app est actuellement configurée avec `localhost:8000` hardcodé dans le code.

```javascript
// desktop-app/renderer/app.js
let config = {
    apiUrl: 'http://localhost:8000',  // ⚠️ NE FONCTIONNERA PAS pour les utilisateurs!
    // ...
};
```

### Solutions possibles:

#### **Option 1: Backend local inclus (Recommandé pour simplicité)**

Bundler le backend Python avec l'app Electron.

**Avantages:**
- Installation simple pour l'utilisateur
- Tout fonctionne out-of-the-box
- Pas besoin de configuration

**Inconvénients:**
- Installateur plus lourd (~500MB avec Python)
- Plus complexe à configurer

**Implémentation:** Voir section "Bundle Backend avec l'App" ci-dessous.

---

#### **Option 2: Backend hébergé centralement**

Héberger le backend sur un serveur cloud et pointer toutes les apps vers cette URL.

**Avantages:**
- Installateur léger
- Mises à jour backend faciles
- Contrôle centralisé

**Inconvénients:**
- Coûts d'hébergement (Azure, AWS)
- Latence réseau
- Tous les utilisateurs partagent les ressources
- Besoin d'authentification/rate limiting

**Implémentation:**
```javascript
// Changer dans renderer/app.js
let config = {
    apiUrl: 'https://flemme-api.votredomaine.com',  // Votre serveur backend
};
```

**Backend hosting:**
- Azure App Service (recommandé car vous utilisez Azure AI)
- AWS Elastic Beanstalk
- DigitalOcean App Platform
- Google Cloud Run

---

#### **Option 3: Backend installé séparément**

L'utilisateur installe l'app + lance le backend manuellement.

**Avantages:**
- Contrôle total
- Pas de coûts cloud

**Inconvénients:**
- **Expérience utilisateur HORRIBLE**
- Installation complexe (Python, dépendances, .env)
- Support difficile

**NON RECOMMANDÉ pour distribution publique.**

---

## 🛠️ Prérequis

### Sur votre machine de build:

- **Node.js** >= 18.x
- **npm** >= 9.x
- **Python** 3.12 (si vous bundlez le backend)

### Pour build multi-plateforme:

- **Windows:** Build sur Windows ou utilisez VM/Docker
- **macOS:** Build sur macOS (signature requise pour distribution)
- **Linux:** Build sur n'importe quelle plateforme

---

## 📋 Étapes de Déploiement

### 1. Préparer le Projet

```bash
cd desktop-app
npm install
```

### 2. Configurer le Backend URL

**Décidez quelle option vous voulez (voir section précédente)**, puis éditez:

```javascript
// desktop-app/renderer/app.js
let config = {
    apiUrl: 'VOTRE_URL_ICI',  // Changez selon votre choix
    enableReflection: true,
    ws: null
};
```

### 3. Tester en Local

Avant de builder, testez que tout fonctionne:

```bash
# Terminal 1: Backend
cd ..
.\.venv312\Scripts\python.exe backend\main.py

# Terminal 2: Desktop app
cd desktop-app
npm start
```

Testez:
- Connexion WebSocket
- Exécution d'une tâche
- Bouton Stop
- Raccourci clavier Ctrl+Shift+A

### 4. Vérifier les Icônes

Assurez-vous que les 3 fichiers d'icônes existent:

```
desktop-app/
  assets/
    icon.png   (512x512 - Linux)
    icon.ico   (Multi-res - Windows)
    icon.icns  (Multi-res - macOS)
```

Si besoin, consultez [CHANGER_ICONES.md](./CHANGER_ICONES.md).

---

## 🏗️ Build par Plateforme

### Windows (.exe)

```bash
cd desktop-app
npm run build:win
```

**Sortie:**
```
dist/
  Flemme-Setup-1.0.0.exe  (~70MB sans backend, ~500MB avec backend)
```

**Installateur NSIS:**
- Installation guidée
- Choix du répertoire
- Raccourci bureau
- Raccourci menu démarrer
- Désinstalleur inclus

**Tester:**
- Double-cliquez sur `Flemme-Setup-1.0.0.exe`
- Suivez l'installation
- Lancez l'app depuis le menu démarrer
- Vérifiez le system tray

---

### macOS (.dmg)

```bash
cd desktop-app
npm run build:mac
```

**Sortie:**
```
dist/
  Flemme-1.0.0.dmg  (~70MB sans backend)
```

**⚠️ Signature de code requise pour distribution:**

Sans signature, les utilisateurs verront:
> "Flemme can't be opened because it is from an unidentified developer"

**Pour signer l'app:**

1. **Obtenez un Apple Developer Account** ($99/an)
2. **Créez des certificats:**
   ```bash
   # Developer ID Application certificate
   # Developer ID Installer certificate
   ```
3. **Configurez electron-builder:**
   ```json
   // package.json
   "build": {
     "mac": {
       "identity": "Developer ID Application: Votre Nom (TEAM_ID)",
       "hardenedRuntime": true,
       "gatekeeperAssess": false,
       "entitlements": "build/entitlements.mac.plist",
       "entitlementsInherit": "build/entitlements.mac.plist"
     }
   }
   ```
4. **Notarize l'app** (requis pour macOS 10.15+)

**Workaround pour tests (NON pour distribution):**
```bash
# L'utilisateur doit faire clic-droit > Ouvrir la première fois
# Ou désactiver Gatekeeper (dangereux):
sudo spctl --master-disable
```

---

### Linux (.AppImage)

```bash
cd desktop-app
npm run build:linux
```

**Sortie:**
```
dist/
  Flemme-1.0.0.AppImage  (~80MB sans backend)
```

**AppImage = portable:**
- Pas d'installation requise
- Lancé directement
- Fonctionne sur Ubuntu, Fedora, Arch, etc.

**Tester:**
```bash
chmod +x dist/Flemme-1.0.0.AppImage
./dist/Flemme-1.0.0.AppImage
```

---

## 🎁 Bundle Backend avec l'App (Option 1)

Pour que l'app fonctionne sans serveur externe, bundlez Python + backend.

### Étape 1: Installer PyInstaller

```bash
cd ..
.\.venv312\Scripts\python.exe -m pip install pyinstaller
```

### Étape 2: Créer un Executable Python

```bash
cd backend
pyinstaller --onefile \
  --add-data "../.env;." \
  --hidden-import "gui_agents.s3.agents.agent_s" \
  --hidden-import "gui_agents.s3.agents.grounding" \
  --hidden-import "gui_agents.s3.agents.worker" \
  main.py
```

**Sortie:**
```
backend/dist/main.exe  (~50MB + modèles AI = ~400MB)
```

### Étape 3: Intégrer dans Electron

```javascript
// desktop-app/main.js - Ajouter au démarrage

const { spawn } = require('child_process');
const path = require('path');

// Démarrer le backend au lancement de l'app
let backendProcess;

function startBackend() {
    const backendPath = path.join(
        process.resourcesPath,  // Chemin des ressources Electron
        'backend',
        'main.exe'  // Ou 'main' sur Linux/Mac
    );

    console.log('🚀 Démarrage du backend:', backendPath);

    backendProcess = spawn(backendPath, [], {
        stdio: 'ignore',  // Pas de logs
        detached: false
    });

    backendProcess.on('error', (err) => {
        console.error('❌ Erreur backend:', err);
        dialog.showErrorBox(
            'Erreur de démarrage',
            'Le backend n\'a pas pu démarrer. Veuillez réinstaller l\'application.'
        );
    });
}

// Lancer au démarrage
app.whenReady().then(() => {
    startBackend();

    // Attendre 2 secondes que le backend démarre
    setTimeout(() => {
        createWindow();
        createTray();
    }, 2000);
});

// Nettoyer à la fermeture
app.on('before-quit', () => {
    if (backendProcess) {
        backendProcess.kill();
    }
});
```

### Étape 4: Copier Backend dans Build

```json
// desktop-app/package.json
{
  "build": {
    "files": [
      "main.js",
      "preload.js",
      "renderer/**/*",
      "assets/**/*"
    ],
    "extraResources": [
      {
        "from": "../backend/dist/main.exe",
        "to": "backend/main.exe"
      },
      {
        "from": "../.env",
        "to": "backend/.env"
      }
    ]
  }
}
```

### Étape 5: Update apiUrl

```javascript
// desktop-app/renderer/app.js
let config = {
    apiUrl: 'http://localhost:8000',  // Backend local bundlé
    // ...
};
```

### Étape 6: Build

```bash
cd desktop-app
npm run build:win
```

**Installateur final:**
- `Flemme-Setup-1.0.0.exe` (~500MB)
- Inclut Python + Backend + Dependencies
- Fonctionne standalone

---

## 🌐 Héberger Backend sur Azure (Option 2)

### Prérequis

- Compte Azure
- Azure CLI installé

### Étape 1: Créer une Web App

```bash
az login
az group create --name flemme-rg --location westeurope
az appservice plan create \
  --name flemme-plan \
  --resource-group flemme-rg \
  --sku B1 \
  --is-linux

az webapp create \
  --name flemme-backend \
  --resource-group flemme-rg \
  --plan flemme-plan \
  --runtime "PYTHON:3.12"
```

### Étape 2: Configurer les Variables

```bash
az webapp config appsettings set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --settings \
    AZURE_OPENAI_NAME="votre-modele" \
    AZURE_OPENAI_ENDPOINT="https://..." \
    AZURE_OPENAI_API_KEY="votre-clé" \
    # ... toutes les vars de .env
```

### Étape 3: Déployer le Backend

```bash
cd backend
az webapp up \
  --name flemme-backend \
  --resource-group flemme-rg \
  --runtime "PYTHON:3.12"
```

**URL publique:**
```
https://flemme-backend.azurewebsites.net
```

### Étape 4: Update Frontend

```javascript
// desktop-app/renderer/app.js
let config = {
    apiUrl: 'https://flemme-backend.azurewebsites.net',
    // ...
};
```

### Étape 5: Sécurité (IMPORTANT!)

**Ajoutez authentification:**

```python
# backend/main.py
from fastapi import Header, HTTPException

API_KEY = os.getenv("FLEMME_API_KEY")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.websocket("/ws/agent")
async def websocket_agent(
    websocket: WebSocket,
    x_api_key: str = Header(...)
):
    await verify_api_key(x_api_key)
    # ... reste du code
```

```javascript
// desktop-app/renderer/app.js
config.ws = new WebSocket(`${wsUrl}/ws/agent`, {
    headers: {
        'X-API-Key': 'VOTRE_CLE_API'
    }
});
```

**Ajoutez rate limiting:**
```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.websocket("/ws/agent")
@limiter.limit("10/minute")  # Max 10 tâches par minute
async def websocket_agent(...):
    # ...
```

---

## 📤 Distribution des Installateurs

### Option 1: GitHub Releases (Gratuit)

1. **Créez un repo GitHub**
2. **Créez une release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. **Uploadez les builds:**
   - Allez sur GitHub > Releases > Draft new release
   - Uploadez:
     - `Flemme-Setup-1.0.0.exe` (Windows)
     - `Flemme-1.0.0.dmg` (macOS)
     - `Flemme-1.0.0.AppImage` (Linux)
   - Écrivez les release notes
   - Publiez

**Téléchargement:**
```
https://github.com/votre-username/flemme/releases/latest
```

---

### Option 2: Site Web Custom

Hébergez les fichiers sur votre propre serveur.

**Structure:**
```
votre-site.com/
  downloads/
    windows/
      Flemme-Setup-1.0.0.exe
    mac/
      Flemme-1.0.0.dmg
    linux/
      Flemme-1.0.0.AppImage
  index.html  (page de téléchargement)
```

**HTML exemple:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Télécharger Flemme</title>
</head>
<body>
    <h1>Flemme - AI Desktop Assistant</h1>

    <h2>Télécharger pour votre plateforme:</h2>

    <a href="/downloads/windows/Flemme-Setup-1.0.0.exe" class="download-btn">
        🪟 Windows (70MB)
    </a>

    <a href="/downloads/mac/Flemme-1.0.0.dmg" class="download-btn">
        🍎 macOS (70MB)
    </a>

    <a href="/downloads/linux/Flemme-1.0.0.AppImage" class="download-btn">
        🐧 Linux (80MB)
    </a>
</body>
</html>
```

**Hébergement:**
- **Netlify** (gratuit, simple)
- **Vercel** (gratuit)
- **AWS S3 + CloudFront**
- Votre propre serveur

---

### Option 3: CDN (Fichiers Lourds)

Pour des fichiers > 100MB, utilisez un CDN:

**Cloudflare R2 (Gratuit jusqu'à 10GB):**
```bash
# Upload via interface web ou API
# URL publique: https://pub-xxx.r2.dev/Flemme-Setup-1.0.0.exe
```

**AWS S3:**
```bash
aws s3 cp dist/Flemme-Setup-1.0.0.exe s3://flemme-downloads/windows/
aws s3 presign s3://flemme-downloads/windows/Flemme-Setup-1.0.0.exe
```

---

## 🔄 Auto-Updates (Bonus)

Electron supporte les mises à jour automatiques avec electron-updater.

### Configuration

```bash
npm install electron-updater
```

```javascript
// desktop-app/main.js
const { autoUpdater } = require('electron-updater');

app.whenReady().then(() => {
    // Vérifier les updates au démarrage
    autoUpdater.checkForUpdatesAndNotify();

    // Vérifier toutes les heures
    setInterval(() => {
        autoUpdater.checkForUpdatesAndNotify();
    }, 3600000);
});

autoUpdater.on('update-available', () => {
    dialog.showMessageBox({
        type: 'info',
        title: 'Mise à jour disponible',
        message: 'Une nouvelle version de Flemme est disponible. Téléchargement en cours...'
    });
});

autoUpdater.on('update-downloaded', () => {
    dialog.showMessageBox({
        type: 'info',
        title: 'Mise à jour prête',
        message: 'La mise à jour sera installée au prochain démarrage.',
        buttons: ['Redémarrer maintenant', 'Plus tard']
    }).then((result) => {
        if (result.response === 0) {
            autoUpdater.quitAndInstall();
        }
    });
});
```

### Héberger les Updates

```json
// package.json
{
  "build": {
    "publish": {
      "provider": "github",
      "owner": "votre-username",
      "repo": "flemme"
    }
  }
}
```

ou

```json
{
  "build": {
    "publish": {
      "provider": "generic",
      "url": "https://votre-site.com/updates/"
    }
  }
}
```

---

## 📊 Checklist de Release

Avant de distribuer l'app:

- [ ] Backend URL configuré (bundlé ou hébergé)
- [ ] Variables d'environnement sécurisées
- [ ] Icônes personnalisées (icon.png, icon.ico, icon.icns)
- [ ] Version mise à jour dans package.json
- [ ] Tests sur chaque plateforme
- [ ] Raccourci clavier testé (Ctrl+Shift+A)
- [ ] System tray fonctionne
- [ ] WebSocket se reconnecte automatiquement
- [ ] Bouton Stop fonctionne
- [ ] Build Windows (.exe) créé
- [ ] Build macOS (.dmg) créé + signé
- [ ] Build Linux (.AppImage) créé
- [ ] README avec instructions d'installation
- [ ] Page de téléchargement créée
- [ ] Release notes écrites
- [ ] Fichiers uploadés (GitHub/S3/CDN)
- [ ] Auto-updates configuré (optionnel)

---

## 🐛 Problèmes Courants

### "App can't be opened" (macOS)

**Cause:** App non signée

**Solution temporaire:**
```bash
sudo xattr -r -d com.apple.quarantine /Applications/Flemme.app
```

**Solution permanente:** Signer l'app avec Apple Developer certificate.

---

### "Windows protected your PC"

**Cause:** App non signée avec certificat Windows

**Solution utilisateur:**
1. Cliquer "More info"
2. Cliquer "Run anyway"

**Solution permanente:** Acheter un code signing certificate (~$200/an)

---

### Backend ne démarre pas (bundlé)

**Vérifications:**
1. `backend/dist/main.exe` existe dans `process.resourcesPath`
2. Fichier `.env` copié avec le backend
3. Logs du backend visibles:
   ```javascript
   backendProcess = spawn(backendPath, [], {
       stdio: 'pipe'  // Au lieu de 'ignore'
   });
   backendProcess.stdout.on('data', (data) => {
       console.log('Backend:', data.toString());
   });
   ```

---

### WebSocket connection refused

**Vérifications:**
1. Backend est bien démarré (port 8000)
2. URL correcte dans `renderer/app.js`
3. Firewall ne bloque pas
4. CORS configuré dans backend

---

## 💰 Coûts Estimés

### Option 1: Backend Bundlé
- **Dev:** Gratuit
- **Distribution:** Gratuit (GitHub Releases)
- **Code Signing (optionnel):**
  - macOS: $99/an (Apple Developer)
  - Windows: $200/an (Code signing cert)

---

### Option 2: Backend Hébergé Azure
- **Azure App Service B1:** ~$13/mois
- **Azure OpenAI:** Pay-per-use (GPT-4 + embeddings)
- **Bande passante:** ~$0.05/GB
- **Total estimé:** $20-50/mois selon usage

---

### Option 3: Backend Auto-hébergé
- **VPS (DigitalOcean, Hetzner):** $5-20/mois
- **Domaine:** $10/an
- **SSL (Let's Encrypt):** Gratuit

---

## 📚 Ressources

- **Electron Builder:** https://www.electron.build/
- **electron-updater:** https://www.electron.build/auto-update
- **PyInstaller:** https://pyinstaller.org/
- **Azure App Service:** https://azure.microsoft.com/en-us/products/app-service
- **GitHub Releases:** https://docs.github.com/en/repositories/releasing-projects-on-github

---

## ✅ Prochaines Étapes

1. **Décider architecture backend** (bundlé vs hébergé)
2. **Configurer URL dans le code**
3. **Tester sur chaque plateforme**
4. **Créer les builds**
5. **Uploader sur GitHub/site web**
6. **Écrire documentation utilisateur**
7. **Annoncer la release!**

---

**Bonne chance avec le déploiement de Flemme! 🚀**
