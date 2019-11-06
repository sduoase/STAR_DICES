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
    
    def test_single_like_remove_like(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/story/1/like')
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
        reply = self.app.get('/story/1/remove_like')
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNone(l)
    
    def test_not_existing_story(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/story/5/like')
        self.assertEqual(reply.status_code, 404)
        
    def test_single_dislike_remove_dislike(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/story/1/dislike')
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
        reply = self.app.get('/story/1/remove_dislike')
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNone(l)
         
    def test_like_dislike(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/story/1/like')
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNone(l)
        reply = self.app.get('/story/1/dislike')
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNone(l)
   
