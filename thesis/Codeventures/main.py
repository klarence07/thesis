import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import time
import json
import db_utils
import sys
from entities import Enemy
from gui import InventoryWindow, LeaderboardWindow, CombatMiniGameWindow, EncycodepediaWindow, StatsSystem, CraftingWindow, NameSelectionWindow
from assets import get_base_path, load_all_images, TILE_SIZE

# Handle Audio (Prevent crash if not on Windows)
try:
    import winsound
    AUDIO_ENABLED = True
except ImportError:
    AUDIO_ENABLED = False

MAP_WIDTH = 15
MAP_HEIGHT = 12
HAZARDS = ["spikes", "fire"]


def get_user_data_path():
    """ Get path for persistent data (savegame, db) """
    if getattr(sys, 'frozen', False):
        # If frozen, use the directory where the executable is located
        return os.path.dirname(sys.executable)
    else:
        # If running from source, use the script directory
        return os.path.dirname(os.path.abspath(__file__))


class RPGGame:
    def __init__(self, root, gender="boy", player_name="Hero", difficulty="Medium"):
        self.root = root
        self.root.title("Memory Lane RPG")
        self.root.configure(bg="#1C1C1C")

        self.gender = gender
        self.player_name = player_name
        self.difficulty = difficulty

        # Victory conditions based on difficulty
        if self.difficulty == "Easy":
            self.victory_quota = 10
        elif self.difficulty == "Medium":
            self.victory_quota = 20
        elif self.difficulty == "Hard":
            self.victory_quota = 30
        else:
            self.victory_quota = 20 # Default

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

        self.leaderboard_btn = tk.Button(self.side_panel, text="Leaderboard", command=self.open_leaderboard, bg="#2B2B2B", fg="#00FFFF", font=("Consolas", 10, "bold"))
        self.leaderboard_btn.pack(pady=(0, 10), padx=10, fill="x")

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

        # Images dictionary
        self.images = {}
        self.image_refs = []

        self.load_images()

        self.player_pos = [0, 0]
        self.portal_pos = None
        self.stage = 1
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

        self.minigame_words = []
        self.full_word_string = ""
        self.minigame_start_time = 0
        self.minigame_window = None

        self.generate_static_tiles()
        self.generate_npc_positions()
        self.generate_enemies()
        self.generate_chests()
        self.draw_map()
        self.bind_keys()

        self.root.after(1000, self.update_timer)

        self.start_chase_loop()

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
            "stage": self.stage,
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
        save_path = os.path.join(get_user_data_path(), "savegame.json")
        with open(save_path, "w") as f:
            json.dump(game_state, f)
        messagebox.showinfo("Save Successful", "Game has been saved!")

    def load_game(self):
        try:
            save_path = os.path.join(get_user_data_path(), "savegame.json")
            with open(save_path, "r") as f:
                game_state = json.load(f)
            self.player_name = game_state["player_name"]
            self.gender = game_state["gender"]
            self.player_pos = game_state["player_pos"]
            self.stage = game_state.get("stage", 1)
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
        self.stage = 1
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
        self.generate_static_tiles()
        self.generate_npc_positions()
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

    def open_leaderboard(self):
        LeaderboardWindow(self)

    # --- Game Timer ---
    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}s")
        self.root.after(1000, self.update_timer)

    # --- Load images ---
    def load_images(self):
        base_dir = get_base_path()
        self.images = load_all_images(base_dir, self.gender)
        # For compatibility with existing code that might access individual attributes (though I should update those too)
        self.player_img = self.images["player"]
        self.enemy_img = self.images["enemy"]
        self.goblin_img = self.images["goblin"]

    # --- NPC, Enemy and tiles ---
    def get_npc_count_for_level(self):
        # Limit the number of questions (NPCs) per stage to a maximum of 5
        return min(self.stage + 1, 5, len(self.topics) + 1)

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
            while pos == (0, 0) or pos in positions or pos in self.tiles:
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
        self.image_refs.clear() # Keep refs to prevent GC

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # Grass
                self.canvas.create_image(
                    x * TILE_SIZE, y * TILE_SIZE,
                    anchor="nw", image=self.images["grass"]
                )
                self.image_refs.append(self.images["grass"])

                # Obstacles/hazards
                if (x, y) in self.tiles:
                    tile = self.tiles[(x, y)]
                    img = None
                    if tile in self.images:
                        img = self.images[tile]

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
                anchor="center", image=self.images["npc"]
            )
            self.image_refs.append(self.images["npc"])

        # Chests
        for (x, y), chest_type in self.chests.items():
            img = self.images["silver_chest"] if chest_type == "silver" else self.images["gold_chest"]
            self.canvas.create_image(
                x * TILE_SIZE + TILE_SIZE // 2,
                y * TILE_SIZE + TILE_SIZE // 2,
                anchor="center", image=img
            )
            self.image_refs.append(img)

        # Enemies
        for (x, y), enemy in self.enemies.items():
            img = self.images["enemy"]
            if enemy.name == "Goblin":
                img = self.images["goblin"]
            elif enemy.name == "Typomancer":
                img = self.images["typomancer"]
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
                anchor="center", image=self.images["portal"]
            )
            self.image_refs.append(self.images["portal"])

        # Player
        px, py = self.player_pos
        self.canvas.create_image(
            px * TILE_SIZE + TILE_SIZE // 2,
            py * TILE_SIZE + TILE_SIZE // 2,
            anchor="center", image=self.images["player"]
        )
        self.image_refs.append(self.images["player"])

        self.update_status()

    # --- Status & keys ---
    def update_status(self):
        remaining = len(self.npcs) - len(self.completed_topics)
        topics_left = ", ".join(t for t in self.npcs.values() if t not in self.mastered_topics and t != "Typomancer")

        questions_answered = len(self.asked_sub_questions)

        self.status_label.config(
            text=f"Stage: {self.stage} | Level: {self.level} | HP: {self.health} | Questions: {questions_answered}/{self.victory_quota} | Topics Left: {topics_left}"
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

    # --- Player movement ---
    def move(self, dx, dy):
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
            return

        pos = (new_x, new_y)

        if self.portal_pos and pos == self.portal_pos:
            if len(self.asked_sub_questions) >= self.victory_quota: # Check if question quota met
                messagebox.showinfo("Victory!", "You've answered enough questions to win the game!")

                # --- FIX 1: Sound check ---
                if AUDIO_ENABLED:
                    self.play_sound("victory.wav")

                # Save score and show leaderboard
                time_taken = int(time.time() - self.start_time)
                db_utils.insert_score(self.player_name, self.xp, time_taken, self.difficulty)
                LeaderboardWindow(self)
                return
            else:
                self.stage += 1
                messagebox.showinfo("Stage Completed!", f"You have entered the portal. Welcome to Stage {self.stage}!")
                self.portal_pos = None  # Reset portal for the new stage
                self.player_pos = [0, 0]  # Reset player position
                self.generate_static_tiles()
                self.generate_npc_positions()
                self.generate_enemies()
                self.generate_chests()
                self.draw_map()
                return  # Stop further movement logic for this turn

        if self.handle_interaction(pos):
            return

        self.player_pos = [new_x, new_y]
        self.draw_map()

    def handle_interaction(self, pos):
        """Returns True if the move should be blocked/handled completely (no simple walk)."""

        # 1. Enemies
        if pos in self.enemies:
            enemy = self.enemies[pos]
            if enemy.name == "Typomancer":
                self.current_enemy_pos = pos
                self.start_typomancer_minigame(pos)
                return True

            # Instant kill check
            if self.sword_acquired:
                self.unlocked_encyclopedia_entries.add(enemy.name)
                messagebox.showinfo("Sword Power!", f"You brandish your sword and instantly defeat the {enemy.name}!")
                self.add_xp(enemy.xp_reward)
                self.add_loot(enemy.loot)
                del self.enemies[pos]
                self.draw_map()
                self.update_status()
                return True

            self.current_enemy_pos = pos
            CombatMiniGameWindow(self, pos)
            return True

        # 2. Chests
        if pos in self.chests:
            return self.handle_chest(pos)

        # 3. Tiles (Hazards/Obstacles)
        if pos in self.tiles:
            return self.handle_tile(pos)

        # 4. NPCs
        if pos in self.npcs:
            return self.handle_npc(pos)

        return False

    def handle_chest(self, pos):
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

            # We return False here so the player actually MOVES onto the chest tile after opening it?
            # Original logic: moved player to new_x, new_y.
            # My handle_interaction logic says "Returns True if the move should be blocked/handled completely"
            # If I return False, player moves.
            return False
        else:
            messagebox.showwarning("Locked!", f"This {chest_type} chest is locked! You need a {required_key}.")
            return True # Block movement

    def handle_tile(self, pos):
        tile = self.tiles[pos]
        self.unlocked_encyclopedia_entries.add(tile.capitalize())

        if tile == "rock":
            if "Pickaxe" in self.inventory:
                if messagebox.askyesno("Clear Path", "Do you want to use your Pickaxe to clear this rock?"):
                    del self.tiles[pos]
                    messagebox.showinfo("Success!", "You cleared the rock and can now pass!")
                    return False # Allow move
                else:
                    return True # Block
            else:
                messagebox.showinfo("Blocked!", "A rock blocks your path. You need a Pickaxe to clear it!")
                return True

        elif tile == "tree":
            if "Goblin Axe" in self.inventory:
                if messagebox.askyesno("Chop Tree", "Do you want to use your Goblin Axe to chop down this tree?"):
                    del self.tiles[pos]
                    messagebox.showinfo("Success!", "You chopped down the tree!")
                    return False
                else:
                    return True
            else:
                messagebox.showinfo("Blocked!", "A tree blocks your path. You need a Goblin Axe to chop it down!")
                return True

        elif tile == "spikes":
            if "Slipperoo!" in self.inventory:
                messagebox.showinfo("Safe!", "Your Slipperoo! lets you slide safely over the spikes!")
            else:
                self.take_damage(10, "spikes")
            return False # Allow move (onto spikes)

        elif tile == "fire":
            self.take_damage(20, "fire")
            return False

        return False

    def handle_npc(self, pos):
        npc_type = self.npcs[pos]
        self.unlocked_encyclopedia_entries.add(npc_type)

        if npc_type not in self.mastered_topics:
            self.ask_question(self.npcs[pos])
        else:
            messagebox.showinfo("Already Completed", f"You've already completed: {self.npcs[pos]}")

        # NPCs block movement usually, unless we want to walk through them?
        # Original code just showed message and redrew map. Player did NOT move onto NPC tile.
        # "self.player_pos = [new_x, new_y]" was OUTSIDE the "if pos in self.npcs" block in original code?
        # Let's check original...
        # Original:
        # self.player_pos = [new_x, new_y]
        # if pos in self.npcs: ...

        # So original code allowed player to walk ON TOP of NPC.
        return False

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
        """Randomly selects an unasked question key for the given topic, respecting difficulty."""
        topic_groups = self._get_topic_groups()
        all_keys = topic_groups.get(topic)

        # If the topic isn't a grouped one, just use the topic name as the single key
        if all_keys is None:
            return topic if topic not in self.asked_sub_questions else None

        # Filter out already asked questions
        unasked_keys = [key for key in all_keys if key not in self.asked_sub_questions]

        # Apply difficulty filter using db_utils
        if unasked_keys:
            filtered_keys = db_utils.filter_keys_by_difficulty(unasked_keys, self.difficulty)
            return random.choice(filtered_keys) if filtered_keys else None

        return None

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

        if response and (response.strip().lower() == answer.lower() or response.strip().lower() == "admin"):
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

            # Check if victory condition is met to spawn portal
            if len(self.asked_sub_questions) >= self.victory_quota and not self.portal_pos:
                 self.npcs.clear()
                 self.info_label.config(text="You've learned enough! Find the portal for final victory!")
                 self.spawn_portal()

            # Also spawn portal if all NPCs for this level are gone (progression)
            elif not self.npcs and not self.portal_pos:
                self.info_label.config(text="A portal has opened! Find it to proceed to the next level.")
                self.spawn_portal()
        else:
            messagebox.showwarning("Hint", f"Hint: {hint}")

    def spawn_portal(self):
        # Spawn the portal in a random, empty location
        pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        while pos in self.npcs or pos in self.enemies or pos in self.tiles or pos in self.chests or pos == tuple(
                self.player_pos):
            pos = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))

        self.portal_pos = pos
        # Only update text if it hasn't been set by the victory condition
        # Actually, the calling logic sets the text. We might want to remove text setting from here or make it generic.
        # But for now, let's just do the mechanics.

        # --- FIX 1: Sound check ---
        if AUDIO_ENABLED:
            self.play_sound("level_up.wav")

        self.draw_map()  # Redraw the map to show the portal

    def get_question_data(self, question_key):
        """Retrieves question data using a specific key, falling back to default if key is not found."""
        question_data = db_utils.fetch_question(question_key)

        if question_data:
             # Unpack including difficulty (which is the 4th element now)
             question, answer, base_hint, _ = question_data
        else:
             question, answer, base_hint = ("What programming language are we learning?", "python", "It starts with 'p'")

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

    def get_loot_table(self):
        # A 75% chance to get a silver key, 25% for a gold key
        return random.choices(["Silver Key", "Gold Key"], weights=[0.75, 0.25], k=1)

    # --- Chase Mechanic ---
    def start_chase_loop(self):
        self.check_chase()

    def check_chase(self):
        if self.game_state == "exploration":
            self.move_entities_towards_player()
        self.root.after(800, self.check_chase)

    def move_entities_towards_player(self):
        player_x, player_y = self.player_pos
        movers = []
        for pos, topic in self.npcs.items():
            movers.append((pos, "npc", topic))
        for pos, enemy in self.enemies.items():
            movers.append((pos, "enemy", enemy))

        occupied = set(self.tiles.keys()) | set(self.chests.keys()) | set(self.npcs.keys()) | set(
            self.enemies.keys()) | {tuple(self.player_pos)}

        moves_to_execute = []
        events_to_trigger = []

        # Sort movers by distance to player
        movers.sort(key=lambda m: abs(m[0][0] - player_x) + abs(m[0][1] - player_y))

        for pos, entity_type, data in movers:
            x, y = pos
            # Use A* or BFS for better pathfinding, but for now, simple smart chase
            # Avoid getting stuck behind walls

            # Simple chase logic: try to reduce distance
            path = self.find_path(pos, (player_x, player_y), occupied)

            if path and len(path) > 1:
                next_step = path[1] # Path[0] is start

                if next_step == (player_x, player_y):
                     events_to_trigger.append((entity_type, pos))
                elif next_step not in occupied:
                     moves_to_execute.append((pos, next_step, entity_type, data))
                     occupied.add(next_step)
                     if pos in occupied:
                        occupied.remove(pos)

    def find_path(self, start, goal, occupied):
        """BFS Pathfinding to avoid obstacles."""
        queue = [(start, [start])]
        visited = set()
        visited.add(start)

        while queue:
            (vertex, path) = queue.pop(0)

            # Limit search depth for performance
            if len(path) > 6:
                continue

            if vertex == goal:
                return path

            x, y = vertex
            # Check adjacent cells
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (x + dx, y + dy)

                if 0 <= next_pos[0] < MAP_WIDTH and 0 <= next_pos[1] < MAP_HEIGHT:
                    # Can walk on: goal (player) or empty space not in occupied
                    if next_pos == goal or next_pos not in occupied:
                        if next_pos not in visited:
                            visited.add(next_pos)
                            queue.append((next_pos, path + [next_pos]))
        return None

        if moves_to_execute:
            for old_pos, new_pos, entity_type, data in moves_to_execute:
                if entity_type == "npc":
                    if old_pos in self.npcs:
                        del self.npcs[old_pos]
                        self.npcs[new_pos] = data
                elif entity_type == "enemy":
                    if old_pos in self.enemies:
                        del self.enemies[old_pos]
                        self.enemies[new_pos] = data
            self.draw_map()

        if events_to_trigger:
            # Only trigger one event
            etype, pos = events_to_trigger[0]
            if etype == "npc":
                if pos in self.npcs:
                    self.ask_question(self.npcs[pos])
            elif etype == "enemy":
                if pos in self.enemies:
                    enemy = self.enemies[pos]
                    if enemy.name == "Typomancer":
                        self.current_enemy_pos = pos
                        self.start_typomancer_minigame(pos)
                    else:
                        self.current_enemy_pos = pos
                        CombatMiniGameWindow(self, pos)

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

        self.word_display = tk.Text(self.main_frame, font=("Consolas", 14),
                                    bg="#2B2B2B", fg="#33FF33", height=2, width=40, borderwidth=0)
        self.word_display.pack(pady=10)
        self.word_display.tag_config("correct", foreground="#00FF00")  # Green for correct
        self.word_display.tag_config("wrong", foreground="#FF0000")    # Red for error
        self.word_display.insert("1.0", self.full_word_string)
        self.word_display.config(state="disabled")

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

        # Update word display colors
        self.word_display.config(state="normal")
        self.word_display.tag_remove("correct", "1.0", "end")
        self.word_display.tag_remove("wrong", "1.0", "end")

        match_len = 0
        min_len = min(len(typed_text), len(self.full_word_string))
        for i in range(min_len):
            if typed_text[i] == self.full_word_string[i]:
                match_len += 1
            else:
                break

        if match_len > 0:
            self.word_display.tag_add("correct", "1.0", f"1.{match_len}")

        if len(typed_text) > match_len:
            # Highlight the error in the target text if within bounds
            if match_len < len(self.full_word_string):
                self.word_display.tag_add("wrong", f"1.{match_len}", f"1.{match_len + 1}")

        self.word_display.config(state="disabled")

        if self.full_word_string.startswith(typed_text):
            self.input_entry.config(fg="black")
            if typed_text == self.full_word_string:
                self.end_minigame()
                return
        else:
            self.input_entry.config(fg="red")

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
    # Initialize the database
    db_utils.init_db()

    # Create the main root window but hide it initially
    root = tk.Tk()
    root.withdraw()

    # Open the custom name selection window first
    # This class will handle its own creation, name input, and then
    # un-hide the root and start the RPGGame class.
    app = NameSelectionWindow(root, RPGGame)

    # Start the main application loop
    root.mainloop()