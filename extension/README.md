# 🚀 Agent S3 Browser Extension

Extension de navigateur minimaliste pour contrôler Agent S3 depuis votre navigateur.

## 📋 Installation (Mode Développement)

### 1. Lancer le Backend

```powershell
# Activer l'environnement virtuel Python 3.12
.\.venv312\Scripts\Activate.ps1

# Aller dans le dossier backend
cd backend

# Installer les dépendances
pip install fastapi uvicorn websockets python-dotenv

# Lancer l'API
python main.py
```

Le serveur démarrera sur `http://localhost:8000`

### 2. Charger l'Extension dans Chrome/Edge

1. **Ouvrez Chrome ou Edge**

2. **Accédez aux extensions:**
   - Chrome: `chrome://extensions`
   - Edge: `edge://extensions`

3. **Activez le "Mode développeur"** (toggle en haut à droite)

4. **Cliquez sur "Charger l'extension non empaquetée"**

5. **Sélectionnez le dossier:** `C:\Users\tom\Agent-S\extension`

6. **L'extension apparaît!**
   - Épinglez-la dans la barre d'outils (icône puzzle)

### 3. Tester l'Extension

1. **Cliquez sur l'icône de l'extension** dans la barre d'outils

2. **La popup s'ouvre** avec l'interface minimaliste

3. **Tapez une commande**, par exemple:
   ```
   Ouvrir le bloc-notes
   ```

4. **Observez** la réflexion de l'agent et l'exécution en temps réel!

---

## 🎨 Interface

L'interface est **minimaliste, transparente, noir/gris** comme demandé:

- 🎯 **Input en bas** pour taper vos commandes
- 💬 **Chat au centre** qui affiche:
  - Vos messages (bleu)
  - Les réflexions de l'agent (orange)
  - Les actions (violet)
  - Les succès (vert)
  - Les erreurs (rouge)
- ⚙️ **Settings** (icône engrenage) pour configurer l'URL de l'API

---

## 🔧 Configuration

Cliquez sur l'icône ⚙️ pour ouvrir les paramètres:

- **URL de l'API**: Par défaut `http://localhost:8000`
- **Activer la réflexion**: Afficher les pensées de l'agent

---

## 📡 Communication avec le Backend

L'extension communique avec le backend via **WebSocket** pour du streaming en temps réel:

```
Extension (WebSocket) ←→ Backend API (FastAPI) ←→ Agent S3
```

**Avantages:**
- ✅ Streaming en temps réel de la réflexion
- ✅ Pas de polling
- ✅ Connexion persistante
- ✅ Mise à jour instantanée de l'UI

---

## 🧪 Exemples de Commandes

Essayez ces commandes:

### Navigation
```
Ouvrir Chrome et aller sur google.com
Ouvrir le menu démarrer
Rechercher "calculatrice" et l'ouvrir
```

### Automation
```
Ouvrir le bloc-notes et écrire "Hello World"
Créer un nouveau fichier Excel
Fermer toutes les fenêtres Chrome
```

### LinkedIn (votre use case!)
```
Aller sur LinkedIn et rechercher "Python Developer"
Ouvrir mon profil LinkedIn
Scroller dans le feed LinkedIn
```

---

## 🔒 Sécurité

⚠️ **Important:**

- L'extension communique avec `localhost:8000` par défaut
- En production, utilisez **HTTPS** et **authentification**
- Ne partagez jamais vos clés API dans l'extension

---

## 🛠️ Développement

### Structure des Fichiers

```
extension/
├── manifest.json     # Configuration de l'extension
├── popup.html        # Interface utilisateur
├── popup.js          # Logic de l'UI et WebSocket
├── styles.css        # Styles minimalistes
├── background.js     # Service worker
└── icons/            # Icônes (à créer)
```

### Rechargement à Chaud

Quand vous modifiez le code:

1. **Backend:** Redémarrez `python main.py` (ou utilisez `uvicorn --reload`)
2. **Extension:** Cliquez sur le bouton refresh dans `chrome://extensions`

---

## 📦 Publication (Future)

Pour publier sur le Chrome Web Store:

1. Créez les icônes manquantes (16x16, 48x48, 128x128)
2. Compressez le dossier `extension/` en `.zip`
3. Créez un compte développeur Chrome ($5 unique)
4. Soumettez l'extension
5. Attendez la review (~2-3 jours)

---

## 🐛 Résolution de Problèmes

### L'extension ne se connecte pas

1. Vérifiez que le backend est lancé: http://localhost:8000/health
2. Vérifiez les logs dans la console de l'extension (F12 dans la popup)
3. Vérifiez que le WebSocket est autorisé (pas de bloqueur)

### Les actions ne s'exécutent pas

1. Vérifiez que Agent S3 est correctement configuré (`.env`)
2. Vérifiez les logs du backend
3. Vérifiez que PyAutoGUI a les permissions

### L'UI ne s'affiche pas correctement

1. Rechargez l'extension
2. Vérifiez la console pour les erreurs
3. Assurez-vous que `styles.css` est bien chargé

---

## 🚀 Prochaines Étapes

- [ ] Ajouter les icônes manquantes
- [ ] Implémenter l'authentification
- [ ] Ajouter un historique des commandes
- [ ] Implémenter la gestion de session
- [ ] Ajouter des raccourcis clavier
- [ ] Mode sombre/clair (actuellement sombre uniquement)

---

**Bon développement! 🎉**
