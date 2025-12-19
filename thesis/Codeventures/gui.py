import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
import sys
import db_utils
from assets import get_base_path
# We avoid importing main or RPGGame here to prevent circular dependency
# Instead, we assume the 'game' object passed has the necessary attributes/methods.

# Constants for Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Handle Audio (Prevent crash if not on Windows)
try:
    import winsound
    AUDIO_ENABLED = True
except ImportError:
    AUDIO_ENABLED = False


class InventoryWindow:
    def __init__(self, game):
        self.game = game
        self.window = tk.Toplevel(game.root)
        self.window.title("Inventory")
        self.window.geometry("450x550")
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

    def get_image_path(self, item_name):
        base_dir = get_base_path()
        filename = None
        if "Silver Key" in item_name: filename = "silver_key.png"
        elif "Gold Key" in item_name: filename = "gold_key.png"
        elif "Sword" in item_name: filename = "sword.png"
        elif "Pickaxe" in item_name: filename = "pickaxe.png"
        elif "Goblin Axe" in item_name: filename = "goblin_axe.png"
        elif "Slime Goo" in item_name: filename = "slime_goo.png"
        elif "Potion" in item_name: filename = "potion.png"

        if filename:
            path = os.path.join(base_dir, filename)
            if os.path.exists(path):
                return path
            path = os.path.join(base_dir, "assets", filename)
            if os.path.exists(path):
                return path
        return None

    def load_item_image(self, item_name, size):
        path = self.get_image_path(item_name)
        if path:
            try:
                img = Image.open(path).resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image for {item_name}: {e}")
                return None
        return None

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

                    img = self.load_item_image(item_name, (40, 40))

                    btn_kwargs = {
                        "text": btn_text if not img else "",
                        "bg": "#1C1C1C",
                        "fg": item_color,
                        "font": btn_font,
                        "compound": "center",
                        "command": lambda name=item_name: self.show_item_actions(name)
                    }

                    if img:
                        btn_kwargs["image"] = img
                    else:
                        btn_kwargs["width"] = 5
                        btn_kwargs["height"] = 2

                    btn = tk.Button(slot_container, **btn_kwargs)
                    if img:
                        btn.image = img
                        btn.config(width=44, height=44)

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

        img = self.load_item_image(item_name, (100, 100))
        if img:
            lbl = tk.Label(self.action_frame, image=img, bg="#8B4513")
            lbl.image = img
            lbl.pack(pady=5)

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


