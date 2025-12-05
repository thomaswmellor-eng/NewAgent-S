# 🎨 Comment Changer les Icônes de Flemme

## Fichiers d'icônes nécessaires

L'app a besoin de **3 formats d'icônes**:

| Format | Fichier | Utilisation |
|--------|---------|-------------|
| **PNG** | `assets/icon.png` | Linux + Placeholder (512x512) |
| **ICO** | `assets/icon.ico` | Windows (multi-résolution) |
| **ICNS** | `assets/icon.icns` | macOS (multi-résolution) |

---

## Méthode 1: Avec une Image Existante (Recommandé)

### Étape 1: Préparer ton image

1. Trouve ou crée ton logo/icône
2. Assure-toi qu'elle soit **carrée** (ex: 512x512, 1024x1024)
3. Format idéal: PNG avec fond transparent

### Étape 2: Convertir en PNG 512x512

Utilise un éditeur d'image (Photoshop, GIMP, Figma, etc.):
- Redimensionne à **512x512 pixels**
- Sauvegarde comme `icon.png`
- Place dans `desktop-app/assets/icon.png`

### Étape 3: Créer l'icône Windows (.ico)

**Option A: En ligne (le plus simple)**
1. Va sur https://convertio.co/png-ico/
2. Upload `icon.png`
3. Télécharge le `.ico` généré
4. Renomme en `icon.ico`
5. Place dans `desktop-app/assets/icon.ico`

**Option B: Avec ImageMagick**
```bash
magick convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

### Étape 4: Créer l'icône macOS (.icns)

**Option A: En ligne**
1. Va sur https://cloudconvert.com/png-to-icns
2. Upload `icon.png`
3. Télécharge le `.icns` généré
4. Place dans `desktop-app/assets/icon.icns`

**Option B: Avec iconutil (macOS uniquement)**
```bash
# Créer iconset
mkdir MyIcon.iconset
sips -z 16 16   icon.png --out MyIcon.iconset/icon_16x16.png
sips -z 32 32   icon.png --out MyIcon.iconset/icon_16x16@2x.png
sips -z 32 32   icon.png --out MyIcon.iconset/icon_32x32.png
# ... (plus de tailles)
iconutil -c icns MyIcon.iconset
```

---

## Méthode 2: Créer avec Python (Script fourni)

### Modifier le script existant

Édite `desktop-app/create_icon.py`:

```python
# Change la couleur de fond
background_color = '#3B82F6'  # Bleu actuel
# En:
background_color = '#FF6B6B'  # Rouge, par exemple

# Change le texte
text = "S3"
# En:
text = "F"  # Pour "Flemme"
```

### Lancer le script

```bash
cd desktop-app
python create_icon.py
```

Cela génère:
- `assets/icon.png` (512x512)
- `assets/icon-tray.png` (256x256)

Puis convertis en .ico et .icns avec les méthodes ci-dessus.

---

## Méthode 3: Avec un Designer Pro

### Figma / Sketch / Illustrator

1. Crée ton design
2. Exporte en:
   - **PNG 512x512** (avec fond transparent)
   - **PNG 1024x1024** (haute résolution)

3. Utilise un service comme:
   - https://icon.kitchen/ (génère tous les formats)
   - https://makeappicon.com/ (spécialisé app icons)

4. Télécharge et place les fichiers dans `assets/`

---

## Vérifier que ça fonctionne

### Test en développement

```bash
cd desktop-app
npm start
```

- L'icône apparaît dans le system tray (barre des tâches)
- L'icône apparaît dans la barre de titre (si activée)

### Test après build

```bash
npm run build:win
```

- Installe `dist/Flemme-Setup.exe`
- Vérifie l'icône dans:
  - Menu Démarrer
  - Bureau (si raccourci créé)
  - Barre des tâches
  - System tray

---

## Tailles d'icônes recommandées

| Plateforme | Format | Tailles incluses |
|------------|--------|------------------|
| **Windows** | .ico | 16, 32, 48, 64, 128, 256 |
| **macOS** | .icns | 16, 32, 64, 128, 256, 512, 1024 |
| **Linux** | .png | 512x512 |

---

## Outils utiles

### En ligne
- https://convertio.co/ - Convertisseur universel
- https://cloudconvert.com/ - Conversion de formats
- https://icon.kitchen/ - Générateur d'icônes app
- https://makeappicon.com/ - Icônes iOS/Android/Desktop

### Logiciels
- **GIMP** (gratuit) - Éditeur d'images
- **ImageMagick** (CLI) - Conversion en batch
- **Inkscape** (gratuit) - Design vectoriel
- **Figma** (gratuit) - Design professionnel

---

## Conseils Design

### ✅ Bonnes pratiques

- **Fond transparent** pour le PNG
- **Design simple** - visible en petit (16x16)
- **Contrastes forts** - lisible sur fond clair/sombre
- **Pas de texte fin** - illisible en petit
- **Marges** - laisse 10% d'espace autour

### ❌ À éviter

- Trop de détails (illisible en petit)
- Dégradés complexes
- Texte trop long
- Couleurs trop claires/sombres

---

## Exemple: Icône "Flemme"

### Option simple: Emoji
- Trouve un emoji qui représente "flemme" (💤 😴 🛋️)
- Capture en haute résolution
- Utilise comme base

### Option custom: Lettre F
```python
# Édite create_icon.py
text = "F"
background_color = '#6366F1'  # Violet
```

### Option pro: Logo custom
- Crée dans Figma
- Exporte 1024x1024
- Convertis avec icon.kitchen

---

## Problèmes courants

### L'icône n'apparaît pas après build

1. Vérifie que les fichiers existent:
   - `assets/icon.ico` (Windows)
   - `assets/icon.icns` (macOS)
   - `assets/icon.png` (Linux)

2. Rebuild l'app:
   ```bash
   npm run build:win
   ```

3. Vide le cache Electron:
   ```bash
   rm -rf node_modules/.cache
   ```

### L'icône est floue

- Utilise une source haute résolution (1024x1024)
- Vérifie que le .ico contient plusieurs tailles
- Assure-toi que le PNG est bien 512x512

### L'icône a un fond blanc

- Utilise un PNG avec **canal alpha** (transparence)
- Dans GIMP: Layer → Transparency → Add Alpha Channel

---

**C'est tout!** Change les 3 fichiers dans `assets/` et rebuild 🎨
