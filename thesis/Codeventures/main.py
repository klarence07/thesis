import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import time
import json

# Handle Audio (Prevent crash if not on Windows)
try:
    import winsound
    AUDIO_ENABLED = True
except ImportError:
    AUDIO_ENABLED = False

TILE_SIZE = 50
MAP_WIDTH = 15
MAP_HEIGHT = 12
HAZARDS = ["spikes", "fire"]


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


class Enemy:
    def __init__(self, name, health, damage, xp_reward, loot):
        self.name = name
        self.health = health
        self.damage = damage
        self.xp_reward = xp_reward
        self.loot = loot


class CombatSystem:
    def __init__(self, game):
        self.game = game
        self.player_dodges = 0
        self.max_dodges = 3
        self.enemy_pos = None

    def start_combat(self, enemy_pos):
        self.game.game_state = "combat"
        self.game.canvas.delete("all")
        enemy_data = self.game.enemies[enemy_pos]
        self.game.unlocked_encyclopedia_entries.add(enemy_data.name)
        self.game.info_label.config(text=f"A {enemy_data.name} appeared!")
        self.game.status_label.config(text="Dodge its attacks! Use WASD to move.")
        self.enemy_pos = list(enemy_pos)
        self.player_dodges = 0
        self.game.root.after(1000, self.enemy_cutscene)

    def enemy_cutscene(self):
        # A simple "cutscene" where the enemy moves
        if self.game.game_state != "combat":
            return

        self.game.canvas.delete("all")
        self.game.canvas.create_image(
            self.game.player_pos[0] * TILE_SIZE + TILE_SIZE // 2,
            self.game.player_pos[1] * TILE_SIZE + TILE_SIZE // 2,
            anchor="center", image=self.game.player_img
        )

        # Check if the enemy still exists at its original position
        enemy_data = self.game.enemies.get(tuple(self.game.current_enemy_pos))
        if not enemy_data:
            # Enemy not found, end combat gracefully
            self.end_combat("win")
            return

        enemy_img = self.game.enemy_img if enemy_data.name == "Slime" else self.game.goblin_img

        self.game.canvas.create_image(
            self.enemy_pos[0] * TILE_SIZE + TILE_SIZE // 2,
            self.enemy_pos[1] * TILE_SIZE + TILE_SIZE // 2,
            anchor="center", image=enemy_img
        )

        self.enemy_pos[0] = self.game.player_pos[0]
        self.game.root.after(500, self.enemy_attack)

    def enemy_attack(self):
        """Handles the enemy's attack action."""
        if self.game.game_state != "combat":
            return

        # Get the enemy data using the original position where combat started.
        enemy_data = self.game.enemies.get(tuple(self.game.current_enemy_pos))

        # If the enemy data is not found, it means the enemy was already removed
        # (e.g., in a previous step). We should end combat safely.
        if not enemy_data:
            self.end_combat("win")
            return

        # Clear the canvas and redraw the player
        self.game.canvas.delete("all")
        self.game.canvas.create_image(
            self.game.player_pos[0] * TILE_SIZE + TILE_SIZE // 2,
            self.game.player_pos[1] * TILE_SIZE + TILE_SIZE // 2,
            anchor="center", image=self.game.player_img
        )

        # Determine the correct image for the enemy
        enemy_img = self.game.enemy_img if enemy_data.name == "Slime" else self.game.goblin_img

        # Redraw the enemy at its current mini-game position
        self.game.canvas.create_image(
            self.enemy_pos[0] * TILE_SIZE + TILE_SIZE // 2,
            self.enemy_pos[1] * TILE_SIZE + TILE_SIZE // 2,
            anchor="center", image=enemy_img
        )

        # Move the enemy closer to the player
        dx = self.game.player_pos[0] - self.enemy_pos[0]
        dy = self.game.player_pos[1] - self.enemy_pos[1]

        if dx != 0:
            self.enemy_pos[0] += dx // abs(dx)
        if dy != 0:
            self.enemy_pos[1] += dy // abs(dy)

        # Check if the enemy has caught the player
        if self.enemy_pos == self.game.player_pos:
            self.game.take_damage(enemy_data.damage, enemy_data.name)
            self.end_combat("loss")
        else:
            self.player_dodges += 1
            if self.player_dodges >= self.max_dodges:
                self.end_combat("win")
            else:
                # Slower for goblin, faster for slime
                delay = 800 if enemy_data.name == "Goblin" else 500
                self.game.root.after(delay, self.enemy_attack)

    def end_combat(self, result):
        self.game.game_state = "exploration"

        enemy_pos = tuple(self.game.current_enemy_pos)
        enemy_defeated = self.game.enemies.pop(enemy_pos, None)

        if not enemy_defeated:
            # This case handles situations where the enemy was already removed
            # but combat was still running.
            self.game.current_enemy = None
            self.game.current_enemy_pos = None
            self.game.draw_map()
            self.game.update_status()
            return

        if result == "win":
            self.game.info_label.config(text=f"You successfully outran the {enemy_defeated.name}!")
            self.game.add_xp(enemy_defeated.xp_reward)
            self.game.add_loot(enemy_defeated.loot)
            if AUDIO_ENABLED:
                self.game.play_sound("victory.wav")
        else:  # "loss"
            # This is specifically for the goblin. If you lose, it's an instant Game Over.
            self.game.info_label.config(text=f"The {enemy_defeated.name} caught you! You were defeated...")
            if enemy_defeated.name == "Goblin":
                self.game.take_damage(self.game.health, "goblin-caught")
            else:
                # For slimes, you just take damage and the game continues
                pass

        self.game.current_enemy = None
        self.game.current_enemy_pos = None
        self.game.draw_map()
        self.game.update_status()