class CombatMiniGameWindow:
    def __init__(self, game, enemy_pos):
        self.game = game
        self.enemy_pos_map = enemy_pos
        self.enemy_data = self.game.enemies[enemy_pos]
        self.game.game_state = "combat_minigame"
        self.game.unlocked_encyclopedia_entries.add(self.enemy_data.name)

        self.window = tk.Toplevel(self.game.root)
        self.window.title(f"Combat: {self.enemy_data.name}")
        self.window.geometry("450x500")
        self.window.configure(bg="#1C1C1C")
        # Prevent closing via X to ensure combat is resolved
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.attributes('-topmost', True)
        self.window.grab_set()

        # UI
        self.main_frame = tk.Frame(self.window, bg="#8B4513", padx=10, pady=10, relief="ridge", borderwidth=4)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.info_label = tk.Label(self.main_frame, text=f"Outrun the {self.enemy_data.name}!", font=("Consolas", 14, "bold"), bg="#8B4513", fg="#00FFFF")
        self.info_label.pack(pady=5)

        self.status_label = tk.Label(self.main_frame, text="Dodges: 0/3", font=("Consolas", 12), bg="#8B4513", fg="#33FF33")
        self.status_label.pack(pady=5)

        self.canvas = tk.Canvas(self.main_frame, width=400, height=400, bg="#222222", highlightthickness=2, highlightbackground="#333333")
        self.canvas.pack()

        self.grid_size = 8
        self.cell_size = 50
        self.player_local_pos = [0, 0]
        self.enemy_local_pos = [7, 7]
        self.player_dodges = 0
        self.max_dodges = 3

        self.draw_minigame()

        self.window.bind("<Key>", self.on_key)
        self.window.focus_force()

        self.game.root.after(1000, self.enemy_move_step)

    def draw_minigame(self):
        self.canvas.delete("all")

        # Draw Player
        px, py = self.player_local_pos
        self.canvas.create_image(px * self.cell_size + 25, py * self.cell_size + 25, image=self.game.player_img)

        # Draw Enemy
        ex, ey = self.enemy_local_pos
        enemy_img = self.game.enemy_img if self.enemy_data.name == "Slime" else self.game.goblin_img
        self.canvas.create_image(ex * self.cell_size + 25, ey * self.cell_size + 25, image=enemy_img)

    def on_key(self, event):
        key = event.keysym.lower()
        dx, dy = 0, 0
        if key in ("up", "w"): dy = -1
        elif key in ("down", "s"): dy = 1
        elif key in ("left", "a"): dx = -1
        elif key in ("right", "d"): dx = 1

        nx, ny = self.player_local_pos[0] + dx, self.player_local_pos[1] + dy
        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
            # Check if walking into enemy
            if [nx, ny] == self.enemy_local_pos:
                self.game_over_combat("caught")
            else:
                self.player_local_pos = [nx, ny]
                self.draw_minigame()

    def enemy_move_step(self):
        if not self.window.winfo_exists(): return

        # Move towards player
        dx = self.player_local_pos[0] - self.enemy_local_pos[0]
        dy = self.player_local_pos[1] - self.enemy_local_pos[1]

        if dx != 0:
            self.enemy_local_pos[0] += 1 if dx > 0 else -1
        elif dy != 0:
            self.enemy_local_pos[1] += 1 if dy > 0 else -1

        self.draw_minigame()

        if self.enemy_local_pos == self.player_local_pos:
            self.game_over_combat("caught")
        else:
            self.player_dodges += 1
            self.status_label.config(text=f"Dodges: {self.player_dodges}/{self.max_dodges}")

            if self.player_dodges >= self.max_dodges:
                self.game_over_combat("win")
            else:
                delay = 800 if self.enemy_data.name == "Goblin" else 500
                self.game.root.after(delay, self.enemy_move_step)

    def game_over_combat(self, result):
        self.window.destroy()
        self.game.game_state = "exploration"

        if result == "win":
            self.game.info_label.config(text=f"You successfully outran the {self.enemy_data.name}!")
            self.game.add_xp(self.enemy_data.xp_reward)
            self.game.add_loot(self.enemy_data.loot)
            if self.enemy_pos_map in self.game.enemies:
                del self.game.enemies[self.enemy_pos_map]
            if AUDIO_ENABLED:
                self.game.play_sound("victory.wav")
        else:
             self.game.info_label.config(text=f"The {self.enemy_data.name} caught you!")
             if self.enemy_data.name == "Goblin":
                 self.game.take_damage(self.game.health, "goblin-caught")
             else:
                 self.game.take_damage(self.enemy_data.damage, "Slime")

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


