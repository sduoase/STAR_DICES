import unittest
import random

from monolith.classes.Die import Die
from monolith.classes.DiceSet import DiceSet, _throw_to_faces

class TestDie(unittest.TestCase):

    def test_single_die_single_face(self):
        die = Die(["1"], "test_theme")
        dice_set = DiceSet([die], "test_theme")
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["1"])
    
    def test_multi_die_single_face(self):
        die1 = Die(["1"], "test_theme")
        die2 = Die(["2"], "test_theme")
        dice_set = DiceSet([die1, die2], "test_theme")
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["1", "2"])
    
    def test_single_die_multi_face(self):
        random.seed(0) # 1, 1, 0, 1, 2, ...
        die = Die(["1", "2", "3"], "test_theme")
        dice_set = DiceSet([die], "test_theme")
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["2"])
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["2"])
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["1"])
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["2"])
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["3"])

    def test_multi_die_multi_face(self):
        random.seed(0) # 1, 1, 0, 1, 2, 1, ...
        die1 = Die(["1", "2", "3"], "test_theme")
        die2 = Die(["4", "5", "6"], "test_theme")
        dice_set = DiceSet([die1, die2], "test_theme")
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["2", "5"])
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["1", "5"])
        self.assertEqual(_throw_to_faces(dice_set.throw()), ["3", "5"])
