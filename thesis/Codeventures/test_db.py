import unittest
import os
import sys

# Add the directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import db_utils

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Ensure we start with a fresh DB or at least one that is initialized
        db_utils.init_db()

    def test_fetch_question(self):
        # Test fetching a known question
        question, answer, hint = db_utils.fetch_question("Control Flow")
        self.assertEqual(question, "What keyword starts a conditional block?")
        self.assertEqual(answer, "if")
        self.assertEqual(hint, "Starts with 'i'")

    def test_fetch_question_not_found(self):
        # Test fetching a non-existent question
        result = db_utils.fetch_question("NonExistentKey")
        self.assertIsNone(result)

    def test_fetch_all_questions(self):
        questions = db_utils.fetch_all_questions()
        self.assertTrue(len(questions) > 0)
        self.assertIn("Control Flow", questions)

if __name__ == '__main__':
    unittest.main()
