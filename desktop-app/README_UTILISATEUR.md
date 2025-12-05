# 🤖 Flemme - AI Desktop Assistant

Flemme est un assistant IA de bureau qui contrôle votre ordinateur en langage naturel.

---

## 📥 Installation

### Windows

1. **Téléchargez** `Flemme Setup 1.0.0.exe`
2. **Double-cliquez** sur le fichier téléchargé
3. **Suivez** l'assistant d'installation:
   - Choisissez le dossier d'installation
   - Cochez "Créer un raccourci bureau" (optionnel)
4. **Cliquez** sur "Installer"

### ⚠️ Avertissement Windows Defender

Windows peut afficher un message de sécurité car l'application n'est pas signée numériquement:

> "Windows a protégé votre PC"

**C'est normal!** Pour continuer:
1. Cliquez sur **"Informations complémentaires"**
2. Cliquez sur **"Exécuter quand même"**

---

## 🚀 Démarrage

### Première Utilisation

1. **Lancez Flemme** depuis:
   - Le menu Démarrer
   - Le raccourci bureau
   - L'icône dans la barre des tâches (system tray)

2. **La fenêtre apparaît** en haut à droite de votre écran

3. **L'icône Flemme** apparaît dans le system tray (à côté de l'horloge)

### Raccourci Clavier Global

Appuyez sur **Ctrl+Shift+A** n'importe où pour:
- Afficher la fenêtre si elle est cachée
- Masquer la fenêtre si elle est visible

---

## 💬 Utilisation

### Donner des Instructions

Tapez vos instructions en langage naturel dans le champ de texte:

**Exemples:**

```
Ouvre Google Chrome et va sur YouTube
```

```
Crée un nouveau document Word et écris "Bonjour"
```

```
Trouve le fichier "rapport.pdf" sur mon bureau
```

```
Ferme toutes les fenêtres Edge
```

```
Recherche "recette de crêpes" sur Google
```

### Pendant l'Exécution

- **Messages en temps réel** s'affichent pour montrer ce que l'agent fait
- **Bouton Stop** (⏹️) apparaît pour arrêter l'exécution si besoin
- **L'agent prend des captures d'écran** pour comprendre ce qu'il fait

### Arrêter une Tâche

Si l'agent fait quelque chose d'inattendu:
1. **Cliquez** sur le bouton **Stop** (carré rouge)
2. L'exécution s'arrête immédiatement
3. Le bouton **Envoyer** réapparaît

---

## ⚙️ Paramètres

### System Tray (Barre des Tâches)

**Clic droit** sur l'icône Flemme dans le system tray:

| Option | Description |
|--------|-------------|
| **Afficher Flemme** | Ouvre la fenêtre |
| **Masquer** | Cache la fenêtre |
| **Toujours au-dessus** | Garde la fenêtre au-dessus des autres |
| **Quitter** | Ferme complètement l'application |

### Garder la Fenêtre Visible

Par défaut, la fenêtre reste **toujours au-dessus** des autres applications.

Pour désactiver:
- System tray → Décochez "Toujours au-dessus"

---

## 🔧 Fonctionnalités

### Ce que Flemme Peut Faire

- ✅ **Ouvrir des applications** (Chrome, Word, Excel, etc.)
- ✅ **Naviguer sur le web** (rechercher, cliquer, remplir des formulaires)
- ✅ **Manipuler des fichiers** (ouvrir, renommer, déplacer)
- ✅ **Contrôler Windows** (fenêtres, raccourcis clavier)
- ✅ **Automatiser des tâches répétitives**

### Ce que Flemme NE Fait PAS

- ❌ Accéder à Internet sans navigateur
- ❌ Lire dans votre tête
- ❌ Faire du café ☕ (malheureusement)

---

## 🐛 Problèmes Courants

### "Connexion au serveur échouée"

**Cause:** Le backend n'a pas démarré correctement.

**Solution:**
1. Fermez complètement Flemme (System tray → Quitter)
2. Relancez l'application
3. Attendez 5 secondes avant d'utiliser