class LeaderboardWindow:
    def __init__(self, game):
        self.game = game
        self.previous_state = self.game.game_state
        self.game.game_state = "menu"
        self.window = tk.Toplevel(game.root)
        self.window.title("Leaderboard")
        self.window.geometry("500x400")
        self.window.configure(bg="#1C1C1C")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- UI: Wrapper ---
        self.main_frame = tk.Frame(
            self.window,
            bg="#8B4513",
            padx=10, pady=10,
            relief="ridge", borderwidth=4
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.main_frame, text=f"Leaderboard ({self.game.difficulty})", font=("Consolas", 16, "bold"), bg="#8B4513", fg="#33FF33").pack(pady=10)

        # Scrollable Frame
        self.canvas = tk.Canvas(self.main_frame, bg="#2B2B2B", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2B2B2B")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=5)

        self.load_leaderboard()

        self.close_btn = tk.Button(self.main_frame, text="Close Game", command=self.window.destroy, bg="#FF3366", fg="#1C1C1C", font=("Consolas", 12, "bold"))
        self.close_btn.pack(pady=10)
        self.close_btn.config(command=self.close_and_quit)

        self.reset_btn = tk.Button(self.main_frame, text="Reset Leaderboard", command=self.reset_leaderboard, bg="#FFD700", fg="#1C1C1C", font=("Consolas", 10, "bold"))
        self.reset_btn.pack(pady=5)

    def reset_leaderboard(self):
        username = simpledialog.askstring("Admin Login", "Enter Admin Username:")
        if not username:
            return

        password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show="*")
        if not password:
            return

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the leaderboard? This cannot be undone."):
                db_utils.reset_leaderboard()
                messagebox.showinfo("Success", "Leaderboard has been reset.")
                self.load_leaderboard()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def load_leaderboard(self):
        scores = db_utils.fetch_leaderboard(self.game.difficulty)

        # Clear existing widgets in scrollable_frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Header
        header_frame = tk.Frame(self.scrollable_frame, bg="#2B2B2B")
        header_frame.pack(fill="x", pady=2)
        tk.Label(header_frame, text="Rank", width=5, bg="#2B2B2B", fg="#FFD700", font=("Consolas", 10, "bold")).pack(side="left")
        tk.Label(header_frame, text="Name", width=15, bg="#2B2B2B", fg="#FFD700", font=("Consolas", 10, "bold")).pack(side="left")
        tk.Label(header_frame, text="Score (XP)", width=10, bg="#2B2B2B", fg="#FFD700", font=("Consolas", 10, "bold")).pack(side="left")
        tk.Label(header_frame, text="Time (s)", width=10, bg="#2B2B2B", fg="#FFD700", font=("Consolas", 10, "bold")).pack(side="left")

        for idx, row in enumerate(scores, 1):
            row_frame = tk.Frame(self.scrollable_frame, bg="#2B2B2B")
            row_frame.pack(fill="x", pady=2)

            fg_color = "#33FF33" if row['name'] == self.game.player_name else "#FFFFFF"

            tk.Label(row_frame, text=f"{idx}", width=5, bg="#2B2B2B", fg=fg_color, font=("Consolas", 10)).pack(side="left")
            tk.Label(row_frame, text=f"{row['name']}", width=15, bg="#2B2B2B", fg=fg_color, font=("Consolas", 10)).pack(side="left")
            tk.Label(row_frame, text=f"{row['score']}", width=10, bg="#2B2B2B", fg=fg_color, font=("Consolas", 10)).pack(side="left")
            tk.Label(row_frame, text=f"{row['time_taken']}", width=10, bg="#2B2B2B", fg=fg_color, font=("Consolas", 10)).pack(side="left")

    def on_close(self):
        self.game.game_state = self.previous_state
        self.window.destroy()

    def close_and_quit(self):
        self.window.destroy()
        self.game.root.quit()


class NameSelectionWindow:
    """Custom window to input player name and choose gender before starting the main game."""
    def __init__(self, master, game_class):
        self.master = master
        self.game_class = game_class
        # self.master.withdraw() # We withdraw in __main__
        self.window = tk.Toplevel(master)
        self.window.title("Character Creation")
        self.window.geometry("380x300")
        self.window.configure(bg="#1C1C1C")
        self.window.resizable(False, False)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
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

        tk.Label(
            self.main_frame,
            text="SELECT DIFFICULTY",
            font=("Consolas", 12),
            bg="#8B4513",
            fg="#FFD700"
        ).pack(pady=(20, 10))

        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_frame = tk.Frame(self.main_frame, bg="#8B4513")
        difficulty_frame.pack()

        for diff in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(
                difficulty_frame,
                text=diff,
                variable=self.difficulty_var,
                value=diff,
                bg="#8B4513",
                fg="#33FF33",
                selectcolor="#2B2B2B",
                font=("Consolas", 10, "bold")
            ).pack(side="left", padx=10)

    def on_close(self):
        """Handle window closure."""
        self.window.destroy()
        self.master.destroy()
        sys.exit()

    def start_game(self, gender):
        player_name = self.name_entry.get().strip()
        if not player_name:
            player_name = "Hero"

        difficulty = self.difficulty_var.get()

        self.window.destroy()
        self.master.deiconify()

        game = self.game_class(self.master, gender=gender, player_name=player_name, difficulty=difficulty)
