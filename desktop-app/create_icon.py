"""
Script pour créer une icône PNG simple pour Agent S3
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Crée une icône 512x512 simple"""

    # Créer une image 512x512
    size = 512
    img = Image.new('RGB', (size, size), color='#3B82F6')  # Bleu
    draw = ImageDraw.Draw(img)

    # Dessiner le cercle de fond
    circle_margin = 20
    draw.ellipse(
        [circle_margin, circle_margin, size - circle_margin, size - circle_margin],
        fill='#3B82F6',
        outline='#60A5FA',
        width=8
    )

    # Dessiner des cercles décoratifs aux coins
    corner_radius = 30
    corners = [
        (80, 80),
        (size - 80, 80),
        (80, size - 80),
        (size - 80, size - 80)
    ]

    for x, y in corners:
        draw.ellipse(
            [x - corner_radius, y - corner_radius, x + corner_radius, y + corner_radius],
            fill='#FFFFFF',
            outline='#E0E0E0',
            width=3
        )

    # Dessiner des lignes connectant les cercles
    draw.line([corners[0], corners[1]], fill='#FFFFFF', width=4)
    draw.line([corners[2], corners[3]], fill='#FFFFFF', width=4)
    draw.line([corners[0], corners[2]], fill='#FFFFFF', width=4)
    draw.line([corners[1], corners[3]], fill='#FFFFFF', width=4)

    # Ajouter le texte "S3"
    try:
        # Essayer d'utiliser une belle police
        font = ImageFont.truetype("arial.ttf", 180)
    except:
        # Fallback sur la police par défaut
        font = ImageFont.load_default()

    # Calculer la position du texte (centré)
    text = "S3"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 20

    # Dessiner le texte avec ombre
    shadow_offset = 5
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, fill='#1E40AF', font=font)
    draw.text((text_x, text_y), text, fill='#FFFFFF', font=font)

    # Sauvegarder
    output_path = os.path.join('assets', 'icon.png')
    img.save(output_path, 'PNG', quality=95)
    print(f"[OK] Icone creee: {output_path}")
    print(f"   Taille: 512x512 pixels")

    # Créer aussi une version 256x256 pour le tray
    img_small = img.resize((256, 256), Image.Resampling.LANCZOS)
    output_small = os.path.join('assets', 'icon-tray.png')
    img_small.save(output_small, 'PNG', quality=95)
    print(f"[OK] Icone tray creee: {output_small}")

if __name__ == '__main__':
    # Vérifier que Pillow est installé
    try:
        import PIL
    except ImportError:
        print("[ERREUR] Pillow n'est pas installe!")
        print("Installation: pip install Pillow")
        exit(1)

    # Créer le dossier assets s'il n'existe pas
    os.makedirs('assets', exist_ok=True)

    # Créer l'icône
    create_icon()

    print("\n[OK] Icones creees avec succes!")
    print("\nPour creer l'icone .ico pour Windows:")
    print("1. Allez sur https://convertio.co/png-ico/")
    print("2. Uploadez assets/icon.png")
    print("3. Telechargez et sauvegardez comme assets/icon.ico")
