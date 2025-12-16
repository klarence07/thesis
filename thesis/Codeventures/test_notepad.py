
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock tkinter and Pillow before importing main
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock() # Mock ttk as well
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['PIL.ImageDraw'] = MagicMock()
sys.modules['PIL.ImageFont'] = MagicMock()
sys.modules['PIL.ImageTk'] = MagicMock()

import main
import db_utils

class TestAnswerKeyWindow(unittest.TestCase):
    def setUp(self):
        # Mock database calls
        self.mock_db_utils = MagicMock()
        main.db_utils = self.mock_db_utils
        main.db_utils.fetch_all_questions.return_value = {
            "key1": ("Question 1", "Answer 1", "Hint 1", "Easy"),
            "key2": ("Question 2", "Answer 2", "Hint 2", "Hard"),
        }

        # Mock TK root
        self.root = MagicMock()

        # Instantiate game
        self.game = main.RPGGame(self.root)
        self.game._get_topic_groups = MagicMock(return_value={
            "Topic A": ["key1"],
            "Topic B": ["key2"]
        })

    def test_notepad_initialization(self):
        # Instantiate the window
        notepad = main.AnswerKeyWindow(self.game)

        # Check if fetch_all_questions was called
        main.db_utils.fetch_all_questions.assert_called_once()

        # Check if treeview inserts were called (simulating data loading)
        # We can't easily check the structure without a real Tkinter,
        # but we can check if `self.tree.insert` was called.
        self.assertTrue(notepad.tree.insert.called)

        # Expect 2 topics + 2 questions = 4 calls minimum
        self.assertGreaterEqual(notepad.tree.insert.call_count, 4)

if __name__ == '__main__':
    unittest.main()
