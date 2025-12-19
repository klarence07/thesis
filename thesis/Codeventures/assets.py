import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sys

TILE_SIZE = 50

def get_base_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

def create_placeholder_images(base_dir):
    """Create placeholder images if not found, including stride simulation."""
    try:
        # Attempt to load a Consolas-like monospace font for the neon theme
        font = ImageFont.truetype("consolas.ttf", 28)
    except:
        font = ImageFont.load_default()

    # Grass
    grass = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (34, 139, 34, 255))
    draw = ImageDraw.Draw(grass)
    # New speckled grass texture
    for _ in range(100):
        x, y = random.randint(0, TILE_SIZE), random.randint(0, TILE_SIZE)
        draw.point((x, y), fill=(0, 100, 0, 180))
    grass.save(os.path.join(base_dir, "grass.png"))

    # Player (Simulating Stride/Movement Frame - Red/Orange)
    player = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0)) # Transparent BG
    draw = ImageDraw.Draw(player)

    # Body (Dark Red/Orange theme based on previous context)
    body_color = (200, 50, 0, 255)
    leg_color = (150, 30, 0, 255)

    draw.rectangle([5, 5, TILE_SIZE - 5, TILE_SIZE - 5], fill=body_color)

    # Stride Simulation: One leg forward, one leg back
    draw.line([(TILE_SIZE // 2 - 5, TILE_SIZE - 10), (TILE_SIZE // 2 - 15, TILE_SIZE - 5)], fill=leg_color, width=3) # Forward Leg
    draw.line([(TILE_SIZE // 2 + 5, TILE_SIZE - 10), (TILE_SIZE // 2 + 10, TILE_SIZE - 15)], fill=leg_color, width=3) # Back Leg

    # Letter 'P'
    bbox = draw.textbbox((0, 0), "P", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2 - 2), "P", font=font, fill="white")
    player.save(os.path.join(base_dir, "player.png"))

    # NPC (Simulating Stride/Movement Frame - Blue)
    npc = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(npc)

    # Body (Dark Blue theme)
    body_color_npc = (0, 0, 200, 255)
    leg_color_npc = (0, 0, 150, 255)

    draw.ellipse([5, 5, TILE_SIZE - 5, TILE_SIZE - 5], fill=body_color_npc)

    # Stride Simulation: One leg forward, one leg back
    draw.line([(TILE_SIZE // 2 - 5, TILE_SIZE - 10), (TILE_SIZE // 2 - 15, TILE_SIZE - 5)], fill=leg_color_npc, width=3) # Forward Leg
    draw.line([(TILE_SIZE // 2 + 5, TILE_SIZE - 10), (TILE_SIZE // 2 + 10, TILE_SIZE - 15)], fill=leg_color_npc, width=3) # Back Leg

    # Letter 'N'
    bbox = draw.textbbox((0, 0), "N", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2 - 2), "N", font=font, fill="white")
    npc.save(os.path.join(base_dir, "Npc.png"))

    # Enemy
    enemy = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (128, 0, 128, 255))  # Purple
    draw = ImageDraw.Draw(enemy)
    draw.polygon([(TILE_SIZE / 2, 5), (TILE_SIZE - 5, TILE_SIZE - 5), (5, TILE_SIZE - 5)], fill=(100, 0, 100, 255))

    bbox = draw.textbbox((0, 0), "E", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2), "E", font=font, fill="white")
    enemy.save(os.path.join(base_dir, "enemy.png"))

    # Goblin
    goblin = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 128, 0, 255))  # Green
    draw = ImageDraw.Draw(goblin)
    draw.polygon([(TILE_SIZE / 2, 5), (TILE_SIZE - 5, TILE_SIZE - 5), (5, TILE_SIZE - 5)], fill=(0, 100, 0, 255))

    bbox = draw.textbbox((0, 0), "G", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2), "G", font=font, fill="white")
    goblin.save(os.path.join(base_dir, "goblin.png"))

    # Typomancer
    typo = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 100, 200, 255))  # Blue
    draw = ImageDraw.Draw(typo)
    draw.ellipse([5, 5, TILE_SIZE - 5, TILE_SIZE - 5], fill=(0, 75, 150, 255))

    bbox = draw.textbbox((0, 0), "T", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2), "T", font=font, fill="white")
    typo.save(os.path.join(base_dir, "typomancer.png"))

    # Silver Chest
    silver_chest = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (192, 192, 192, 255))
    draw = ImageDraw.Draw(silver_chest)
    draw.rectangle([5, 15, TILE_SIZE - 5, TILE_SIZE - 5], fill=(160, 160, 160, 255))
    draw.rectangle([10, 5, TILE_SIZE - 10, 20], fill=(220, 220, 220, 255))
    bbox = draw.textbbox((0, 0), "SC", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2), "SC", font=font, fill="black")
    silver_chest.save(os.path.join(base_dir, "silver_chest.png"))

    # Gold Chest
    gold_chest = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (255, 215, 0, 255))
    draw = ImageDraw.Draw(gold_chest)
    draw.rectangle([5, 15, TILE_SIZE - 5, TILE_SIZE - 5], fill=(218, 165, 32, 255))
    draw.rectangle([10, 5, TILE_SIZE - 10, 20], fill=(255, 230, 0, 255))
    bbox = draw.textbbox((0, 0), "GC", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2), "GC", font=font, fill="black")
    gold_chest.save(os.path.join(base_dir, "gold_chest.png"))

    # Pickaxe
    pickaxe = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (139, 69, 19, 255))  # Brown
    draw = ImageDraw.Draw(pickaxe)
    draw.line([(TILE_SIZE / 4, TILE_SIZE / 4), (TILE_SIZE / 2, TILE_SIZE / 2), (TILE_SIZE * 3 / 4, TILE_SIZE * 3 / 4)],
              fill=(0, 0, 0, 255), width=3)
    draw.line([(TILE_SIZE / 4, TILE_SIZE * 3 / 4), (TILE_SIZE / 2, TILE_SIZE / 2), (TILE_SIZE * 3 / 4, TILE_SIZE / 4)],
              fill=(0, 0, 0, 255), width=3)
    bbox = draw.textbbox((0, 0), "P", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((TILE_SIZE - w) / 2, (TILE_SIZE - h) / 2), "P", font=font, fill="white")
    pickaxe.save(os.path.join(base_dir, "pickaxe.png"))

    # Portal
    portal = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(portal)
    # Swirling effect
    draw.ellipse([5, 5, TILE_SIZE - 5, TILE_SIZE - 5], fill=(75, 0, 130, 200))  # Indigo
    draw.ellipse([10, 10, TILE_SIZE - 10, TILE_SIZE - 10], fill=(138, 43, 226, 220))  # BlueViolet
    draw.ellipse([15, 15, TILE_SIZE - 15, TILE_SIZE - 15], fill=(255, 255, 255, 255))  # White center
    portal.save(os.path.join(base_dir, "portal.png"))

