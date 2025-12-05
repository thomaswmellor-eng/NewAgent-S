# ☁️ Guide: Déployer le Backend Flemme sur Azure App Service

## 📋 Prérequis

- ✅ Compte Azure (gratuit: https://azure.microsoft.com/free/)
- ✅ Azure CLI installé (https://docs.microsoft.com/cli/azure/install-azure-cli)
- ✅ Le dossier `backend/` de votre projet

---

## 🗂️ Étape 1: Préparer le Dossier Backend

### Créer requirements.txt

Si vous n'avez pas encore de `requirements.txt`, créez-le:

```bash
cd backend
pip freeze > requirements.txt
```

**Ou créez manuellement avec les dépendances essentielles:**

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
websockets==12.0
pyautogui==0.9.54
Pillow==10.1.0
anthropic==0.7.7
openai==1.3.5
httpx==0.25.1
pydantic==2.5.0
```

### Structure du Dossier à Déployer

```
backend/
├── main.py
├── agent_runner.py
├── requirements.txt  ← IMPORTANT!
├── gui_agents/
│   └── s3/
│       └── agents/
│           ├── __init__.py
│           ├── agent_s.py
│           ├── grounding.py
│           ├── worker.py
│           └── procedural_memory.py
├── .gitignore  (ajouter .env)
└── (PAS de .env - on configure sur Azure)
```

---

## ☁️ Étape 2: Créer l'App Service sur Azure

### Option A: Via le Portail Azure (Interface Web) - FACILE

1. **Allez sur** https://portal.azure.com
2. **Cliquez** sur "Create a resource"
3. **Cherchez** "Web App" → Click "Create"

**Configuration:**

| Paramètre | Valeur |
|-----------|--------|
| **Subscription** | Votre abonnement |
| **Resource Group** | Créer nouveau: `flemme-rg` |
| **Name** | `flemme-backend` (doit être unique) |
| **Publish** | Code |
| **Runtime stack** | Python 3.12 |
| **Region** | West Europe (ou proche de vous) |
| **Pricing plan** | B1 Basic (~13€/mois) |

4. **Cliquez** "Review + Create" → "Create"
5. **Attendez** 2-3 minutes que la ressource soit créée

---

### Option B: Via Azure CLI (Plus Rapide)

```bash
# 1. Se connecter à Azure
az login

# 2. Créer un groupe de ressources
az group create --name flemme-rg --location westeurope

# 3. Créer un plan App Service
az appservice plan create \
  --name flemme-plan \
  --resource-group flemme-rg \
  --sku B1 \
  --is-linux

# 4. Créer la Web App
az webapp create \
  --name flemme-backend \
  --resource-group flemme-rg \
  --plan flemme-plan \
  --runtime "PYTHON:3.12"
```

**Résultat:** Votre app sera accessible à `https://flemme-backend.azurewebsites.net`

---

## 🔑 Étape 3: Configurer les Variables d'Environnement

**⚠️ IMPORTANT:** Ne JAMAIS déployer le fichier `.env` sur Azure!

### Via le Portail Azure

1. **Allez** sur https://portal.azure.com
2. **Ouvrez** votre Web App `flemme-backend`
3. **Menu de gauche** → Settings → **Configuration**
4. **Cliquez** "New application setting"
5. **Ajoutez** chaque variable du `.env`:

| Name | Value |
|------|-------|
| `AZURE_OPENAI_NAME` | votre-modele-claude |
| `AZURE_OPENAI_ENDPOINT` | https://votre-endpoint.openai.azure.com/ |
| `AZURE_OPENAI_API_KEY` | votre-clé-api |
| `OPENAI_API_VERSION` | 2024-08-01-preview |
| `AZURE_FARA_NAME` | votre-modele-fara |
| `AZURE_FARA_ENDPOINT` | https://votre-fara-endpoint/ |
| `AZURE_FARA_API_KEY` | votre-clé-fara |
| `GROUNDING_WIDTH` | 1920 |
| `GROUNDING_HEIGHT` | 1080 |
| `AZURE_TASK_PLANNER_NAME` | votre-gpt4 |
| `AZURE_TASK_PLANNER_ENDPOINT` | https://votre-endpoint/ |
| `AZURE_TASK_PLANNER_API_KEY` | votre-clé |

6. **Cliquez** "Save" en haut

### Via Azure CLI

```bash
az webapp config appsettings set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --settings \
    AZURE_OPENAI_NAME="votre-modele" \
    AZURE_OPENAI_ENDPOINT="https://..." \
    AZURE_OPENAI_API_KEY="votre-clé" \
    OPENAI_API_VERSION="2024-08-01-preview" \
    AZURE_FARA_NAME="..." \
    AZURE_FARA_ENDPOINT="..." \
    AZURE_FARA_API_KEY="..." \
    GROUNDING_WIDTH="1920" \
    GROUNDING_HEIGHT="1080" \
    AZURE_TASK_PLANNER_NAME="..." \
    AZURE_TASK_PLANNER_ENDPOINT="..." \
    AZURE_TASK_PLANNER_API_KEY="..."
```

---

## 📤 Étape 4: Déployer le Code

### Méthode 1: Déploiement Local (Azure CLI)

```bash
cd backend

# Déployer depuis le dossier local
az webapp up \
  --name flemme-backend \
  --resource-group flemme-rg \
  --runtime "PYTHON:3.12"
```

**Durée:** 3-5 minutes

---

### Méthode 2: Via GitHub Actions (Déploiement Automatique)

**Avantages:** Déploiement automatique à chaque push

1. **Créer un repo GitHub:**
```bash
cd ..  # Racine du projet Agent-S
git init
git add backend/
git commit -m "Initial backend commit"
git remote add origin https://github.com/votre-username/flemme-backend.git
git push -u origin main
```

2. **Configurer le déploiement GitHub sur Azure:**
```bash
az webapp deployment source config \
  --name flemme-backend \
  --resource-group flemme-rg \
  --repo-url https://github.com/votre-username/flemme-backend \
  --branch main \
  --manual-integration
```

3. **Créer GitHub Actions workflow:**

Créez `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches:
      - main
    paths:
      - 'backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'flemme-backend'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: ./backend
```

4. **Obtenir le profil de publication:**
   - Portail Azure → Votre Web App → "Download publish profile"
   - GitHub → Settings → Secrets → New secret
   - Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Value: Collez le contenu du fichier XML

---

### Méthode 3: Déploiement ZIP (Simple)

```bash
cd backend

# Créer une archive
zip -r backend.zip . -x "*.pyc" -x "__pycache__/*" -x ".env"

# Déployer
az webapp deployment source config-zip \
  --name flemme-backend \
  --resource-group flemme-rg \
  --src backend.zip
```

---

## 🔧 Étape 5: Configurer le Startup Command

Azure doit savoir comment lancer votre app FastAPI.

### Via le Portail Azure

1. **Allez** sur votre Web App
2. **Configuration** → General settings
3. **Startup Command:**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
4. **Save**

### Via Azure CLI

```bash
az webapp config set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --startup-file "python -m uvicorn main:app --host 0.0.0.0 --port 8000"
```

---

## ✅ Étape 6: Vérifier le Déploiement

### Tester l'API

```bash
# Tester que le serveur répond
curl https://flemme-backend.azurewebsites.net/

# Devrait retourner: {"message": "Flemme Backend API"}
```

### Voir les Logs

**Via le Portail:**
1. Web App → Monitoring → **Log stream**
2. Voir les logs en temps réel

**Via CLI:**
```bash
az webapp log tail \
  --name flemme-backend \
  --resource-group flemme-rg
```

---

## 🔒 Étape 7: Sécuriser l'API

### Ajouter une API Key

**Modifier `backend/main.py`:**

```python
from fastapi import FastAPI, WebSocket, Header, HTTPException
import os

app = FastAPI()

# Clé API pour authentification
API_KEY = os.getenv("FLEMME_API_KEY", "votre-clé-secrète-changez-moi")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.websocket("/ws/agent")
async def websocket_agent(
    websocket: WebSocket,
    x_api_key: str = Header(...)
):
    # Vérifier l'API key
    try:
        await verify_api_key(x_api_key)
    except HTTPException:
        await websocket.close(code=1008)  # Policy Violation
        return

    await websocket.accept()
    # ... reste du code
```

**Ajouter la variable sur Azure:**
```bash
az webapp config appsettings set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --settings FLEMME_API_KEY="votre-clé-super-secrète-unique"
```

---

## 🖥️ Étape 8: Modifier l'App Desktop

Maintenant que le backend est hébergé, modifiez l'app desktop pour pointer vers Azure:

### Modifier `desktop-app/renderer/app.js`

```javascript
// Configuration
let config = {
    apiUrl: 'https://flemme-backend.azurewebsites.net',  // Votre backend Azure
    enableReflection: true,
    ws: null
};

// Connexion WebSocket avec API Key
function connectWebSocket() {
    const wsUrl = config.apiUrl.replace('https', 'wss').replace('http', 'ws');

    // Note: WebSocket headers ne fonctionnent pas dans le navigateur
    // On va passer l'API key via query parameter
    config.ws = new WebSocket(`${wsUrl}/ws/agent?api_key=votre-clé-api`);

    // ... reste du code
}
```

### Modifier `backend/main.py` pour accepter API key via query param

```python
@app.websocket("/ws/agent")
async def websocket_agent(
    websocket: WebSocket,
    api_key: str = Query(None)  # API key via query parameter
):
    # Vérifier l'API key
    if api_key != API_KEY:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    # ... reste du code
```

### Supprimer le Code de Backend Bundlé

**Modifier `desktop-app/main.js`:**

```javascript
// Commenter ou supprimer ces fonctions
/*
function startBackend() { ... }
function stopBackend() { ... }
*/

// Initialisation de l'app
app.whenReady().then(() => {
    // NE PAS démarrer le backend
    // startBackend();  ← Commenter

    // Pas besoin d'attendre - backend déjà sur Azure
    createWindow();
    createTray();
    setLoginItemSettings();

    // ... reste du code
});
```

### Rebuild l'App Desktop

```bash
cd desktop-app
npm run build:win -- --config electron-builder.yml
```

**Résultat:** Installateur beaucoup plus léger (~70 MB au lieu de 134 MB)!

---

## 💰 Coûts Azure

### Plan B1 Basic (Recommandé)

| Ressource | Prix |
|-----------|------|
| App Service B1 | ~13€/mois |
| Bande passante sortante | ~0.05€/GB |
| **Total estimé** | **15-20€/mois** |

### Réduire les Coûts

**Plan F1 Free (Gratuit):**
- 60 minutes CPU/jour
- 1 GB RAM
- 1 GB stockage
- **Limitations:** App s'arrête après inactivité

```bash
# Passer au plan gratuit
az appservice plan update \
  --name flemme-plan \
  --resource-group flemme-rg \
  --sku F1
```

⚠️ **Attention:** Le plan gratuit a des limitations strictes - pas idéal pour production.

---

## 🔄 Mises à Jour

### Redéployer après Modifications

```bash
cd backend
az webapp up \
  --name flemme-backend \
  --resource-group flemme-rg
```

Ou avec GitHub Actions: juste `git push` → déploiement automatique!

---

## 🐛 Troubleshooting

### Le Backend ne Démarre Pas

**Vérifier les logs:**
```bash
az webapp log tail --name flemme-backend --resource-group flemme-rg
```

**Erreurs communes:**
- `ModuleNotFoundError`: Vérifier `requirements.txt`
- `Port already in use`: Utiliser `--port 8000` dans startup command
- `Environment variable not found`: Vérifier Configuration → Application settings

### WebSocket Connection Failed

**Vérifier:**
1. URL correcte: `wss://` (pas `ws://`)
2. Port 8000 ou défaut (Azure gère)
3. API key correcte
4. CORS configuré dans FastAPI

**Ajouter CORS si nécessaire:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production: liste spécifique
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Timeout / Slow Response

**Augmenter le plan:**
```bash
az appservice plan update \
  --name flemme-plan \
  --resource-group flemme-rg \
  --sku B2  # Plus de RAM/CPU
```

---

## 📊 Monitoring

### Activer Application Insights

```bash
az monitor app-insights component create \
  --app flemme-insights \
  --location westeurope \
  --resource-group flemme-rg

# Connecter à la Web App
az webapp config appsettings set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --settings APPLICATIONINSIGHTS_CONNECTION_STRING="..."
```

### Métriques Importantes

- **Response time:** Temps de réponse API
- **Failed requests:** Requêtes échouées
- **CPU usage:** Utilisation CPU
- **Memory usage:** Utilisation mémoire

---

## ✅ Checklist de Déploiement

- [ ] Compte Azure créé
- [ ] `requirements.txt` créé
- [ ] App Service créée sur Azure
- [ ] Variables d'environnement configurées (sans .env!)
- [ ] Startup command configuré
- [ ] Code déployé via CLI/GitHub/ZIP
- [ ] Backend accessible via URL
- [ ] Logs vérifiés (pas d'erreurs)
- [ ] API Key configurée pour sécurité
- [ ] Desktop app modifiée pour pointer vers Azure
- [ ] Backend bundlé retiré de l'app desktop
- [ ] Nouveau build créé et testé

---

## 🎉 Résultat Final

**Avant (Backend Bundlé):**
- ❌ Clés API exposées dans l'installateur
- ❌ 134 MB d'installateur
- ❌ Risque de coûts incontrôlés

**Après (Backend Azure):**
- ✅ Clés API sécurisées sur Azure
- ✅ 70 MB d'installateur
- ✅ Contrôle total de l'accès
- ✅ Monitoring et logs centralisés
- ✅ Mises à jour backend sans redistribuer l'app

---

**Votre backend Flemme est maintenant prêt pour la production! 🚀**
