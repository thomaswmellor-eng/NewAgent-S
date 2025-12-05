# ✅ Checklist de Déploiement Backend

## 📋 Structure Actuelle (Correcte)

```
backend/
├── main.py                    ✅
├── agent_runner.py            ✅
├── requirements.txt           ✅ (nettoyé)
├── .env                       ✅ (NE PAS déployer!)
├── .gitignore                 ✅ (créé)
├── gui_agents/                ✅ (dossier complet)
│   └── s3/
│       └── agents/
│           ├── __init__.py
│           ├── agent_s.py
│           ├── grounding.py
│           ├── worker.py
│           └── procedural_memory.py
└── DEPLOY_CHECKLIST.md        ✅ (ce fichier)
```

---

## ✅ Vérifications Faites

- [x] `gui_agents/` est dans `backend/`
- [x] `.env` est dans `backend/`
- [x] Tous les `__init__.py` sont présents
- [x] `requirements.txt` nettoyé (pas de référence GitHub)
- [x] Imports fonctionnent: `from gui_agents.s3.agents.agent_s import AgentS3`
- [x] `.gitignore` créé pour protéger `.env`

---

## 🚀 Prochaines Étapes

### 1. Tester Localement

```bash
cd backend
../.venv312/Scripts/python.exe main.py
```

Vérifier que le serveur démarre sans erreur.

---

### 2. Déployer sur Azure

**Option A: CLI (Plus rapide)**

```bash
# Se connecter à Azure
az login

# Déployer
cd backend
az webapp up --name flemme-backend --runtime "PYTHON:3.12" --sku B1
```

**Option B: Portail Web**
- https://portal.azure.com
- Create Resource → Web App
- Python 3.12
- Upload le dossier `backend/`

---

### 3. Configurer les Variables d'Environnement sur Azure

⚠️ **IMPORTANT:** Ne JAMAIS uploader le fichier `.env`!

**Via le Portail Azure:**
1. Aller sur votre Web App
2. Configuration → Application settings
3. Ajouter **CHAQUE** variable du `.env`:

```
AZURE_OPENAI_NAME=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
OPENAI_API_VERSION=...
AZURE_FARA_NAME=...
AZURE_FARA_ENDPOINT=...
AZURE_FARA_API_KEY=...
GROUNDING_WIDTH=1920
GROUNDING_HEIGHT=1080
AZURE_TASK_PLANNER_NAME=...
AZURE_TASK_PLANNER_ENDPOINT=...
AZURE_TASK_PLANNER_API_KEY=...
```

**Via CLI:**
```bash
az webapp config appsettings set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --settings \
    AZURE_OPENAI_NAME="..." \
    AZURE_OPENAI_ENDPOINT="..." \
    AZURE_OPENAI_API_KEY="..." \
    # ... (toutes les autres)
```

---

### 4. Configurer le Startup Command

```bash
az webapp config set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --startup-file "python -m uvicorn main:app --host 0.0.0.0 --port 8000"
```

---

### 5. Tester l'API Azure

```bash
curl https://flemme-backend.azurewebsites.net/
# Devrait retourner: {"message": "Flemme Backend API"}
```

---

### 6. Modifier l'App Desktop

**Fichier:** `desktop-app/renderer/app.js`

```javascript
// AVANT
let config = {
    apiUrl: 'http://localhost:8000',
    // ...
};

// APRÈS
let config = {
    apiUrl: 'https://flemme-backend.azurewebsites.net',
    // ...
};
```

---

### 7. Supprimer le Backend Bundlé de l'App Desktop

**Fichier:** `desktop-app/main.js`

Commenter les fonctions:
```javascript
/*
function startBackend() { ... }
function stopBackend() { ... }
*/

app.whenReady().then(() => {
    // startBackend();  ← Commenter
    // setTimeout(() => {  ← Remplacer par:

    createWindow();
    createTray();
    setLoginItemSettings();

    // ... reste du code
});
```

---

### 8. Mettre à Jour electron-builder.yml

**Retirer `extraResources`:**

