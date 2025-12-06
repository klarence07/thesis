import unittest
import os
import sys
import sqlite3

# Add the directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import db_utils

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Ensure we start with a fresh DB or at least one that is initialized
        db_utils.init_db()

    def test_fetch_question(self):
        # Test fetching a known question
        result = db_utils.fetch_question("Control Flow")
        self.assertIsNotNone(result)
        # Unpack based on known schema (4 items)
        question, answer, hint, difficulty = result
        self.assertEqual(question, "What keyword starts a conditional block?")
        self.assertEqual(answer, "if")
        self.assertEqual(hint, "Starts with 'i'")
        self.assertEqual(difficulty, "Easy")

    def test_fetch_question_not_found(self):
        # Test fetching a non-existent question
        result = db_utils.fetch_question("NonExistentKey")
        self.assertIsNone(result)

    def test_fetch_all_questions(self):
        questions = db_utils.fetch_all_questions()
        self.assertTrue(len(questions) > 0)
        self.assertIn("Control Flow", questions)

    def test_leaderboard(self):
        # Clear leaderboard for testing
        conn = db_utils.get_db_connection()
        conn.execute("DELETE FROM leaderboard")
        conn.commit()
        conn.close()

        # Save scores
        db_utils.save_high_score("Player1", 100, 60.5, "Medium")
        db_utils.save_high_score("Player2", 200, 50.0, "Medium")
        db_utils.save_high_score("Player3", 150, 45.0, "Hard") # Different difficulty

        # Fetch leaderboard for Medium
        leaderboard = db_utils.get_leaderboard("Medium")

        # Check count
        self.assertEqual(len(leaderboard), 2)

        # Check order (Player2 should be first because higher score)
        self.assertEqual(leaderboard[0]['name'], "Player2")
        self.assertEqual(leaderboard[1]['name'], "Player1")

if __name__ == '__main__':
    unittest.main()
