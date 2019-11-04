import unittest

from monolith.app import create_app
from monolith.database import db, User, Story, Like, Dislike

class TestLike(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.app = self.app.test_client()
    
    def tearDown(self):
        with self.context:
            db.drop_all()
    
    def test_single_like(self):
        reply = self.app.get('/story/1/like')
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
        reply = self.app.get('/story/1/remove_like')
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNone(l)    