---

### L'Agent Ne Fait Rien

**Vérifications:**
- ✅ Votre écran est-il allumé? 😄
- ✅ L'instruction est-elle claire?
- ✅ Y a-t-il des messages d'erreur dans la fenêtre?

**Essayez:**
- Reformuler l'instruction plus simplement
- Décomposer en plusieurs étapes
- Vérifier que l'application cible est installée

---

### L'Agent Fait la Mauvaise Chose

**Solution immédiate:**
1. **Cliquez** sur le bouton **Stop** ⏹️
2. L'exécution s'arrête

**Améliorer:**
- Soyez plus précis dans vos instructions
- Indiquez les étapes intermédiaires
- Testez d'abord avec des tâches simples

---

### Windows Defender Bloque l'Application

**Normal!** Flemme n'est pas (encore) signé numériquement.

**Solution:**
1. Windows Defender → Cliquez sur "Plus d'infos"
2. Cliquez sur "Exécuter quand même"

**Ou:**
1. Windows Defender → Protection contre les virus et menaces
2. Gérer les paramètres
3. Ajoutez Flemme aux exclusions

---

### Le Raccourci Ctrl+Shift+A Ne Fonctionne Pas

**Cause:** Une autre application utilise ce raccourci.

**Solutions:**
- Fermez les autres applications
- Ou utilisez le system tray pour afficher/masquer

---

## 🔒 Confidentialité et Sécurité

### Données Collectées

**Aucune donnée n'est envoyée à des serveurs externes.**

Flemme fonctionne **100% en local** sur votre machine:
- Backend Python sur `localhost:8000`
- Captures d'écran traitées localement
- Aucune télémétrie

### Clés API

Flemme utilise Azure OpenAI pour l'intelligence artificielle.

Les clés API sont stockées dans l'application (configuration du développeur).

---

## 🆘 Support

### Problème Non Résolu?

1. **Vérifiez** cette documentation
2. **Redémarrez** l'application
3. **Contactez** le développeur avec:
   - Description du problème
   - Capture d'écran de l'erreur
   - Version de Windows

---

## 📝 Notes Techniques

### Configuration Requise

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 4 GB minimum
- **Espace disque:** 200 MB
- **Connexion Internet:** Requise (pour l'IA Azure)

### Ports Utilisés

- **8000:** Backend FastAPI (localhost uniquement)

Si ce port est déjà utilisé, Flemme ne fonctionnera pas.

---

## 📄 Désinstallation

### Windows

1. **Paramètres Windows** → Applications
2. **Cherchez** "Flemme"
3. **Cliquez** sur "Désinstaller"
4. **Suivez** l'assistant

**Ou:**
- Menu Démarrer → Flemme → Désinstaller

---

## 🎯 Astuces d'Utilisation

### Instructions Efficaces

**✅ Bon:**
```
Ouvre Chrome et va sur google.com
```

**❌ Moins bon:**
```
Peux-tu peut-être ouvrir un navigateur si c'est possible?
```

---

### Décomposer les Tâches

**✅ Bon:**
```
1. Ouvre Word
2. Écris "Rapport mensuel"
3. Sauvegarde le document
```

**❌ Complexe:**
```
Crée un rapport mensuel complet avec graphiques et analyse
```

---

### Être Spécifique

**✅ Bon:**
```
Ouvre le fichier "rapport.pdf" sur le bureau
```

**❌ Vague:**
```
Ouvre un fichier quelque part
```

---

## 🚀 Prochaines Étapes

Maintenant que Flemme est installé:

1. **Testez** avec des tâches simples
2. **Explorez** les possibilités
3. **Automatisez** vos tâches répétitives
4. **Partagez** vos astuces avec la communauté!

---

## 📞 Contact

- **Email:** [votre-email@exemple.com]
- **Site web:** [votre-site.com]
- **GitHub:** [github.com/votre-username/flemme]

---

**Merci d'utiliser Flemme! 🤖✨**

*Version 1.0.0*