def load_resized_image(path):
    try:
        img = Image.open(path).resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def load_all_images(base_dir, gender):
    images = {}
    if not all(os.path.exists(os.path.join(base_dir, img)) for img in
               ["grass.png", "Npc.png", "enemy.png", "goblin.png", "typomancer.png", "silver_chest.png",
                "gold_chest.png", "pickaxe.png", "portal.png"]):
        create_placeholder_images(base_dir)

    images["grass"] = load_resized_image(os.path.join(base_dir, "grass.png"))
    images["npc"] = load_resized_image(os.path.join(base_dir, "Npc.png"))
    images["enemy"] = load_resized_image(os.path.join(base_dir, "enemy.png"))
    images["goblin"] = load_resized_image(os.path.join(base_dir, "goblin.png"))
    images["typomancer"] = load_resized_image(os.path.join(base_dir, "typomancer.png"))
    images["silver_chest"] = load_resized_image(os.path.join(base_dir, "silver_chest.png"))
    images["gold_chest"] = load_resized_image(os.path.join(base_dir, "gold_chest.png"))
    images["pickaxe"] = load_resized_image(os.path.join(base_dir, "pickaxe.png"))
    images["portal"] = load_resized_image(os.path.join(base_dir, "portal.png"))
    images["sword"] = load_resized_image(os.path.join(base_dir, "sword.png"))
    images["goblin_axe"] = load_resized_image(os.path.join(base_dir, "goblin_axe.png"))
    images["slime_goo"] = load_resized_image(os.path.join(base_dir, "slime_goo.png"))
    images["silver_key"] = load_resized_image(os.path.join(base_dir, "silver_key.png"))
    images["gold_key"] = load_resized_image(os.path.join(base_dir, "gold_key.png"))
    images["rock"] = load_resized_image(os.path.join(base_dir, "rock.png"))
    images["spikes"] = load_resized_image(os.path.join(base_dir, "Spikes.png"))
    images["fire"] = load_resized_image(os.path.join(base_dir, "fire.png"))
    images["tree"] = load_resized_image(os.path.join(base_dir, "tree.png"))

    if gender == "girl" and os.path.exists(os.path.join(base_dir, "girl.png")):
        images["player"] = load_resized_image(os.path.join(base_dir, "girl.png"))
    elif gender == "boy" and os.path.exists(os.path.join(base_dir, "boy.png")):
        images["player"] = load_resized_image(os.path.join(base_dir, "boy.png"))
    else:
        images["player"] = load_resized_image(os.path.join(base_dir, "player.png"))

    return images
