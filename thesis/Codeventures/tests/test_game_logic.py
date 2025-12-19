import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock tkinter and PIL before importing main
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['PIL.ImageTk'] = MagicMock()
sys.modules['PIL.ImageDraw'] = MagicMock()
sys.modules['PIL.ImageFont'] = MagicMock()

# Now we can import RPGGame
from main import RPGGame

class TestRPGGame(unittest.TestCase):
    def setUp(self):
        self.root = MagicMock()
        # Mock load_images to prevent file operations
        with patch('main.RPGGame.load_images'):
            with patch('main.RPGGame.generate_static_tiles'):
                with patch('main.RPGGame.generate_npc_positions'):
                    with patch('main.RPGGame.generate_enemies'):
                         with patch('main.RPGGame.generate_chests'):
                             with patch('main.RPGGame.draw_map'):
                                with patch('main.RPGGame.start_chase_loop'):
                                     self.game = RPGGame(self.root)

    def test_initial_state(self):
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.xp, 0)
        self.assertEqual(self.game.health, 100)

    def test_add_xp_level_up(self):
        # Level 1 requires 20 XP
        self.game.level = 1
        self.game.xp = 0
        self.game.add_xp(25)

        self.assertEqual(self.game.level, 2)
        self.assertEqual(self.game.xp, 5) # 25 - 20 = 5
        self.assertEqual(self.game.skill_points, 2)

    def test_take_damage(self):
        self.game.health = 100
        self.game.take_damage(10, "test_source")
        self.assertEqual(self.game.health, 90)

    def test_check_topic_complete(self):
        # Setup a dummy topic
        topic = "Test Topic"
        # Mock _get_topic_groups to return known keys
        self.game._get_topic_groups = MagicMock(return_value={topic: ["q1", "q2"]})

        self.game.asked_sub_questions = {"q1"}
        self.assertFalse(self.game.check_topic_complete(topic))

        self.game.asked_sub_questions.add("q2")
        self.assertTrue(self.game.check_topic_complete(topic))

if __name__ == '__main__':
    unittest.main()