class EncycodepediaWindow:
    def __init__(self, game):
        self.game = game
        self.window = tk.Toplevel(game.root)
        self.window.title("Encycodepedia")
        self.window.geometry("400x500")
        self.window.configure(bg="#1C1C1C")

        self.all_entries = {
            "Enemies": ["Slime", "Goblin", "Typomancer"],
            "Items": ["Silver Key", "Gold Key", "Sword", "Pickaxe", "Goblin Axe", "Slipperoo!"],
            "Tiles": ["Spikes", "Fire", "Rock", "Tree"],
            "NPCs": [],
            "Topics": ["Control Flow", "Loops", "Functions", "Lists", "Dictionaries", "Sets", "Classes"]
        }

        self.descriptions = {
            "Slime": "A common, low-level enemy that can be defeated by outmaneuvering it. They drop a gooey substance.",
            "Goblin": "A fast and cunning enemy. If they catch you, it's game over!",
            "Typomancer": "A master of words and a quirky sorcerer. She challenges travelers to a typing test to prove their wit.",
            "Silver Key": "A key used to open Silver Chests, which contain a small amount of XP.",
            "Gold Key": "A rare key used to open Gold Chests, which contain valuable loot like a Sword or Pickaxe.",
            "Sword": "A powerful weapon that allows you to instantly defeat enemies on contact.",
            "Pickaxe": "A tool used to break through Rock formations, creating a new path.",
            "Goblin Axe": "An item dropped by a Goblin. Can be used to chop down Trees.",
            "Slipperoo!": "A pair of boots crafted from Slime Goo. Allows you to slide safely over spikes without taking damage.",
            "Spikes": "A dangerous floor hazard. Stepping on them will cause you to lose health.",
            "Fire": "A fiery floor hazard. Causes more damage than spikes.",
            "Rock": "A large boulder blocking your path. Requires a Pickaxe to be destroyed.",
            "Tree": "A large tree blocking your path. Requires a Goblin Axe to be chopped down.",
            "Control Flow": "The order in which individual statements or instructions are executed in a program.",
            "Loops": "A programming construct that repeats a sequence of instructions until a specific condition is met.",
            "Functions": "A block of organized, reusable code that is used to perform a single, related action.",
            "Lists": "A collection of items which are ordered and changeable. Allows duplicate members.",
            "Dictionaries": "A collection of key-value pairs which is ordered, changeable, and does not allow duplicates.",
            "Sets": "An unordered collection of unique and immutable objects.",
            "Classes": "A blueprint for creating objects, providing a way to structure code and data."
        }
        
        # --- UI: Tree Wrapper ---
        self.main_frame = tk.Frame(
            self.window, 
            bg="#8B4513", 
            padx=10, pady=10, 
            relief="ridge", borderwidth=4
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = tk.Label(self.main_frame, text="Encycodepedia", font=("Consolas", 16, "bold"), bg="#8B4513", fg="#33FF33")
        self.label.pack(pady=10)

        self.frame = tk.Frame(self.main_frame, bg="#2B2B2B", padx=10, pady=10)
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(self.frame, bg="#2B2B2B", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg="#2B2B2B")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.update_display()
        self.inner_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_description(self, entry_name):
        description = self.descriptions.get(entry_name, "No description available.")
        messagebox.showinfo(entry_name, description)

    def update_display(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for category, entries in self.all_entries.items():
            header = tk.Label(self.inner_frame, text=f"-- {category} --", font=("Consolas", 12, "bold"), bg="#2B2B2B",
                              fg="#00FFFF")
            header.pack(fill="x", pady=(10, 5))
            for entry in entries:
                is_unlocked = entry in self.game.unlocked_encyclopedia_entries
                display_name = entry if is_unlocked else "???"
                label_color = "#33FF33" if is_unlocked else "gray"

                label = tk.Label(self.inner_frame, text=display_name, font=("Consolas", 10), bg="#2B2B2B", fg=label_color,
                                 cursor="hand2" if is_unlocked else "")
                label.pack(fill="x", padx=10)

                if is_unlocked:
                    label.bind("<Button-1>", lambda e, name=entry: self.show_description(name))


class StatsSystem:
    def __init__(self, game):
        self.game = game
        self.window = tk.Toplevel(game.root)
        self.window.title("Upgrade Stats")
        self.window.geometry("350x240") 
        self.window.configure(bg="#1C1C1C")
        
        # --- UI: Tree Wrapper ---
        self.main_frame = tk.Frame(
            self.window, 
            bg="#8B4513", 
            padx=10, pady=10, 
            relief="ridge", borderwidth=4
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = tk.Label(self.main_frame, text="Available Skill Points: 0", bg="#8B4513", fg="#33FF33",
                              font=("Consolas", 12))
        self.label.pack(pady=10)

        self.hp_frame = tk.Frame(self.main_frame, bg="#2B2B2B")
        self.hp_frame.pack(pady=5, padx=10, fill="x")
        self.hp_label = tk.Label(self.hp_frame, text=f"Path of the Warrior: {self.game.stats['HP']}/5", bg="#2B2B2B",
                                 fg="#33FF33")
        self.hp_label.pack(side="left", padx=5)
        self.hp_btn = tk.Button(self.hp_frame, text="Upgrade Path of the Warrior (+20 HP)",
                                command=lambda: self.upgrade_stat("HP"),
                                bg="#33CCFF", fg="#1C1C1C")
        self.hp_btn.pack(side="right", padx=5)

        self.wits_frame = tk.Frame(self.main_frame, bg="#2B2B2B")
        self.wits_frame.pack(pady=5, padx=10, fill="x")
        self.wits_label = tk.Label(self.wits_frame, text=f"Path of the Coder: {self.game.stats['Wits']}/5",
                                   bg="#2B2B2B", fg="#33FF33")
        self.wits_label.pack(side="left", padx=5)
        self.wits_btn = tk.Button(self.wits_frame, text="Upgrade Path of the Coder (+1 Clue)",
                                  command=lambda: self.upgrade_stat("Wits"), bg="#33CCFF", fg="#1C1C1C")
        self.wits_btn.pack(side="right", padx=5)

        self.update_display()

    def upgrade_stat(self, stat):
        if self.game.skill_points > 0 and self.game.stats[stat] < 5:
            self.game.skill_points -= 1
            self.game.stats[stat] += 1
            if stat == "HP":
                self.game.max_health += 20
                self.game.health += 20
                if self.game.health > self.game.max_health:
                    self.game.health = self.max_health

            display_names = {"HP": "Path of the Warrior", "Wits": "Path of the Coder"}
            stat_name = display_names.get(stat, stat)
            messagebox.showinfo("Success", f"You have upgraded {stat_name} to level {self.game.stats[stat]}!")
            self.game.update_status()
            self.update_display()

    def update_display(self):
        self.label.config(text=f"Available Skill Points: {self.game.skill_points}")
        self.hp_label.config(text=f"Path of the Warrior: {self.game.stats['HP']}/5")
        self.wits_label.config(text=f"Path of the Coder: {self.game.stats['Wits']}/5")

        self.hp_btn.config(state="normal" if self.game.skill_points > 0 and self.game.stats['HP'] < 5 else "disabled")
        self.wits_btn.config(
            state="normal" if self.game.skill_points > 0 and self.game.stats['Wits'] < 5 else "disabled")


class CraftingWindow:
    def __init__(self, game):
        self.game = game
        self.window = tk.Toplevel(game.root)
        self.window.title("Crafting")
        self.window.geometry("400x200")
        self.window.configure(bg="#1C1C1C")
        
        # --- UI: Tree Wrapper ---
        self.main_frame = tk.Frame(
            self.window, 
            bg="#8B4513", 
            padx=10, pady=10, 
            relief="ridge", borderwidth=4
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.recipes = {
            "Slipperoo!": {"Slime Goo": 5}
        }

        self.title_label = tk.Label(self.main_frame, text="Available Recipes", bg="#8B4513", fg="#33FF33",
                                    font=("Consolas", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frame for Slipperoo recipe
        self.slipperoo_frame = tk.Frame(self.main_frame, bg="#2B2B2B")
        self.slipperoo_frame.pack(pady=5, padx=10, fill="x")

        self.recipe_label = tk.Label(self.slipperoo_frame, text="Slipperoo! (Requires: 5x Slime Goo)", bg="#2B2B2B",
                                     fg="#33FF33")
        self.recipe_label.pack(side="left", padx=5)

        self.craft_btn = tk.Button(self.slipperoo_frame, text="Craft", command=lambda: self.craft_item("Slipperoo!"),
                                   bg="#33CCFF", fg="#1C1C1C")
        self.craft_btn.pack(side="right", padx=5)

        self.update_display()

    def craft_item(self, item_name):
        recipe = self.recipes.get(item_name)
        if not recipe:
            messagebox.showerror("Error", "Unknown recipe.")
            return

        # Check if player has enough ingredients
        can_craft = True
        for ingredient, required_amount in recipe.items():
            if self.game.inventory.count(ingredient) < required_amount:
                can_craft = False
                break

        if can_craft:
            # Remove ingredients
            for ingredient, required_amount in recipe.items():
                for _ in range(required_amount):
                    self.game.inventory.remove(ingredient)

            # Add crafted item
            self.game.add_loot(item_name)
            messagebox.showinfo("Success!", f"You successfully crafted {item_name}!")
            self.game.update_status()
            self.update_display()
        else:
            messagebox.showwarning("Failed", "You don't have enough ingredients to craft this item.")

    def update_display(self):
        # Check for Slipperoo recipe
        required_goo = self.recipes["Slipperoo!"]["Slime Goo"]
        has_goo = self.game.inventory.count("Slime Goo")

        self.recipe_label.config(text=f"Slipperoo! (Req: 5x Slime Goo) - You have: {has_goo}")

        if has_goo >= required_goo:
            self.craft_btn.config(state="normal")
        else:
            self.craft_btn.config(state="disabled")


class InventoryWindow:
    def __init__(self, game):
        self.game = game
        self.window = tk.Toplevel(game.root)
        self.window.title("Inventory")
        self.window.geometry("450x450") 
        self.window.configure(bg="#1C1C1C") 
        self.window.resizable(False, False)
        
        # --- UI: Tree Wrapper ---
        self.main_frame = tk.Frame(
            self.window, 
            bg="#8B4513", 
            padx=10, pady=10, 
            relief="ridge", borderwidth=4
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Map to count items for stacking
        self.item_counts = {}
        for item in self.game.inventory:
            self.item_counts[item] = self.item_counts.get(item, 0) + 1

        self.unique_items = list(self.item_counts.keys())
        self.grid_size = 5  # 5x5 grid for 25 slots

        tk.Label(self.main_frame, text="Player Inventory", font=("Consolas", 16, "bold"), bg="#8B4513", fg="#33FF33").pack(pady=10)

        self.grid_frame = tk.Frame(self.main_frame, bg="#2B2B2B", padx=5, pady=5) # Frame color
        self.grid_frame.pack(padx=10, pady=10)

        self.action_frame = tk.Frame(self.main_frame, bg="#8B4513") # Base color
        self.action_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.slot_buttons = []
        self.display_inventory_grid()

    def get_item_icon_config(self, item_name):
        # Returns item-specific text, color, and description
        if "Key" in item_name:
            return "KEY", "#FFD700", "Use to open chests."
        if item_name == "Sword":
            return "SWD", "#FF3366", "Allows instant enemy defeat."
        if item_name == "Pickaxe":
            return "PXE", "#33CCFF", "Use to break rocks."
        if item_name == "Goblin Axe":
            return "AXE", "#00FFFF", "Use to chop down trees."
        if item_name == "Slime Goo":
            return "GOO", "#33FF33", "Crafting material."
        if item_name == "Slipperoo!":
            return "SLP", "#00FFFF", "Passive item. Walk safely over spikes."
        if "Potion" in item_name:
            return "POT", "#FF3366", "Restores 50 HP."
        return "???", "gray", "Unknown item."

    def display_inventory_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.slot_buttons.clear()

        item_idx = 0
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                item_name = None
                count = 0
                if item_idx < len(self.unique_items):
                    item_name = self.unique_items[item_idx]
                    count = self.item_counts[item_name]
                    item_idx += 1

                if item_name:
                    item_text, item_color, _ = self.get_item_icon_config(item_name)
                    slot_container = tk.Frame(self.grid_frame, bg="#2B2B2B", borderwidth=2, relief="solid") 
                    slot_container.grid(row=r, column=c, padx=5, pady=5)
                    
                    btn_text = f"{item_text}"
                    btn_font = ("Consolas", 10, "bold")
                    if count == 1 and item_name not in ["Silver Key", "Gold Key", "Slime Goo", "Potion"]:
                        btn_text = item_name.split()[0][:3].upper() if " " in item_name else item_name[:3].upper()

                    btn = tk.Button(
                        slot_container, text=btn_text, bg="#1C1C1C", fg=item_color, font=btn_font,
                        width=5, height=2, compound="center",
                        command=lambda name=item_name: self.show_item_actions(name)
                    )
                    btn.pack(padx=2, pady=2)
                    if count > 1 or "Key" in item_name or "Goo" in item_name:
                        tk.Label(btn, text=f"x{count}", bg="#1C1C1C", fg="#33FF33", font=("Consolas", 7, "bold")).place(relx=1.0, rely=1.0, anchor="se")
                    self.slot_buttons.append(btn)
                else:
                    empty_frame = tk.Frame(self.grid_frame, bg="#2B2B2B", width=50, height=50, borderwidth=1, relief="sunken")
                    empty_frame.grid(row=r, column=c, padx=5, pady=5)
                    empty_frame.grid_propagate(False)

    def show_item_actions(self, item_name):
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        _, item_color, item_desc = self.get_item_icon_config(item_name)
        count = self.item_counts[item_name]

        tk.Label(self.action_frame, text=f"Item: {item_name} (x{count})", font=("Consolas", 12, "bold"), bg="#8B4513", fg="#33FF33").pack(pady=5)
        tk.Label(self.action_frame, text=item_desc, font=("Consolas", 10), bg="#8B4513", fg="#00FFFF", wraplength=400).pack()

        if "Potion" in item_name:
            tk.Button(self.action_frame, text="Use Potion (+50 HP)", bg="#33CCFF", fg="#1C1C1C", command=lambda: self.use_item(item_name)).pack(pady=10)
        elif "Key" in item_name or "Goo" in item_name or "Slipperoo" in item_name or "Axe" in item_name or "Sword" in item_name:
             tk.Label(self.action_frame, text="Use is passive or requires a map interaction.", bg="#8B4513", fg="gray").pack(pady=10)

    def use_item(self, item_name):
        if item_name not in self.game.inventory:
            messagebox.showwarning("Error", f"You do not have a {item_name} to use.")
            return

        if "Potion" in item_name:
            if self.game.health < self.game.max_health:
                heal_amount = 50
                self.game.health += heal_amount
                if self.game.health > self.game.max_health:
                    self.game.health = self.game.max_health
                
                self.game.inventory.remove(item_name)
                self.game.update_status()
                messagebox.showinfo("Used", f"You used a {item_name} and recovered {heal_amount} HP!")
                
                self.item_counts[item_name] -= 1
                if self.item_counts[item_name] == 0:
                    del self.item_counts[item_name]
                    self.unique_items = list(self.item_counts.keys())
                
                self.display_inventory_grid()
                for widget in self.action_frame.winfo_children():
                    widget.destroy()
            else:
                messagebox.showinfo("Full HP", "Your health is already full!")
        else:
            messagebox.showinfo("Tool", f"The {item_name} is used passively or on the map.")


class NameSelectionWindow:
    """Custom window to input player name and choose gender before starting the main game."""
    def __init__(self, master):
        self.master = master
        # self.master.withdraw() # We withdraw in __main__
        self.window = tk.Toplevel(master)
        self.window.title("Character Creation")
        self.window.geometry("380x300")
        self.window.configure(bg="#1C1C1C")
        self.window.resizable(False, False)
        
        self.window.grab_set()

        # --- UI: Tree Wrapper ---
        self.main_frame = tk.Frame(
            self.window, 
            bg="#8B4513", 
            padx=10, pady=10, 
            relief="ridge", borderwidth=4
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            self.main_frame, 
            text="State Your Name Adventurer", 
            font=("Consolas", 14, "bold"), 
            bg="#8B4513", 
            fg="#33FF33"
        ).pack(pady=(10, 10))

        input_frame = tk.Frame(
            self.main_frame, 
            bg="#2B2B2B", 
            padx=10, 
            pady=10, 
            relief="groove", 
            borderwidth=2
        )
        input_frame.pack(pady=10, padx=20)

        self.name_entry = tk.Entry(
            input_frame, 
            font=("Consolas", 14), 
            bg="#1C1C1C", 
            fg="#00FFFF", 
            insertbackground="#00FFFF",
            width=25, 
            bd=0, 
            relief="flat"
        )
        self.name_entry.pack()
        self.name_entry.focus_set()

        tk.Label(
            self.main_frame, 
            text="SELECT AVATAR TYPE", 
            font=("Consolas", 12), 
            bg="#8B4513", 
            fg="#FFD700"
        ).pack(pady=(20, 10))

        button_frame = tk.Frame(self.main_frame, bg="#8B4513")
        button_frame.pack()

        tk.Button(
            button_frame, 
            text="BOY (M)", 
            width=10, 
            bg="#33CCFF", 
            fg="#1C1C1C", 
            font=("Consolas", 12, "bold"),
            command=lambda: self.start_game("boy")
        ).pack(side="left", padx=15)

        tk.Button(
            button_frame, 
            text="GIRL (F)", 
            width=10, 
            bg="#FF3366", 
            fg="#1C1C1C", 
            font=("Consolas", 12, "bold"),
            command=lambda: self.start_game("girl")
        ).pack(side="right", padx=15)

    def start_game(self, gender):
        player_name = self.name_entry.get().strip()
        if not player_name:
            player_name = "Hero"
        
        self.window.destroy()
        self.master.deiconify()
        
        game = RPGGame(self.master, gender=gender, player_name=player_name)


class RPGGame:
    def __init__(self, root, gender="boy", player_name="Hero"):
        self.root = root
        self.root.title("Memory Lane RPG")
        self.root.configure(bg="#1C1C1C")

        self.gender = gender
        self.player_name = player_name
        
        # --- UI: Expandable Main Frame with Border ---
        self.frame = tk.Frame(
            root, 
            bg="#8B4513", 
            padx=10, 
            pady=10, 
            relief="ridge", 
            borderwidth=4
        )
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.side_panel = tk.Frame(self.frame, bg="#1C1C1C", width=200)
        self.side_panel.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=10)

        self.name_frame = tk.Frame(self.side_panel, bg="#2B2B2B", relief="groove", borderwidth=2)
        self.name_frame.pack(fill="x", pady=(10, 5), padx=10)

        self.name_lbl = tk.Label(
            self.name_frame,
            text=f"Name: {self.player_name}",
            fg="#33FF33", bg="#2B2B2B",
            font=("Consolas", 12, "bold"), anchor="w"
        )
        self.name_lbl.pack(fill="x", pady=5, padx=5)

        self.stats_lbl = tk.Label(
            self.side_panel,
            text="Path of the Warrior: 0 | Path of the Coder: 0",
            fg="#33FF33", bg="#1C1C1C",
            font=("Consolas", 10), anchor="w"
        )
        self.stats_lbl.pack(fill="x", pady=(5, 5), padx=10)

        self.skill_points_lbl = tk.Label(
            self.side_panel,
            text="Skill Points: 0",
            fg="#FFD700", bg="#1C1C1C",
            font=("Consolas", 10), anchor="w"
        )
        self.skill_points_lbl.pack(fill="x", pady=(5, 5), padx=10)

        # Health bar and label
        self.health_label = tk.Label(
            self.side_panel, text="HP: 100", fg="#33FF33", bg="#1C1C1C",
            font=("Consolas", 12, "bold"), anchor="w"
        )
        self.health_label.pack(fill="x", pady=(5, 5), padx=10)
        self.health_bar_canvas = tk.Canvas(
            self.side_panel, width=150, height=20, bg="#2B2B2B",
            highlightthickness=1, highlightbackground="#33FF33"
        )
        self.health_bar_canvas.pack(pady=(0, 10), padx=10)

        self.xp_label = tk.Label(
            self.side_panel, text="XP: 0", fg="#33CCFF", bg="#1C1C1C",
            font=("Consolas", 12, "bold"), anchor="w"
        )
        self.xp_label.pack(fill="x", pady=(5, 5), padx=10)
        self.xp_bar_canvas = tk.Canvas(
            self.side_panel, width=150, height=20, bg="#2B2B2B",
            highlightthickness=1, highlightbackground="#33FF33"
        )
        self.xp_bar_canvas.pack(pady=(0, 10), padx=10)

        self.start_time = time.time()
        self.timer_label = tk.Label(
            self.side_panel, text="Time: 0s", fg="#00FFFF", bg="#1C1C1C",
            font=("Consolas", 12, "bold"), anchor="w"
        )
        self.timer_label.pack(fill="x", pady=(5, 5), padx=10)

        self.potion_label = tk.Label(
            self.side_panel, text="Potions: 0", fg="#FFD700", bg="#1C1C1C",
            font=("Consolas", 12, "bold"), anchor="w"
        )
        self.potion_label.pack(fill="x", pady=(10, 5), padx=10)

        # --- MINECRAFT-STYLE INVENTORY ON SIDE PANEL ---
        
        # Inventory Button (Styled like Minecraft Stone/Wood Button)
        self.inventory_btn = tk.Button(
            self.side_panel, 
            text="INVENTORY", 
            command=self.show_inventory,
            bg="#727272", # Stone button gray
            fg="#FFFFFF", # White text
            font=("Consolas", 12, "bold"),
            relief="raised",
            borderwidth=5, # Blocky border
            activebackground="#8B8B8B",
            activeforeground="#FFFFFF"
        )
        self.inventory_btn.pack(pady=(20, 10), padx=10, fill="x")

        # Save and Load buttons
        self.save_btn = tk.Button(self.side_panel, text="Save Game", command=self.save_game, bg="#33CCFF", fg="#1C1C1C", font=("Consolas", 10, "bold"))
        self.save_btn.pack(pady=(5, 5), padx=10, fill="x")

        self.load_btn = tk.Button(self.side_panel, text="Load Game", command=self.load_game, bg="#6699FF", fg="#1C1C1C", font=("Consolas", 10, "bold"))
        self.load_btn.pack(pady=(0, 10), padx=10, fill="x")

        self.upgrade_btn = tk.Button(self.side_panel, text="Upgrade Stats", command=self.open_stats_window, bg="#2B2B2B", fg="#00FFFF", font=("Consolas", 10, "bold"))
        self.upgrade_btn.pack(pady=(0, 10), padx=10, fill="x")

        self.encyclopedia_btn = tk.Button(self.side_panel, text="Encycodepedia", command=self.open_encyclopedia, bg="#2B2B2B", fg="#00FFFF", font=("Consolas", 10, "bold"))
        self.encyclopedia_btn.pack(pady=(0, 10), padx=10, fill="x")

        self.craft_btn = tk.Button(self.side_panel, text="Crafting", command=self.open_crafting_window, bg="#2B2B2B", fg="#00FFFF", font=("Consolas", 10, "bold"))
        self.craft_btn.pack(pady=(0, 10), padx=10, fill="x")

        self.canvas = tk.Canvas(
            self.frame, width=MAP_WIDTH * TILE_SIZE,
            height=MAP_HEIGHT * TILE_SIZE, bg="#6699FF",
            highlightthickness=3, highlightbackground="#33FF33"
        )
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

        self.info_label = tk.Label(
            self.frame, text="Use arrow keys or WASD to move", fg="#00FFFF",
            bg="#2B2B2B", font=("Consolas", 12, "bold")
        )
        self.info_label.grid(row=1, column=1, sticky="w", padx=10)

        self.status_label = tk.Label(root, text="", bg="#1C1C1C", fg="#33FF33", font=("Consolas", 10), anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=(0, 5))

        self.loot_label = tk.Label(root, text="Loot: None", bg="#1C1C1C", fg="#FFD700", font=("Consolas", 10), anchor="w")
        self.loot_label.pack(fill="x", padx=10, pady=(0, 10))

        self.grass_img = self.player_img = self.npc_img = self.enemy_img = self.goblin_img = self.typo_img = None
        self.silver_chest_img = self.gold_chest_img = self.pickaxe_img = None
        self.portal_img = None
        self.image_refs = []

        self.load_images()

        self.player_pos = [0, 0]
        self.portal_pos = None
        self.level = 1
        self.xp = 0
        self.stats = {"HP": 0, "Wits": 0}
        self.skill_points = 0
        self.max_health = 100 + self.stats["HP"] * 20
        self.health = self.max_health
        self.topics = [
            "Control Flow", "Loops", "Functions", "Lists",
            "Dictionaries", "Sets", "Classes", "Tuples", "Modules", "JSON",
            "Recursion", "Inheritance", "Polymorphism", "Abstraction", "Encapsulation"
        ]
        self.all_entries = {
            "Enemies": ["Slime", "Goblin", "Typomancer"],
            "Items": ["Silver Key", "Gold Key", "Sword", "Pickaxe", "Goblin Axe"],
            "Tiles": ["Spikes", "Fire", "Rock", "Tree"],
            "NPCs": ["Tuples", "Modules", "JSON", "Recursion", "Inheritance", "Polymymorphism", "Abstraction", "Encapsulation"],
            "Topics": ["Control Flow", "Loops", "Functions", "Lists", "Dictionaries", "Sets", "Classes"]
        }
        self.npcs = {}
        self.enemies = {}
        self.chests = {} 
        self.completed_topics = set()
        self.mastered_topics = set()
        self.inventory = []
        self.tiles = {}
        self.sword_acquired = False
        self.pickaxe_acquired = False
        self.unlocked_encyclopedia_entries = set()
        self.asked_sub_questions = set()

        self.game_state = "exploration"
        self.has_goblin_spawned = False
        self.current_enemy = None
        self.current_enemy_pos = None
        self.combat_system = CombatSystem(self)
        
        self.minigame_words = []
        self.full_word_string = ""
        self.minigame_start_time = 0
        self.minigame_window = None

        self.generate_npc_positions()
        self.generate_static_tiles()
        self.generate_enemies()
        self.generate_chests()
        self.draw_map()
        self.bind_keys()
        
        self.root.after(1000, self.update_timer)
        
        if AUDIO_ENABLED:
            self.play_background_music()

    # --- Sound and Music ---
    def play_sound(self, sound_file):
        if AUDIO_ENABLED and os.path.exists(sound_file):
            winsound.PlaySound(sound_file, winsound.SND_ASYNC | winsound.SND_ALIAS)

    def play_background_music(self):
        music_file = "music.wav"
        if AUDIO_ENABLED and os.path.exists(music_file):
            winsound.PlaySound(music_file, winsound.SND_ASYNC | winsound.SND_LOOP)

    # --- Save and Load Game ---
    def save_game(self):
        game_state = {
            "player_name": self.player_name,
            "gender": self.gender,
            "player_pos": self.player_pos,
            "level": self.level,
            "xp": self.xp,
            "health": self.health,
            "max_health": self.max_health,
            "stats": self.stats,
            "skill_points": self.skill_points,
            "inventory": self.inventory,
            "completed_topics": list(self.completed_topics),
            "mastered_topics": list(self.mastered_topics),
            "unlocked_encyclopedia_entries": list(self.unlocked_encyclopedia_entries),
            "asked_sub_questions": list(self.asked_sub_questions),
            "npcs": {str(k): v for k, v in self.npcs.items()},
            "enemies": {str(k): {"name": v.name, "health": v.health, "damage": v.damage, "xp_reward": v.xp_reward,
                                 "loot": v.loot} for k, v in self.enemies.items()},
            "chests": {str(k): v for k, v in self.chests.items()},
            "sword_acquired": self.sword_acquired,
            "pickaxe_acquired": self.pickaxe_acquired,
            "tiles": {str(k): v for k, v in self.tiles.items()},
            "elapsed_time": int(time.time() - self.start_time),
            "has_goblin_spawned": self.has_goblin_spawned,
            "portal_pos": self.portal_pos
        }
        with open("savegame.json", "w") as f:
            json.dump(game_state, f)
        messagebox.showinfo("Save Successful", "Game has been saved!")

    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                game_state = json.load(f)
            self.player_name = game_state["player_name"]
            self.gender = game_state["gender"]
            self.player_pos = game_state["player_pos"]
            self.level = game_state["level"]
            self.xp = game_state.get("xp", 0)
            self.health = game_state["health"]
            self.max_health = game_state.get("max_health", 100)
            self.stats = game_state.get("stats", {"HP": 0, "Wits": 0})
            self.skill_points = game_state.get("skill_points", 0)
            self.inventory = game_state["inventory"]
            self.completed_topics = set(game_state["completed_topics"])
            self.mastered_topics = set(game_state.get("mastered_topics", []))
            self.unlocked_encyclopedia_entries = set(game_state.get("unlocked_encyclopedia_entries", []))
            self.asked_sub_questions = set(game_state.get("asked_sub_questions", []))
            self.npcs = {tuple(eval(k)): v for k, v in game_state["npcs"].items()}
            self.enemies = {tuple(eval(k)): Enemy(**v) for k, v in game_state.get("enemies", {}).items()}
            self.chests = {tuple(eval(k)): v for k, v in game_state.get("chests", {}).items()}
            self.sword_acquired = game_state.get("sword_acquired", False)
            self.pickaxe_acquired = game_state.get("pickaxe_acquired", False)
            self.tiles = {tuple(eval(k)): v for k, v in game_state["tiles"].items()}
            self.start_time = time.time() - game_state["elapsed_time"]
            self.has_goblin_spawned = game_state.get("has_goblin_spawned", False)
            self.portal_pos = game_state.get("portal_pos", None)

            self.name_lbl.config(text=f"Name: {self.player_name}")
            self.load_images()
            self.draw_map()
            self.update_status()
            messagebox.showinfo("Load Successful", "Game has been loaded!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved game found!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load game: {e}")
            self.reset_game()

    def reset_game(self):
        """Resets the game to its initial state."""
        self.player_pos = [0, 0]
        self.level = 1
        self.xp = 0
        self.health = 100
        self.max_health = 100
        self.stats = {"HP": 0, "Wits": 0}
        self.skill_points = 0
        self.inventory = []
        self.completed_topics.clear()
        self.mastered_topics.clear()
        self.unlocked_encyclopedia_entries.clear()
        self.asked_sub_questions.clear()
        self.has_goblin_spawned = False
        self.sword_acquired = False
        self.pickaxe_acquired = False
        self.start_time = time.time()
        self.portal_pos = None
        self.generate_npc_positions()
        self.generate_static_tiles()
        self.generate_enemies()
        self.generate_chests()
        self.draw_map()
        self.update_status()
        self.info_label.config(text="Use arrow keys or WASD to move")
        messagebox.showinfo("New Game", "The game has been reset!")

    # --- Inventory & Stats ---
    def show_inventory(self):
        # Instantiate the new graphical inventory window
        InventoryWindow(self)

    def open_stats_window(self):
        StatsSystem(self)

    def open_encyclopedia(self):
        EncycodepediaWindow(self)

    def open_crafting_window(self):
        CraftingWindow(self)

    # --- Game Timer ---
    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}s")
        self.root.after(1000, self.update_timer)

    # --- Load images ---
    def load_images(self):
        def load_resized_image(path):
            try:
                img = Image.open(path).resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading {path}: {e}")
                return None

        base_dir = os.path.dirname(os.path.abspath(__file__))
        if not all(os.path.exists(os.path.join(base_dir, img)) for img in
                   ["grass.png", "npc.png", "enemy.png", "goblin.png", "typomancer.png", "silver_chest.png",
                    "gold_chest.png", "pickaxe.png", "portal.png"]):
            create_placeholder_images(base_dir)

        self.grass_img = load_resized_image(os.path.join(base_dir, "grass.png"))
        
        # --- FILENAME FIX ---
        self.npc_img = load_resized_image(os.path.join(base_dir, "Npc.png")) # Was "npc.png"
        # --- END FIX ---
        
        self.enemy_img = load_resized_image(os.path.join(base_dir, "enemy.png"))
        self.goblin_img = load_resized_image(os.path.join(base_dir, "goblin.png"))
        self.typo_img = load_resized_image(os.path.join(base_dir, "typomancer.png"))
        self.silver_chest_img = load_resized_image(os.path.join(base_dir, "silver_chest.png"))
        self.gold_chest_img = load_resized_image(os.path.join(base_dir, "gold_chest.png"))
        self.pickaxe_img = load_resized_image(os.path.join(base_dir, "pickaxe.png"))
        self.portal_img = load_resized_image(os.path.join(base_dir, "portal.png"))

        if self.gender == "girl" and os.path.exists(os.path.join(base_dir, "girl.png")):
            self.player_img = load_resized_image(os.path.join(base_dir, "girl.png"))
        elif self.gender == "boy" and os.path.exists(os.path.join(base_dir, "boy.png")):
            self.player_img = load_resized_image(os.path.join(base_dir, "boy.png"))
        else:
            self.player_img = load_resized_image(os.path.join(base_dir, "player.png"))

        self.rock_img = load_resized_image(os.path.join(base_dir, "rock.png"))
        
        # --- FILENAME FIX ---
        self.spikes_img = load_resized_image(os.path.join(base_dir, "Spikes.png")) # Was "spikes.png"
        # --- END FIX ---
        
        self.fire_img = load_resized_image(os.path.join(base_dir, "fire.png"))
        self.tree_img = load_resized_image(os.path.join(base_dir, "tree.png"))

    # --- NPC, Enemy and tiles ---
    def get_npc_count_for_level(self):
        return min(self.level + 1, len(self.topics) + 1)

    def generate_npc_positions(self):
        self.npcs.clear()
        positions = set()
        
        # Determine available topics (those not yet mastered)
        available_topics = [t for t in self.topics if t not in self.mastered_topics]
        
        npc_count = self.get_npc_count_for_level()
        
        # Cap the count at the number of available topics
        num_to_select = min(npc_count - 1, len(available_topics))
        
        # If there are no topics left, skip NPC generation (portal should have been triggered)
        if num_to_select <= 0:
            self.completed_topics.clear()
            self.player_pos = [0, 0]
            return

        # Select unique topics from the available pool
        selected_topics = random.sample(available_topics, num_to_select)
        
        # Place NPCs
        for topic in selected_topics:
            pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
            while pos == (0, 0) or pos in positions:
                pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
            self.npcs[pos] = topic
            positions.add(pos)

        self.completed_topics.clear()
        self.player_pos = [0, 0]

    def generate_enemies(self):
        self.enemies.clear()

        if not self.has_goblin_spawned:
            goblin_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
            while goblin_pos in self.npcs or goblin_pos in self.tiles or goblin_pos == (0, 0):
                goblin_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
            self.enemies[goblin_pos] = Enemy("Goblin", 20, 10, 20, "Goblin Axe")
            self.has_goblin_spawned = True

        # Ensure Typomancer always spawns
        typo_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        while typo_pos in self.npcs or typo_pos in self.tiles or typo_pos == (0, 0) or typo_pos in self.enemies:
            typo_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        self.enemies[typo_pos] = Enemy("Typomancer", 10, 0, 10, "Typomancer Key")  # Placeholder stats

        num_slimes = random.randint(1, 3)
        positions = set()
        while len(positions) < num_slimes:
            x, y = random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)
            if (x, y) != (0, 0) and (x, y) not in self.npcs and (x, y) not in self.tiles and (x, y) not in self.enemies:
                positions.add((x, y))

        for pos in positions:
            self.enemies[pos] = Enemy("Slime", 15, 3, 5, "Slime Goo")

    def generate_static_tiles(self):
        self.tiles.clear()
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if (x, y) == (0, 0):
                    continue
                roll = random.random()
                if roll < 0.05:
                    self.tiles[(x, y)] = "spikes"
                elif roll < 0.10:
                    self.tiles[(x, y)] = "fire"
                elif roll < 0.15:
                    self.tiles[(x, y)] = "rock"
                elif roll < 0.20:
                    self.tiles[(x, y)] = "tree"

    def generate_chests(self):
        self.chests.clear()

        # Place a Silver Chest
        silver_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        while silver_pos in self.npcs or silver_pos in self.enemies or silver_pos in self.tiles or silver_pos == (0, 0):
            silver_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        self.chests[silver_pos] = "silver"

        # Place a Gold Chest
        gold_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        while gold_pos in self.npcs or gold_pos in self.enemies or gold_pos in self.tiles or gold_pos == (0,
                                                                                                          0) or gold_pos == silver_pos:
            gold_pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        self.chests[gold_pos] = "gold"

    # --- Draw map centered ---
    def draw_map(self):
        self.canvas.delete("all")
        self.image_refs.clear()

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # Grass
                self.canvas.create_image(
                    x * TILE_SIZE, y * TILE_SIZE,
                    anchor="nw", image=self.grass_img
                )
                self.image_refs.append(self.grass_img)

                # Obstacles/hazards
                if (x, y) in self.tiles:
                    tile = self.tiles[(x, y)]
                    img = None
                    if tile == "spikes":
                        img = self.spikes_img
                    elif tile == "fire":
                        img = self.fire_img
                    elif tile == "rock":
                        img = self.rock_img
                    elif tile == "tree":
                        img = self.tree_img
                    if img:
                        self.canvas.create_image(
                            x * TILE_SIZE + TILE_SIZE // 2,
                            y * TILE_SIZE + TILE_SIZE // 2,
                            anchor="center", image=img
                        )
                        self.image_refs.append(img)

        # NPCs
        for (x, y), topic in self.npcs.items():
            self.canvas.create_image(
                x * TILE_SIZE + TILE_SIZE // 2,
                y * TILE_SIZE + TILE_SIZE // 2,
                anchor="center", image=self.npc_img
            )
            self.image_refs.append(self.npc_img)

        # Chests
        for (x, y), chest_type in self.chests.items():
            img = self.silver_chest_img if chest_type == "silver" else self.gold_chest_img
            self.canvas.create_image(
                x * TILE_SIZE + TILE_SIZE // 2,
                y * TILE_SIZE + TILE_SIZE // 2,
                anchor="center", image=img
            )
            self.image_refs.append(img)

        # Enemies
        for (x, y), enemy in self.enemies.items():
            img = self.enemy_img
            if enemy.name == "Goblin":
                img = self.goblin_img
            elif enemy.name == "Typomancer":
                img = self.typo_img
            self.canvas.create_image(
                x * TILE_SIZE + TILE_SIZE // 2,
                y * TILE_SIZE + TILE_SIZE // 2,
                anchor="center", image=img
            )
            self.image_refs.append(img)

        # Portal
        if self.portal_pos:
            px, py = self.portal_pos
            self.canvas.create_image(
                px * TILE_SIZE + TILE_SIZE // 2,
                py * TILE_SIZE + TILE_SIZE // 2,
                anchor="center", image=self.portal_img
            )
            self.image_refs.append(self.portal_img)

        # Player
        px, py = self.player_pos
        self.canvas.create_image(
            px * TILE_SIZE + TILE_SIZE // 2,
            py * TILE_SIZE + TILE_SIZE // 2,
            anchor="center", image=self.player_img
        )
        self.image_refs.append(self.player_img)

        self.update_status()

    # --- Status & keys ---
    def update_status(self):
        remaining = len(self.npcs) - len(self.completed_topics)
        topics_left = ", ".join(t for t in self.npcs.values() if t not in self.mastered_topics and t != "Typomancer")
        self.status_label.config(
            text=f"Level: {self.level} | HP: {self.health} | Completed: {len(self.mastered_topics)} | Remaining: {len(self.topics) - len(self.mastered_topics)} | Topics Left: {topics_left}"
        )
        self.loot_label.config(text="Loot: " + (", ".join(self.inventory) if self.inventory else "None"))
        potion_count = sum(1 for item in self.inventory if "Potion" in item)
        self.potion_label.config(text=f"Potions: {potion_count}")
        inventory_text = "\n".join(self.inventory) if self.inventory else "None"
        
        # --- FIXED: Removed this line to prevent crash since the label was removed ---
        # self.loot_inventory_label.config(text=f"Inventory:\n{inventory_text}")
        
        self.stats_lbl.config(
            text=f"Path of the Warrior: {self.stats['HP']}/5 | Path of the Coder: {self.stats['Wits']}/5")
        self.skill_points_lbl.config(text=f"Skill Points: {self.skill_points}")
        # Update health bar
        self.health_label.config(text=f"HP: {self.health}/{self.max_health}", fg="#FF3366")
        self.health_bar_canvas.delete("all")
        bar_width = (self.health / self.max_health) * 148
        self.health_bar_canvas.create_rectangle(
            1, 1, bar_width, 19, fill="#FF3366", outline=""
        )

        # Update XP bar
        self.xp_label.config(text=f"XP: {self.xp}", fg="#33CCFF")
        self.xp_bar_canvas.delete("all")
        max_xp = self.level * 20
        xp_width = (self.xp / max_xp) * 148
        self.xp_bar_canvas.create_rectangle(
            1, 1, xp_width, 19, fill="#33CCFF", outline=""
        )

    def bind_keys(self):
        self.root.bind_all("<Key>", self.on_key)

    def on_key(self, e):
        key = (e.keysym or "").lower()
        if self.game_state == "exploration":
            if key in ("up", "w"):
                self.move(0, -1)
            elif key in ("down", "s"):
                self.move(0, 1)
            elif key in ("left", "a"):
                self.move(-1, 0)
            elif key in ("right", "d"):
                self.move(1, 0)
        elif self.game_state == "combat":
            self.player_dodge(key)

    def player_dodge(self, key):
        dx, dy = 0, 0
        if key in ("up", "w"):
            dy = -1
        elif key in ("down", "s"):
            dy = 1
        elif key in ("left", "a"):
            dx = -1
        elif key in ("right", "d"):
            dx = 1

        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            self.player_pos = [new_x, new_y]

    # --- Player movement ---
    def move(self, dx, dy):
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
            return

        pos = (new_x, new_y)

        if self.portal_pos and pos == self.portal_pos:
            if len(self.mastered_topics) == len(self.topics): # Check if all topics are mastered
                messagebox.showinfo("Victory!", "You've completed all levels!")
                
                # --- FIX 1: Sound check ---
                if AUDIO_ENABLED:
                    self.play_sound("victory.wav")
                    
                self.root.quit()
                return
            else:
                self.level += 1
                messagebox.showinfo("Level Up!", f"You have entered the portal. Welcome to level {self.level}!")
                self.portal_pos = None  # Reset portal for the new level
                self.player_pos = [0, 0]  # Reset player position
                self.generate_npc_positions()
                self.generate_static_tiles()
                self.generate_enemies()
                self.generate_chests()
                self.draw_map()
                return  # Stop further movement logic for this turn

        # Special check for Typomancer first, as she's a special kind of enemy
        if pos in self.enemies and self.enemies[pos].name == "Typomancer":
            self.current_enemy_pos = pos
            self.start_typomancer_minigame(pos)
            return

        # Check for instant kill with sword
        if self.sword_acquired and pos in self.enemies:
            enemy = self.enemies[pos]
            self.unlocked_encyclopedia_entries.add(enemy.name)
            messagebox.showinfo("Sword Power!", f"You brandish your sword and instantly defeat the {enemy.name}!")
            self.add_xp(enemy.xp_reward)
            self.add_loot(enemy.loot)
            del self.enemies[pos]
            self.draw_map()
            self.update_status()
            return

        # Handle other enemy encounters
        if pos in self.enemies:
            self.current_enemy_pos = pos
            self.combat_system.start_combat(pos)
            return

        # Handle chests
        if pos in self.chests:
            chest_type = self.chests[pos]
            self.unlocked_encyclopedia_entries.add(f"{chest_type.capitalize()} Chest")
            required_key = "Silver Key" if chest_type == "silver" else "Gold Key"
            if required_key in self.inventory:
                self.inventory.remove(required_key)
                del self.chests[pos]

                if chest_type == "silver":
                    self.add_xp(5)
                    goo_amount = random.randint(1, 3)
                    for _ in range(goo_amount):
                        self.add_loot("Slime Goo")
                    messagebox.showinfo("Success!",
                                        f"You opened the silver chest and gained 5 XP and {goo_amount} Slime Goo!")
                elif chest_type == "gold":
                    self.add_xp(10)
                    # Gold chest rewards a random item
                    reward = random.choice(["Sword", "Pickaxe"])
                    self.add_loot(reward)
                    messagebox.showinfo("Success!", f"You opened the gold chest and gained 10 XP and a {reward}!")

                self.player_pos = [new_x, new_y]
                self.draw_map()
                self.update_status()
                return  # Exit early after a chest interaction
            else:
                messagebox.showwarning("Locked!", f"This {chest_type} chest is locked! You need a {required_key}.")
                return  # Stop movement if chest is locked

        if pos in self.tiles:
            tile = self.tiles[pos]
            self.unlocked_encyclopedia_entries.add(tile.capitalize())
            if tile == "rock":
                if "Pickaxe" in self.inventory:
                    if messagebox.askyesno("Clear Path", "Do you want to use your Pickaxe to clear this rock?"):
                        del self.tiles[pos]
                        messagebox.showinfo("Success!", "You cleared the rock and can now pass!")
                        self.player_pos = [new_x, new_y]
                    else:
                        return
                else:
                    messagebox.showinfo("Blocked!", "A rock blocks your path. You need a Pickaxe to clear it!")
                    return
            elif tile == "tree":
                if "Goblin Axe" in self.inventory:
                    if messagebox.askyesno("Chop Tree", "Do you want to use your Goblin Axe to chop down this tree?"):
                        del self.tiles[pos]
                        messagebox.showinfo("Success!", "You chopped down the tree!")
                        self.player_pos = [new_x, new_y]
                    else:
                        return
                else:
                    messagebox.showinfo("Blocked!", "A tree blocks your path. You need a Goblin Axe to chop it down!")
                    return
            elif tile == "spikes":
                if "Slipperoo!" in self.inventory:
                    messagebox.showinfo("Safe!", "Your Slipperoo! lets you slide safely over the spikes!")
                else:
                    self.take_damage(10, "spikes")
            elif tile == "fire":
                self.take_damage(20, "fire")

        self.player_pos = [new_x, new_y]

        if pos in self.npcs:
            npc_type = self.npcs[pos]
            self.unlocked_encyclopedia_entries.add(npc_type)

            if npc_type not in self.mastered_topics:
                self.ask_question(self.npcs[pos])
            else:
                messagebox.showinfo("Already Completed", f"You've already completed: {self.npcs[pos]}")

        self.draw_map()

    def take_damage(self, amount, source=None):
        self.health -= amount
        self.update_status()
        
        # --- FIX 1: Sound check ---
        if AUDIO_ENABLED:
            self.play_sound("damage.wav")
            
        if source:
            if source == "spikes":
                self.unlocked_encyclopedia_entries.add("Spikes")
                messagebox.showwarning("Ouch!", f"You stepped on spikes and lost {amount} HP!")
            elif source == "fire":
                self.unlocked_encyclopedia_entries.add("Fire")
                messagebox.showwarning("Burned!", f"You walked into fire and lost {amount} HP!")
            elif source == "Slime":
                self.unlocked_encyclopedia_entries.add("Slime")
                messagebox.showwarning("Hit!", f"A Slime hit you and you lost {amount} HP!")
            elif source == "Goblin":
                self.unlocked_encyclopedia_entries.add("Goblin")
                messagebox.showwarning("Hit!", f"The Goblin hit you and you lost {amount} HP!")
            elif source == "goblin-caught":
                # Special condition for goblin catching the player
                messagebox.showinfo("Game Over", "The goblin caught you! Game Over.")
                
                # --- FIX 1: Sound check ---
                if AUDIO_ENABLED:
                    self.play_sound("game_over.wav")
                    
                if messagebox.askyesno("New Game?", "Would you like to start a new game?"):
                    self.reset_game()
                else:
                    try:
                        self.root.destroy()
                    except:
                        pass
                return

        if self.health <= 0:
            messagebox.showinfo("Game Over", "You died! Game Over.")
            
            # --- FIX 1: Sound check ---
            if AUDIO_ENABLED:
                self.play_sound("game_over.wav")
                
            if messagebox.askyesno("New Game?", "Would you like to start a new game?"):
                self.reset_game()
            else:
                try:
                    self.root.destroy()
                except:
                    pass

    def add_xp(self, amount):
        self.xp += amount
        messagebox.showinfo("XP Gained", f"You gained {amount} XP!")
        max_xp = self.level * 20
        if self.xp >= max_xp:
            self.level += 1
            self.xp = self.xp - max_xp
            self.skill_points += 2
            self.health = self.max_health
            messagebox.showinfo("Level Up!", f"You reached level {self.level} and gained 2 skill points!")
            self.generate_enemies()
        self.update_status()

    def add_loot(self, item):
        self.inventory.append(item)
        self.unlocked_encyclopedia_entries.add(item)
        if item == "Sword":
            self.sword_acquired = True
        if item == "Pickaxe":
            self.pickaxe_acquired = True
        self.update_status()
        messagebox.showinfo("Loot!", f"You received {item}!")

    # --- Questions & loot ---
    def check_topic_complete(self, topic):
        """Checks if all sub-questions for a main topic have been asked."""
        # Get the full list of question keys for this topic
        topic_groups = self._get_topic_groups()
        all_keys = topic_groups.get(topic, [topic]) # Defaults to just the topic key if no group is found
        
        # Check if all keys for this topic are in the asked set
        return all(key in self.asked_sub_questions for key in all_keys)

    def _get_unasked_question_key(self, topic):
        """Randomly selects an unasked question key for the given topic."""
        topic_groups = self._get_topic_groups()
        all_keys = topic_groups.get(topic)

        # If the topic isn't a grouped one, just use the topic name as the single key
        if all_keys is None:
            return topic if topic not in self.asked_sub_questions else None

        # Filter out already asked questions
        unasked_keys = [key for key in all_keys if key not in self.asked_sub_questions]

        # Return a randomly selected key, or None if all are asked
        return random.choice(unasked_keys) if unasked_keys else None

    def ask_question(self, topic):
        # 1. Get the key for the next unasked question for this topic.
        question_key = self._get_unasked_question_key(topic)
        
        if question_key is None:
            messagebox.showinfo("Already Completed", f"You've completed all available questions for: {topic}")
            self.game_state = "exploration"
            return

        self.game_state = "question"  # Set game state to 'question'
        self.unlocked_encyclopedia_entries.add(topic)
        
        # 2. Retrieve the question data using the randomized key.
        question_data = self.get_question_data(question_key)
        question, answer, hint = question_data
        
        response = simpledialog.askstring("Question",
                                          f"Hello, {self.player_name}! We're exploring {topic} today.\n\n{question}")

        # Reset game state back to 'exploration' regardless of outcome
        self.game_state = "exploration"

        if response and response.strip().lower() == answer.lower():
            # 3. Mark the specific question as asked.
            self.asked_sub_questions.add(question_key)

            # Check for topic completion
            is_complete = self.check_topic_complete(topic)
            
            if is_complete:
                messagebox.showinfo("Correct!", f"Correct! You've completed ALL questions for: {topic}")
                self.completed_topics.add(topic)
                self.mastered_topics.add(topic) # Mark topic as globally mastered
                
                # --- LOGIC: Remove NPC from map ---
                pos_to_remove = None
                for pos, npc_topic in list(self.npcs.items()):
                    if npc_topic == topic:
                        pos_to_remove = pos
                        break
                
                if pos_to_remove:
                    del self.npcs[pos_to_remove]
                # --- END LOGIC ---
                
            else:
                 messagebox.showinfo("Correct!", f"Correct! You've completed one question for: {topic}")


            loot_item = random.choice(self.get_loot_table())
            self.inventory.append(loot_item)
            messagebox.showinfo("Loot", f"You received: {loot_item}!")
            self.unlocked_encyclopedia_entries.add(loot_item)
            
            # --- FIX 1: Sound check ---
            if AUDIO_ENABLED:
                self.play_sound("correct.wav")
                
            self.add_xp(random.randint(4, 10))
            self.draw_map()

            # FIX: Check if the remaining NPC list is empty (all topics for the current level are completed) to trigger the portal.
            if not self.npcs and not self.portal_pos:
                # Check if all topics in the entire game are mastered
                if len(self.mastered_topics) == len(self.topics):
                    self.info_label.config(text="All topics mastered! Find the portal for final victory!")
                
                # Spawn the portal in a random, empty location
                pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
                while pos in self.npcs or pos in self.enemies or pos in self.tiles or pos in self.chests or pos == tuple(
                        self.player_pos):
                    pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))

                self.portal_pos = pos
                self.info_label.config(text="A portal has opened! Find it to proceed to the next level.")
                
                # --- FIX 1: Sound check ---
                if AUDIO_ENABLED:
                    self.play_sound("level_up.wav")
                    
                self.draw_map()  # Redraw the map to show the portal
        else:
            messagebox.showwarning("Hint", f"Hint: {hint}")

    def get_question_data(self, question_key):
        """Retrieves question data using a specific key, falling back to default if key is not found."""
        questions = self._get_full_question_set()
        
        question, answer, base_hint = questions.get(question_key, ("What programming language are we learning?", "python", "It starts with 'p'"))
        
        wits_level = self.stats["Wits"]
        if wits_level > 0:
            clue_letters = answer[:wits_level]
            new_hint = f"Starts with: '{clue_letters}'"
            return question, answer, new_hint
        return question, answer, base_hint

    def _get_topic_groups(self):
        """Defines the mapping of main topics to all their sub-question keys."""
        return {
            "Control Flow": ["Control Flow", "elif", "else_cf", "break", "continue", "return_cf"],
            "Loops": ["Loops", "while", "range", "membership", "else_loop", "indexed_loop"],
            "Functions": ["Functions", "local", "global", "arguments", "parameters", "none"],
            "Lists": ["Lists", "pop", "sort", "len", "zero", "square_list"],
            "Dictionaries": ["Dictionaries", "keys", "get", "immutable", "hash", "curly"],
            "Sets": ["Sets", "intersection", "union", "remove", "discard", "issubset"],
            "Classes": ["Classes", "self", "blueprint", "method", "static", "instance"],
            "Bubble Sort": ["Bubble Sort", "o(n^2)", "inefficiency", "sorted_pass", "o(n)", "flag"],
            "Binary Search": ["Binary Search", "o(log n)", "middle", "required_sorted", "array", "low high"],
            "Factorial": ["Factorial", "24", "recursive_fact", "1", "multiplication", "product"],
            "Fibonacci": ["Fibonacci", "13", "o(2^n)", "memoization", "base cases", "binst formula"],
            "Palindrome": ["Palindrome", "normalize", "yes", "slice", "equality", "same"],
            "List Comp.": ["List Comp.", "square_lc", "if", "efficient", "expression", "list"],
            "String Slice": ["String Slice", "fifth", "step", "end", "reverse", "slice_char"],
            "Func Return": ["Func Return", "return value", "return_kw", "multiple", "pure", "calling"],
            "Class Init": ["Class Init", "del", "class_init", "constructor", "self_ci", "instance_ci"],
            "Try-Except": ["Try-Except", "finally", "else_te", "raise", "exception", "try"],
            "File Open": ["File Open", "w", "r", "a", "os", "with"],
            "Dict Index": ["Dict Index", "items", "keyerror", "ordered", "in", "item"],
            "Set Add": ["Set Add", "update", "hashable", "set_empty", "pop_set", "set_fn"],
            "Lambda": ["Lambda", "lambda_kw", "expression_l", "higher order", "higher order_l", "anonymous"],
            "Tuple Brackets": ["Tuple Brackets", "immutable_t", "count", "one", "unpacking", "comma"],
            # If any NPC topic is not in this list, it will default to a single question with its own name as the key.
            "Tuples": ["Tuples"],
            "Modules": ["Modules"],
            "JSON": ["JSON"],
            "Recursion": ["Recursion"],
            "Inheritance": ["Inheritance"],
            "Polymorphism": ["Polymorphism"],
            "Abstraction": ["Abstraction"],
            "Encapsulation": ["Encapsulation"],
        }

    def _get_full_question_set(self):
        """Returns the dictionary containing all questions, answers, and hints."""
        return {
            
            
          # --- Fundamentals: Control Flow (6 Questions) ---
            "Control Flow": ("What keyword starts a conditional block?", "if", "Starts with 'i'"),
            "elif": ("What keyword is used for an alternative condition?", "elif", "A shortened version of 'else if'."),
            "else_cf": ("What keyword executes when no conditions are met?", "else", "A four-letter word."),
            "break": ("What keyword exits a loop prematurely?", "break", "A word that means to stop."),
            "continue": ("What statement skips the rest of the current loop iteration?", "continue", "A word that means to move on."),
            "return_cf": ("What keyword exits a function and passes control back to the caller?", "return", "Starts with 'r'"),

            # --- Fundamentals: Loops (6 Questions) ---
            "Loops": ("What keyword starts a loop over items?", "for", "Starts with 'f'"),
            "while": ("What keyword creates a loop that runs until a condition is false?", "while", "A five-letter word for duration."),
            "range": ("Which function generates a sequence of numbers for a loop?", "range", "A five-letter function."),
            "membership": ("What does the 'in' keyword check for in a loop header?", "membership", "A ten-letter concept."),
            "else_loop": ("What can be optionally attached to a loop to execute only if the loop finishes normally (without break)?", "else", "Same as the conditional fallback."),
            "indexed_loop": ("What type of iteration is it when a loop iterates through a list index-by-index?", "indexed", "An eight-letter word."),

            # --- Fundamentals: Functions (6 Questions) ---
            "Functions": ("How do you define a function in Python?", "def", "Starts with 'd'"),
            "local": ("What is a variable declared inside a function known as?", "local", "A five-letter word."),
            "global": ("What keyword is used to access a variable outside the current scope?", "global", "Starts with 'g'"),
            "arguments": ("What is the term for the values passed to a function call?", "arguments", "A nine-letter plural noun."),
            "parameters": ("What is the term for the names defined in the function signature?", "parameters", "Starts with 'p'"),
            "none": ("What value does a function return if no explicit return statement is used?", "none", "A type in Python."),

            # --- Fundamentals: Lists (6 Questions) ---
            "Lists": ("Which method adds an item to a list?", "append", "Starts with 'a'"),
            "pop": ("Which method removes an item at a specific index?", "pop", "A three-letter method."),
            "sort": ("Which method is used to sort the list in place?", "sort", "A four-letter word."),
            "len": ("What function returns the number of items in a list?", "len", "A three-letter function."),
            "zero": ("What is the starting index for all Python lists?", "zero", "A four-letter number."),
            "square_list": ("What type of brackets are used to define a list?", "square", "A six-letter shape."),

            # --- Fundamentals: Dictionaries (6 Questions) ---
            "Dictionaries": ("What symbol separates keys and values?", ":", "It's a colon"),
            "keys": ("What method returns a list of all keys in a dictionary?", "keys", "A four-letter plural noun."),
            "get": ("What method safely retrieves a value using a default if the key is missing?", "get", "A three-letter method."),
            "immutable": ("What must all keys in a dictionary be?", "immutable", "Starts with 'i'"),
            "hash": ("What is a dictionary that uses a number as its key indexed by?", "hash", "A four-letter concept."),
            "curly": ("What type of brackets are used to define a dictionary?", "curly", "A five-letter word."),

            # --- Fundamentals: Sets (6 Questions) ---
            "Sets": ("Which Python type is unordered and unique?", "set", "Starts with 's'"),
            "intersection": ("Which set operation finds all elements in both sets?", "intersection", "A twelve-letter word."),
            "union": ("Which set operation finds all elements in either set?", "union", "A five-letter operation."),
            "remove": ("What method is used to remove an element, raising an error if it's not present?", "remove", "A six-letter method."),
            "discard": ("What method removes an element without raising an error if it's not present?", "discard", "An eight-letter method."),
            "issubset": ("What keyword checks for a subset relationship?", "issubset", "A ten-letter method."),

            # --- Fundamentals: Classes (6 Questions) ---
            "Classes": ("What keyword defines a class?", "class", "Starts with 'c'"),
            "self": ("What is the standard name for the first parameter of an instance method?", "self", "A four-letter keyword."),
            "blueprint": ("What is the blueprint for creating objects called?", "class", "Same as the definition keyword."),
            "method": ("What is a function defined inside a class called?", "method", "A six-letter noun."),
            "static": ("What is a variable associated with the class itself, not the instance?", "static", "A six-letter adjective."),
            "instance": ("What is a variable associated with a specific instance of the class called?", "instance", "An eight-letter word."),

            # --- Algorithms: Bubble Sort (6 Questions) ---
            "Bubble Sort": ("What sorting algorithm repeatedly swaps adjacent elements if they are in the wrong order?", "bubble sort", "Starts with 'b'"),
            "o(n^2)": ("What is the worst-case time complexity of this algorithm (using Big O notation)?", "o(n^2)", "Contains an exponent."),
            "inefficiency": ("What is the main drawback of using this sorting method?", "inefficiency", "A thirteen-letter word."),
            "sorted_pass": ("What state is achieved after the first pass of the algorithm?", "sorted", "The largest element is now in the correct position."),
            "o(n)": ("What is the best-case time complexity for a list that is already sorted?", "o(n)", "Linear time."),
            "flag": ("What technique can be added to detect if the list is already sorted and stop early?", "flag", "A four-letter status variable."),

            # --- Algorithms: Binary Search (6 Questions) ---
            "Binary Search": ("What search algorithm works only on sorted arrays by repeatedly dividing the search interval in half?", "binary search", "Starts with 'b'"),
            "o(log n)": ("What is the time complexity of this algorithm?", "o(log n)", "The fastest Big O for searching."),
            "middle": ("What is the first index checked during the algorithm's iteration?", "middle", "A six-letter word."),
            "required_sorted": ("What is the required condition for the input array?", "sorted", "A six-letter adjective."),
            "array": ("What type of data structure is typically searched using this method?", "array", "A five-letter data type."),
            "low high": ("What two values define the search range during an iteration?", "low high", "Two three-letter words."),

            # --- Algorithms: Factorial (6 Questions) ---
            "Factorial": ("What algorithm calculates the product of all integers from 1 up to a given integer?", "factorial", "Starts with 'f'"),
            "24": ("What is the factorial of the number 4?", "24", "A two-digit number."),
            "recursive_fact": ("What type of function is often used to implement this calculation (when it calls itself)?", "recursive", "A nine-letter adjective."),
            "1": ("What is the base case for the calculation (the factorial of 0)?", "1", "A single digit number."),
            "multiplication": ("What mathematical operation is central to calculating the next step?", "multiplication", "A fourteen-letter word."),
            "product": ("What is the term for calculating the product of a sequence of integers?", "product", "A seven-letter word."),

            # --- Algorithms: Fibonacci (6 Questions) ---
            "Fibonacci": ("What is the sequence where each number is the sum of the two preceding ones?", "fibonacci", "Starts with 'f'"),
            "13": ("What is the 7th number in the sequence (starting 0, 1, 1, 2, 3, 5, 8...)?", "13", "A two-digit number."),
            "o(2^n)": ("What is the time complexity of the naive recursive implementation?", "o(2^n)", "Exponential complexity."),
            "memoization": ("What technique can improve the performance of the recursive version?", "memoization", "A twelve-letter word."),
            "base cases": ("What is the name of the two starting numbers in the sequence (0 and 1)?", "base cases", "Two four-letter words."),
            "binst formula": ("What is the formula that relates the sequence to the golden ratio?", "binst formula", "A twelve-letter proper noun."),

            # --- Algorithms: Palindrome (6 Questions) ---
            "Palindrome": ("What is a word or phrase that reads the same backward as forward?", "palindrome", "Starts with 'p'"),
            "normalize": ("What must be done to a string (like removing spaces) before checking if it is a true palindrome?", "normalize", "A nine-letter verb."),
            "yes": ("What is the answer for the number 121?", "yes", "A three-letter confirmation."),
            "slice": ("What Python trick can quickly reverse a string to check it?", "slice", "A five-letter operation."),
            "equality": ("What property must the reversed version of the string have?", "equality", "An eight-letter concept."),
            "same": ("What is the reverse of a single character?", "same", "A four-letter word."),

            # --- Fill-in: List Comp. (6 Questions) ---
            "List Comp.": ("Fill in the blank: [i ___ range(10)] to create a list from 0 to 9.", "for i in", "The word 'in' is one of the blanks."),
            "square_lc": ("What type of brackets are used to define a list comprehension?", "square", "A six-letter shape."),
            "if": ("What optional keyword can filter items within a comprehension?", "if", "A two-letter keyword."),
            "efficient": ("List comprehensions are generally more _ than traditional loops.", "efficient", "A nine-letter adjective."),
            "expression": ("What is the part of the comprehension before the for keyword?", "expression", "A ten-letter word."),
            "list": ("The result of a list comprehension is always what data type?", "list", "A four-letter data type."),

            # --- Fill-in: String Slice (6 Questions) ---
            "String Slice": ("Fill in the blank: my_str[2:] will return the string starting from the _ index.", "second", "An ordinal number."),
            "fifth": ("Fill in the blank: my_str[:5] returns the string up to the _ index (but not including it).", "fifth", "An ordinal number."),
            "step": ("What is the third, optional component of a slice (e.g., [::2])?", "step", "A four-letter word."),
            "end": ("What does a negative index (e.g., [-1]) access?", "end", "The opposite of the start."),
            "reverse": ("What is the result of my_str[::-1]?", "reverse", "A seven-letter action."),
            "slice_char": ("What character is used to separate the slice indices?", ":", "Same as the dictionary separator."),

            # --- Fill-in: Func Return (6 Questions) ---
            "Func Return": ("Fill in the blank: def add(a): ___ a + 1 to complete the function.", "return", "A keyword to send a value back."),
            "return value": ("What is the data sent back from a function called?", "return value", "Two words."),
            "return_kw": ("What keyword can be used to exit a function without returning a value (it returns None)?", "return", "The same keyword."),
            "multiple": ("A function can return how many values?", "multiple", "An eight-letter adjective."),
            "pure": ("A function that computes and gives back a result is called what?", "pure", "A four-letter adjective."),
            "calling": ("What is the process of getting the value from the function called?", "calling", "A seven-letter verb."),

            # --- Fill-in: Class Init (6 Questions) ---
            "Class Init": ("What method is automatically called when a new instance of a class is created? __ _ __", "init", "A special double-underscore method."),
            "del": ("What is the name of the method that cleans up when an object is destroyed? __ ___ __", "del", "A three-letter double-underscore method."),
            "class_init": ("What keyword is used to create a new object instance?", "class", "The name of the blueprint."),
            "constructor": ("What is the entire initialization method officially called?", "constructor", "An eleven-letter word."),
            "self_ci": ("What is the first argument of the _init_ method usually named?", "self", "A four-letter word."),
            "instance_ci": ("What is the term for the object that is created from the class blueprint?", "instance", "An eight-letter word."),

            # --- Fill-in: Try-Except (6 Questions) ---
            "Try-Except": ("Fill in the blank: try: x = 1 / 0 ___ ZeroDivisionError: print(\"Error\")", "except", "A keyword to catch the error."),
            "finally": ("What keyword executes code after the try block, regardless of errors?", "finally", "An eight-letter keyword."),
            "else_te": ("What keyword executes code only if the try block succeeds (no errors)?", "else", "Same as the conditional fallback."),
            "raise": ("What is the general keyword used to raise a user-defined error?", "raise", "A five-letter verb."),
            "exception": ("What is the term for a detected error during execution?", "exception", "A ten-letter word."),
            "try": ("Which block is where you place the code that might cause an error?", "try", "A three-letter keyword."),

            # --- Fill-in: File Open (6 Questions) ---
            "File Open": ("Fill in the blank: ___('file.txt', 'r') as f: to open a file.", "open", "A common built-in function."),
            "w": ("What character is the mode for writing (overwriting) to a file?", "w", "A single lowercase letter."),
            "r": ("What character is the mode for reading a file?", "r", "A single lowercase letter."),
            "a": ("What character is the mode for appending to a file?", "a", "A single lowercase letter."),
            "os": ("What is the name of the standard module for interacting with the operating system?", "os", "Two lowercase letters."),
            "with": ("What keyword is often used to ensure a file is closed after use?", "with", "A four-letter keyword."),

            # --- Fill-in: Dict Index (6 Questions) ---
            "Dict Index": ("Fill in the blank: Dictionaries are indexed by what?", "keys", "The name for the left side of the pair."),
            "items": ("What method returns a view object that displays a list of a dictionary's key-value tuple pairs?", "items", "A five-letter method."),
            "keyerror": ("What is the error raised when you try to access a non-existent key?", "keyerror", "An eight-letter error type."),
            "ordered": ("Dictionaries are always what (since Python 3.7)?", "ordered", "A seven-letter adjective."),
            "in": ("How do you check for the existence of a key in a dictionary?", "in", "A two-letter keyword."),
            "item": ("What is another name for a key-value pair?", "item", "A four-letter word."),

            # --- Fill-in: Set Add (6 Questions) ---
            "Set Add": ("Which method adds a single item to a set?", "add", "A three-letter method name."),
            "update": ("What method is used to add multiple iterable items to a set?", "update", "A six-letter method."),
            "hashable": ("The elements of a set must be what?", "hashable", "An eight-letter property."),
            "set_empty": ("How do you create an empty set (it's not {})?", "set", "A three-letter function."),
            "pop_set": ("What keyword is used to remove an arbitrary element from a set?", "pop", "A three-letter method."),
            "set_fn": ("What is the built-in function used to create a set from a list?", "set", "A three-letter function."),

            # --- Fill-in: Lambda (6 Questions) ---
            "Lambda": ("What is the keyword for an anonymous one-line function?", "lambda", "Starts with 'l'"),
            "lambda_kw": ("What keyword does a lambda function implicitly contain instead of return?", "lambda", "It's the same keyword."),
            "expression_l": ("A lambda function can only contain a single what?", "expression", "A ten-letter word."),
            "higher order": ("What are these functions most commonly used with (e.g., map and filter)?", "higher order", "Two words."),
            "higher order_l": ("What type of function takes one or more functions as arguments?", "higher order", "Same as the common usage."),
            "anonymous": ("What is a short, disposable function called?", "anonymous", "A nine-letter adjective."),

            # --- Fill-in: Tuple Brackets (6 Questions) ---
            "Tuple Brackets": ("Fill in the blank: Tuples use what type of brackets?", "parentheses", "Curved symbols."),
            "immutable_t": ("What is the defining characteristic of a tuple?", "immutable", "An nine-letter property."),
            "count": ("What method counts the number of times a value appears in a tuple?", "count", "A five-letter method."),
            "one": ("What is the smallest size a tuple can be (e.g., (1,))?", "one", "A three-letter number."),
            "unpacking": ("What is the process of extracting values from a tuple into separate variables called?", "unpacking", "A ten-letter word."),
            "comma": ("What must a one-element tuple end with to be recognized as a tuple?", "comma", "A five-letter punctuation."),

            # Fallback for topics not explicitly listed in the groups above:
            "Tuples": ("What is the defining characteristic of a tuple?", "immutable", "It starts with 'i'."),
            "Modules": ("What keyword is used to bring an external module into your script?", "import", "It starts with 'i'."),
            "JSON": ("What format is commonly used to send data from a server to a web page?", "json", "An acronym."),
            "Recursion": ("What is a function that calls itself called?", "recursion", "It starts with 'r'."),
            "Inheritance": ("What is the mechanism where one class acquires the properties of another?", "inheritance", "It starts with 'i'."),
            "Polymorphism": ("What is the ability of an object to take on many forms?", "polymorphism", "It starts with 'p'."),
            "Abstraction": ("What is the process of hiding the complex reality while exposing only the necessary parts?", "abstraction", "It starts with 'a'."),
            "Encapsulation": ("What is the concept of bundling data and the methods that operate on that data?", "encapsulation", "It starts with 'e'."),
        }

    def get_loot_table(self):
        # A 75% chance to get a silver key, 25% for a gold key
        return random.choices(["Silver Key", "Gold Key"], weights=[0.75, 0.25], k=1)

    # --- Typomancer Minigame ---
    def start_typomancer_minigame(self, npc_pos):
        self.unlocked_encyclopedia_entries.add("Typomancer")
        self.game_state = "minigame"
        self.minigame_words = random.sample([
            "python", "variable", "function", "string", "integer", "loop", "array", "class", "dictionary",
            "tuple", "method", "module", "library", "syntax", "error", "boolean", "import" "algorithm", "binary",
            "compiler", "database", "debug", "exception", "framework",
            "hardware", "index", "json", "kernel", "network", "object", "parameter", "query",
            "recursion", "software", "token", "unicode", "virtual", "balding", "java", "Turbo" "Algorithm",
            "Data structure", "Binary", "Bit", "Byte", "Compiler", "Interpreter", "Syntax", "Semantics", "Variable",
            "Function", "Loop", "Recursion", "Object-oriented", "Class", "Inheritance", "Polymorphism", "Encapsulation",
            "Abstraction", "Exception",
            "Agile", "Scrum", "Debugging", "Testing", "Version control", "Continuous integration", "Deployment", "API",
            "Library", "Framework",
            "Kernel", "Process", "Thread", "Scheduling", "Deadlock", "Semaphore", "File system", "Virtual memory",
            "Interrupt", "Cache",
            "CPU", "GPU", "RAM", "ROM", "Register", "Instruction set", "Pipeline", "Bus", "Clock cycle", "Parallelism",
            "Protocol", "TCP/IP", "Bandwidth", "Latency", "Router", "Switch", "Firewall", "Encryption",
            "Authentication", "Cybersecurity",
            "SQL", "Relational database", "Table", "Primary key", "Foreign key", "Index", "Query", "Transaction",
            "Normalization", "NoSQL",
            "Machine learning", "Neural network", "Deep learning", "Training set", "Testing set", "Overfitting",
            "Underfitting", "Natural language processing", "Reinforcement learning", "Big data",
            "IDE", "Git", "Repository", "Branch", "Merge", "Pull request", "Containerization", "Virtualization",
            "Docker", "Cloud computing",
            "Blockchain", "Quantum computing", "Internet of Things", "Edge computing", "Augmented reality",
            "Virtual reality", "Robotics", "Automation", "Cyber-physical systems", "5G", "Accumulator", "Address bus",
            "Address space", "ALU", "Arithmetic shift", "Assembly language", "Associative memory", "Barrel shifter",
            "Base register", "Benchmark",
            "BIOS", "Bitwise operation", "Branch prediction", "Cache coherence", "Cache line", "Chipset",
            "Clock signal", "Control bus", "Control unit", "Core",
            "Cycle time", "Data bus", "Direct memory access", "Dispatch unit", "Dynamic scheduling", "EEPROM",
            "Execution unit", "Fetch", "Floating-point unit", "Firmware",
            "Harvard architecture", "Instruction cache", "Instruction cycle", "Instruction pipeline",
            "Instruction set architecture", "Integrated circuit", "Interrupt vector", "I/O controller", "I/O device",
            "Level 1 cache",
            "Level 2 cache", "Level 3 cache", "Level 4 cache", "Logic gate", "Lookup table", "Main memory", "Memory address register",
            "Memory data register", "Memory hierarchy", "Memory latency", "Memory management unit",
            "Microarchitecture", "Microcode", "Microcontroller", "Microinstruction", "Microprocessor", "Multiprocessor",
            "Multiprogramming", "Nanotechnology", "Nanosecond", "Operand",
            "Opcode", "Out-of-order execution", "Parallel processor", "Parity bit", "Pipeline hazard", "Pipeline stall",
            "Power consumption", "Primary storage", "Program counter", "PROM",
            "Pseudoinstruction", "Read-only memory", "Register file", "RISC", "CISC", "Semiconductor",
            "Sequential logic", "Shift register", "SIMD", "Snooping",
            "Solid-state drive", "Speculative execution", "Stack pointer", "Static RAM", "Superscalar", "System bus",
            "Throughput", "Timing diagram", "Transistor", "Vector processor",
            "Virtual address", "Virtual machine", "Von Neumann architecture", "VLSI", "Word length", "Write-back cache",
            "Write-through cache", "XOR gate", "Yield", "Zero flag"
        ], 5)
        self.full_word_string = " ".join(self.minigame_words)
        self.minigame_start_time = time.time()

        self.minigame_window = tk.Toplevel(self.root)
        self.minigame_window.title("Typomancer Challenge")
        self.minigame_window.geometry("450x250")
        self.minigame_window.configure(bg="#1C1C1C")
        self.minigame_window.protocol("WM_DELETE_WINDOW", self.end_minigame)
        self.minigame_window.attributes('-topmost', True)
        
        # --- UI: Tree Wrapper ---
        self.main_frame = tk.Frame(
            self.minigame_window, 
            bg="#8B4513", 
            padx=10, pady=10, 
            relief="ridge", borderwidth=4
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.typo_label = tk.Label(self.main_frame, text="Typomancer's Challenge!", font=("Consolas", 16, "bold"),
                                   bg="#8B4513", fg="#00FFFF")
        self.typo_label.pack(pady=10)

        self.word_display = tk.Label(self.main_frame, text=self.full_word_string, font=("Consolas", 14),
                                     bg="#2B2B2B", fg="#33FF33", padx=10, pady=5)
        self.word_display.pack(pady=10)

        self.input_entry = tk.Entry(self.main_frame, font=("Consolas", 14), width=30)
        self.input_entry.pack(pady=5)
        self.input_entry.focus_set()
        self.input_entry.bind("<KeyRelease>", self.on_minigame_type)

        self.minigame_timer_label = tk.Label(self.main_frame, text="Time left: 7.50s", font=("Consolas", 12),
                                             bg="#8B4513",
                                             fg="#FF3366")
        self.minigame_timer_label.pack(pady=5)

        self.minigame_npc_pos = npc_pos
        self.update_minigame_timer()

    def update_minigame_timer(self):
        if not hasattr(self, 'minigame_window') or not self.minigame_window.winfo_exists():
            return
        time_left = 7.5 - (time.time() - self.minigame_start_time)
        if time_left <= 0:
            self.minigame_timer_label.config(text="Time's up!")
            self.end_minigame()
        else:
            self.minigame_timer_label.config(text=f"Time left: {time_left:.2f}s")
            self.minigame_window.after(50, self.update_minigame_timer)

    def on_minigame_type(self, event=None):
        if self.game_state != "minigame" or not self.minigame_window.winfo_exists():
            return
        typed_text = self.input_entry.get()
        if self.full_word_string.startswith(typed_text):
            remaining_text = self.full_word_string[len(typed_text):]
            self.word_display.config(text=remaining_text)
            self.input_entry.config(fg="black")

            if typed_text == self.full_word_string:
                self.end_minigame()
                return

        else:
            self.input_entry.config(fg="red")
            match_len = 0
            while match_len < len(typed_text) and self.full_word_string.startswith(typed_text[:match_len + 1]):
                match_len += 1
            remaining_text = self.full_word_string[match_len:]
            self.word_display.config(text=remaining_text)

    def end_minigame(self):
        if not hasattr(self, 'minigame_window') or not self.minigame_window.winfo_exists():
            return

        typed_text = self.input_entry.get().strip()
        self.minigame_window.destroy()

        typed_words_list = typed_text.split()
        correct_words = 0
        for i, target_word in enumerate(self.minigame_words):
            if i < len(typed_words_list) and typed_words_list[i].lower() == target_word.lower():
                correct_words += 1

        total_words = len(self.minigame_words)

        if correct_words > 0:
            exp_reward = correct_words * 5
            self.add_xp(exp_reward)

            loot_chance = random.random()
            if loot_chance <= 0.3:
                key = "Gold Key"
            else:
                key = "Silver Key"

            self.add_loot(key)
            messagebox.showinfo(
                "Challenge Complete",
                f"You typed {correct_words} out of {total_words} words correctly!\nYou earned {exp_reward} XP and a {key}!"
            )
        else:
            messagebox.showinfo("Challenge Failed",
                                "You didn't get any words correct. The Typomancer sighs and wishes you better luck next time.")

        if self.minigame_npc_pos in self.enemies:
            del self.enemies[self.minigame_npc_pos]

        self.game_state = "exploration"
        self.draw_map()
        self.update_status()


if __name__ == "__main__":
    # Create the main root window but hide it initially
    root = tk.Tk()
    root.withdraw()
    
    # Open the custom name selection window first
    # This class will handle its own creation, name input, and then
    # un-hide the root and start the RPGGame class.
    app = NameSelectionWindow(root)
    
    # Start the main application loop
    root.mainloop()