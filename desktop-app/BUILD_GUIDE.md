# 🔨 Guide de Build - Flemme avec Backend Bundlé

## ✅ Build Réussi!

Le build a été configuré avec succès pour inclure le backend Python dans l'app Electron.

---

## 📦 Ce qui est inclus

L'installateur **Flemme Setup 1.0.0.exe** (134MB) contient:
- ✅ Interface Electron (desktop-app)
- ✅ Backend FastAPI bundlé (flemme-backend.exe)
- ✅ Toutes les dépendances Python
- ✅ Configuration .env
- ✅ Agent S3 + Task Planner + Grounding
- ✅ Démarrage automatique du backend au lancement

---

## 🔧 Comment Builder

### 1. Builder le Backend (à refaire si vous modifiez le backend)

```bash
cd backend
../.venv312/Scripts/pyinstaller.exe flemme-backend.spec --clean
```

**Résultat:** `backend/dist/flemme-backend/flemme-backend.exe`

---

### 2. Builder l'App Electron

```bash
cd desktop-app
npm run build:win -- --config electron-builder.yml
```

**Résultat:**
- `desktop-app/dist/Flemme Setup 1.0.0.exe` (installateur)
- `desktop-app/dist/win-unpacked/` (version unpacked pour test)

---

## 🧪 Tester en Développement

### Option 1: Test avec backend séparé (rapide)

```bash
# Terminal 1: Backend
.venv312/Scripts/python.exe backend/main.py

# Terminal 2: Desktop app
cd desktop-app
npm start
```

---

### Option 2: Test avec backend bundlé (comme en production)

```bash
cd desktop-app
npm start
```

Le backend bundlé sera lancé automatiquement depuis `../backend/dist/flemme-backend/`

---

## 📋 Installation pour l'Utilisateur Final

1. **Télécharger** `Flemme Setup 1.0.0.exe`
2. **Double-cliquer** sur l'installateur
3. **Suivre** l'assistant d'installation
4. **Lancer** Flemme depuis le menu Démarrer ou le raccourci bureau
5. **Utiliser** Ctrl+Shift+A pour afficher/masquer la fenêtre

**Le backend démarre automatiquement en arrière-plan!**

---

## 🏗️ Architecture du Build

```
Flemme Setup 1.0.0.exe (134MB)
├── Installateur NSIS
└── Contenu installé dans Program Files/Flemme/
    ├── Flemme.exe (app Electron)
    ├── resources/
    │   ├── app.asar (code Electron)
    │   └── backend/
    │       └── flemme-backend/
    │           ├── flemme-backend.exe (FastAPI server)
    │           └── _internal/ (dépendances Python)
    └── ... (autres fichiers Electron)
```

---

## 🔍 Comment ça Fonctionne

### Au Démarrage

1. **Electron démarre** (main.js)
2. **startBackend()** lance `flemme-backend.exe`
3. **Attendre 3 secondes** que le backend démarre
4. **Créer la fenêtre** et se connecter via WebSocket à `localhost:8000`

### Pendant l'Exécution

- Backend tourne en arrière-plan (console cachée)
- Interface Electron communique via WebSocket
- Agent S3 exécute les tâches avec streaming

### À la Fermeture

- **stopBackend()** tue le processus backend
- Electron se ferme proprement

---

## 🐛 Troubleshooting

### Backend ne démarre pas

**Vérifier dans les logs Electron:**
```javascript
console.log('Backend:', data.toString());
```

**Causes possibles:**
- Fichier .env manquant
- Clés API Azure invalides
- Port 8000 déjà utilisé

**Solution:** Vérifier que `.env` est bien copié dans le build:
```bash
ls "desktop-app/dist/win-unpacked/resources/backend/flemme-backend/"
```

---

### "Cannot connect to backend"

Le backend met ~3 secondes à démarrer. Si le problème persiste:

1. Augmenter le timeout dans [main.js](c:\Users\tom\Agent-S\desktop-app\main.js:246):
   ```javascript
   setTimeout(() => {
       createWindow();
       // ...
   }, 5000);  // 5 secondes au lieu de 3
   ```

2. Vérifier que le backend est lancé:
   - Tâches Windows: chercher "flemme-backend.exe"

---

### Build échoue avec "Cannot create symbolic link"

**Solution:** Utiliser le fichier de config séparé:
```bash
npm run build:win -- --config electron-builder.yml
```

Le fichier `electron-builder.yml` désactive la signature de code qui cause le problème de symlinks.

---

## 📊 Taille des Fichiers

| Composant | Taille |
|-----------|--------|
| Backend executable | ~14 MB |
| Backend dependencies (_internal) | ~50 MB |
| Electron app | ~60 MB |
| **Total installateur** | **~134 MB** |

---

## 🚀 Distribution

Pour distribuer l'app:

1. **Upload** `Flemme Setup 1.0.0.exe` sur:
   - GitHub Releases (gratuit)
   - Votre site web
   - CDN (Cloudflare R2, AWS S3)

2. **Créer** une page de téléchargement:
   ```html
   <a href="/downloads/Flemme-Setup-1.0.0.exe">
       Télécharger Flemme pour Windows (134MB)
   </a>
   ```

3. **Avertir** les utilisateurs:
   > "Windows Defender peut afficher un avertissement car l'app n'est pas signée. Cliquez sur 'Plus d'infos' puis 'Exécuter quand même'."

---

## 🔐 Signature de Code (Optionnel)

Pour éviter les avertissements Windows Defender:

1. **Acheter** un certificat de signature de code (~$200/an)
2. **Configurer** electron-builder:
   ```yml
   win:
     certificateFile: path/to/cert.pfx
     certificatePassword: "votre_mot_de_passe"
   ```
3. **Builder** avec signature

---

## 📝 Notes Importantes

### Variables d'Environnement

Le fichier `.env` est **inclus dans le backend bundlé**.

⚠️ **ATTENTION:** Vos clés API Azure sont dans l'executable!

**Pour production:**
- Utiliser un backend hébergé séparément
- OU chiffrer les clés dans le build
- OU demander aux utilisateurs de fournir leurs propres clés

### Port 8000

Le backend utilise **toujours** le port 8000 en local.

Si un utilisateur a déjà un service sur ce port:
- Le backend échouera
- L'app ne fonctionnera pas

**Solution:** Rendre le port configurable ou utiliser un port aléatoire.

---

## ✅ Checklist Avant Distribution

- [ ] Backend build réussi
- [ ] Desktop app build réussi
- [ ] Backend inclus dans resources/
- [ ] Testé l'installateur sur une machine propre
- [ ] Vérifié que le backend démarre automatiquement
- [ ] Testé une tâche complète (prompt → action)
- [ ] Bouton Stop fonctionne
- [ ] Raccourci Ctrl+Shift+A fonctionne
- [ ] System tray fonctionne
- [ ] Désinstallation fonctionne proprement
- [ ] README avec instructions utilisateur
- [ ] Page de téléchargement créée

---

**C'est tout! Votre app est prête à être distribuée! 🎉**

Pour plus d'options (macOS, Linux, auto-updates, etc.), consultez [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md).
