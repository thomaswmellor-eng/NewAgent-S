# 🚀 Démarrage Rapide - Agent S3 Desktop

## 3 étapes pour lancer l'app

### Étape 1: Installer les dépendances

```bash
cd desktop-app
npm install
```

⏱️ Prend 2-3 minutes

### Étape 2: Lancer l'app

```bash
npm start
```

✅ L'app se lance automatiquement!

### Étape 3: Tester

Dans l'app, tapez:
```
Va sur google.com
```

Et voilà! 🎉

---

## Pour créer l'installateur .exe

```bash
npm run build:win
```

L'installateur sera dans `dist/Agent-S3-Setup.exe`

---

## Raccourcis

- **Ctrl+Shift+A** - Afficher/masquer la fenêtre
- **Ctrl+R** - Recharger l'app (en dev)
- **Ctrl+Shift+I** - DevTools (en dev)

---

## Problème?

### "npm not found"
→ Installez Node.js: https://nodejs.org/

### L'app ne se connecte pas
→ Vérifiez que le backend tourne sur `http://localhost:8000`:
```bash
python backend/main.py
```

### Autre problème
→ Lisez [README.md](./README.md) ou [INSTALL.md](./INSTALL.md)

---

C'est tout! Simple, non? 😎
