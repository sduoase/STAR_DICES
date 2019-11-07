import unittest
import random
import os

from monolith.classes.Die import Die
 
class TestDie(unittest.TestCase):

    def test_empty_die(self):
        self.assertRaises(ValueError, Die, [], "test_theme")
    
    def test_single_face_die(self):
        random.seed(0) # 1, 1, 0, 1, 2, ...
        die = Die(["1"], "test_theme")
        self.assertEqual(die.throw()[0], "1")

    def test_multi_face_die(self):
        random.seed(0) # 1, 1, 0, 1, 2, ...
        die = Die(["1", "2", "3"], "test_theme")
        self.assertEqual(die.throw()[0], "2")
        self.assertEqual(die.throw()[0], "2")
        self.assertEqual(die.throw()[0], "1")
        self.assertEqual(die.throw()[0], "2")
        self.assertEqual(die.throw()[0], "3")
    
    def test_die_to_str(self):
        die = Die(["1", "2", "3"], "test_theme")
        self.assertEqual(str(die), "['1', '2', '3']")
