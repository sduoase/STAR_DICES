import unittest
import random

from monolith.views.stories import is_story_valid
 
class TestIsStoryValid(unittest.TestCase):

    def test_empty_dice_roll(self):
        dice_roll = []
        story_text = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(is_story_valid(story_text, dice_roll), True)
    
    def test_single_word_success(self):
        dice_roll = ["fox"]
        story_text = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(is_story_valid(story_text, dice_roll), True)
    
    def test_single_word_failure(self):
        dice_roll = ["cat"]
        story_text = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(is_story_valid(story_text, dice_roll), False)

    def test_multi_word_success(self):
        dice_roll = ["fox", "dog"]
        story_text = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(is_story_valid(story_text, dice_roll), True)
    
    def test_multi_word_failure(self):
        dice_roll = ["fox", "cat"]
        story_text = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(is_story_valid(story_text, dice_roll), False)
    
    def test_partial_word_matching(self):
        dice_roll = ["bro"]
        story_text = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(is_story_valid(story_text, dice_roll), False)

    def test_punctuation(self):
        dice_roll = ["dog", "fox", "jumps"]
        story_text = "The quick brown fox! jumps, over. the lazy dog?"
        self.assertEqual(is_story_valid(story_text, dice_roll), True)

    def test_case_sensitive(self):
        dice_roll = ["FOX", "dog", "bROwn"]
        story_text = "The quick BrOwN fox jumps over the lazy DOG"
        self.assertEqual(is_story_valid(story_text, dice_roll), True)
