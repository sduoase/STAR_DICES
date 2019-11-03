import unittest
import random

from monolith.classes import Die, DiceSet
 
class TestDie(unittest.TestCase):

    def test_single_die_single_face(self):
        die = Die.Die([1])
        dice_set = DiceSet.DiceSet([die])
        self.assertEqual(dice_set.throw(), [1])
    
    def test_multi_die_single_face(self):
        die1 = Die.Die([1])
        die2 = Die.Die([2])
        dice_set = DiceSet.DiceSet([die1, die2])
        self.assertEqual(dice_set.throw(), [1, 2])
    
    def test_single_die_multi_face(self):
        random.seed(0) # 1, 1, 0, 1, 2, ...
        die = Die.Die([1, 2, 3])
        dice_set = DiceSet.DiceSet([die])
        self.assertEqual(dice_set.throw(), [2])
        self.assertEqual(dice_set.throw(), [2])
        self.assertEqual(dice_set.throw(), [1])
        self.assertEqual(dice_set.throw(), [2])
        self.assertEqual(dice_set.throw(), [3])

    def test_multi_die_multi_face(self):
        random.seed(0) # 1, 1, 0, 1, 2, 1, ...
        die1 = Die.Die([1, 2, 3])
        die2 = Die.Die([4, 5, 6])
        dice_set = DiceSet.DiceSet([die1, die2])
        self.assertEqual(dice_set.throw(), [2, 5])
        self.assertEqual(dice_set.throw(), [1, 5])
        self.assertEqual(dice_set.throw(), [3, 5])

 
if __name__ == '__main__':
    unittest.main()
