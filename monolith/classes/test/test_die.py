import unittest
import random

from monolith.classes import Die, DiceSet
 
class TestDie(unittest.TestCase):

    def test_empty_die(self):
        self.assertRaises(ValueError, Die.Die, [])
    
    def test_single_face_die(self):
        die = Die.Die([1])
        self.assertEqual(die.throw(), 1)

    def test_multi_face_die(self):
        random.seed(0) # 1, 1, 0, 1, 2, ...
        die = Die.Die([1, 2, 3])
        self.assertEqual(die.throw(), 2)
        self.assertEqual(die.throw(), 2)
        self.assertEqual(die.throw(), 1)
        self.assertEqual(die.throw(), 2)
        self.assertEqual(die.throw(), 3)

 
if __name__ == '__main__':
    unittest.main()
