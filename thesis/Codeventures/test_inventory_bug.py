
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock tkinter and Pillow
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['PIL.ImageTk'] = MagicMock()
sys.modules['PIL.ImageDraw'] = MagicMock()
sys.modules['PIL.ImageFont'] = MagicMock()

import main

class TestInventoryBug(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        # Setup inventory with a potion
        self.game.inventory = ["Potion"]
        self.game.sword_img = MagicMock()
        self.game.pickaxe_img = MagicMock()
        self.game.silver_key_img = MagicMock()
        self.game.gold_key_img = MagicMock()
        self.game.slime_goo_img = MagicMock()
        self.game.goblin_axe_img = MagicMock()

    def test_display_inventory_potion(self):
        # This test ensures display_inventory_grid does not crash for Potion
        # which has no image and triggers the 'else' block.

        # Mock InventoryWindow
        with patch('tkinter.Toplevel'):
            inv_window = main.InventoryWindow(self.game)

            # The constructor calls display_inventory_grid
            # If there is an UnboundLocalError, it should raise here.

            # Let's verify buttons were created
            self.assertTrue(len(inv_window.slot_buttons) > 0)

            # Verify the button text for Potion (should be POT)
            # We can't easily check the text attribute of the mock button unless we inspected the calls
            # But the main goal is to ensure no exception was raised.

if __name__ == '__main__':
    unittest.main()
