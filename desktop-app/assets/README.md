# Assets - Icônes

## Créer les icônes pour l'app

L'app a besoin d'icônes dans différents formats:

### Formats nécessaires:

1. **icon.png** (512x512) - Pour Linux et placeholder
2. **icon.ico** (multi-résolution) - Pour Windows
3. **icon.icns** (multi-résolution) - Pour macOS

### Option 1: Convertir le SVG (Recommandé)

1. Ouvrez `icon.svg` dans votre éditeur d'image préféré
2. Exportez en PNG 512x512 → `icon.png`
3. Utilisez un convertisseur en ligne:
   - SVG → ICO: https://convertio.co/svg-ico/
   - SVG → ICNS: https://cloudconvert.com/svg-to-icns/

### Option 2: Utiliser un outil CLI

Installez `electron-icon-maker`:

```bash
npm install -g electron-icon-maker
electron-icon-maker --input=icon.svg --output=./
```

### Option 3: Créer votre propre icône

1. Créez une image 512x512 avec votre design
2. Sauvegardez comme `icon.png`
3. Convertissez en .ico et .icns comme ci-dessus

### Quick Fix (Temporaire)

Pour tester rapidement sans icône:

1. Téléchargez n'importe quelle icône PNG 512x512
2. Renommez-la en `icon.png` et placez-la ici
3. L'app utilisera cette icône

## Note

L'icône SVG actuelle est un placeholder simple (fond bleu avec "S3").
Remplacez-la par votre propre design pour une app plus professionnelle!

### Suggestions de design:

- Logo avec robot/IA
- Icône minimaliste avec "A" ou "S3"
- Gradient moderne bleu/violet
- Style flat design
