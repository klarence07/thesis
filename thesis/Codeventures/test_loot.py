
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock tkinter and Pillow before importing main
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['PIL.ImageTk'] = MagicMock()
sys.modules['PIL.ImageDraw'] = MagicMock()
sys.modules['PIL.ImageFont'] = MagicMock()

# Now import main
import main

class TestRPGGameLoot(unittest.TestCase):
    def setUp(self):
        # Mock root
        self.root = MagicMock()
        # Mock db_utils to avoid database connection
        main.db_utils = MagicMock()

        # Instantiate game
        self.game = main.RPGGame(self.root, gender="boy", player_name="TestHero", difficulty="Easy")

        # Mock load_images to prevent file operations
        self.game.load_images = MagicMock()

    def test_add_loot_logic(self):
        # Mock LootDialog to prevent it from trying to create a window
        with patch('main.LootDialog') as MockLootDialog:
            item = "Sword"
            self.game.sword_img = MagicMock() # Mock the image

            self.game.add_loot(item)

            # Check inventory
            self.assertIn(item, self.game.inventory)

            # Check flag
            self.assertTrue(self.game.sword_acquired)

            # Check if LootDialog was called
            MockLootDialog.assert_called_once()

            # Verify correct image was passed
            args, kwargs = MockLootDialog.call_args
            self.assertEqual(kwargs['item_image'], self.game.sword_img)

if __name__ == '__main__':
    unittest.main()