```yaml
# SUPPRIMER ces lignes:
# extraResources:
#   - from: ../backend/dist/flemme-backend
#     to: backend/flemme-backend
#     filter: ["**/*"]
```

---

### 9. Rebuild l'App Desktop

```bash
cd desktop-app
npm run build:win -- --config electron-builder.yml
```

**Résultat attendu:**
- Installateur ~70 MB (au lieu de 134 MB)
- Pas de backend bundlé
- Se connecte à Azure

---

### 10. Tester l'App Complète

1. Installer le nouveau `Flemme Setup 1.0.0.exe`
2. Lancer l'app
3. Vérifier la connexion WebSocket à Azure
4. Tester une tâche simple: "Ouvre le Bloc-notes"
5. Vérifier les logs Azure pour voir les requêtes

---

## 🔒 Sécurité

### Ajouter une API Key (Recommandé)

**1. Modifier `backend/main.py`:**

```python
from fastapi import FastAPI, WebSocket, Query, HTTPException
import os

API_KEY = os.getenv("FLEMME_API_KEY", "changez-moi-en-production")

@app.websocket("/ws/agent")
async def websocket_agent(
    websocket: WebSocket,
    api_key: str = Query(None)
):
    # Vérifier l'API key
    if api_key != API_KEY:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    # ... reste du code
```

**2. Ajouter sur Azure:**

```bash
az webapp config appsettings set \
  --name flemme-backend \
  --resource-group flemme-rg \
  --settings FLEMME_API_KEY="votre-clé-super-secrète-123xyz"
```

**3. Modifier l'app desktop:**

```javascript
// desktop-app/renderer/app.js
const wsUrl = config.apiUrl.replace('https', 'wss').replace('http', 'ws');
config.ws = new WebSocket(`${wsUrl}/ws/agent?api_key=votre-clé-super-secrète-123xyz`);
```

---

## 📊 Vérification Finale

### Backend Azure
- [ ] Backend déployé et accessible
- [ ] Variables d'environnement configurées (sans .env!)
- [ ] Startup command configuré
- [ ] Logs montrent démarrage réussi
- [ ] API répond à `curl https://flemme-backend.azurewebsites.net/`

### App Desktop
- [ ] URL pointant vers Azure (pas localhost)
- [ ] Backend bundlé retiré
- [ ] Installateur ~70 MB (pas 134 MB)
- [ ] Connexion WebSocket réussie
- [ ] Tâche test exécutée correctement

### Sécurité
- [ ] `.env` JAMAIS commité dans Git
- [ ] API Key configurée (optionnel mais recommandé)
- [ ] Variables sensibles uniquement sur Azure

---

## 💰 Coût Estimé

**Azure App Service B1:**
- ~13€/mois
- 1.75 GB RAM
- 10 GB stockage
- Suffisant pour usage modéré

**Alternative gratuite (limitations):**
- Plan F1 Free
- 60 min CPU/jour
- App s'arrête après inactivité
- Pas idéal pour production

---

## 🐛 Troubleshooting

### Backend ne démarre pas
```bash
# Voir les logs
az webapp log tail --name flemme-backend --resource-group flemme-rg
```

### ModuleNotFoundError: gui_agents
→ Vérifier que `gui_agents/` est bien dans le dossier déployé
→ Vérifier les `__init__.py`

### Variables d'environnement manquantes
→ Vérifier Configuration → Application settings sur Azure
→ Ne PAS utiliser de `.env` sur Azure

### WebSocket connection failed
→ Vérifier l'URL: `wss://` (pas `ws://`)
→ Vérifier que l'API key est correcte
→ Vérifier les logs Azure

---

## ✅ Tout est Prêt!

Votre structure backend est **correcte** et **prête pour le déploiement**!

Prochaine étape: Déployer sur Azure avec la commande:

```bash
cd backend
az webapp up --name flemme-backend --runtime "PYTHON:3.12" --sku B1
```

Puis configurer les variables d'environnement sur le Portail Azure.

**Bon déploiement! 🚀**
