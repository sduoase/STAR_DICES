import unittest

from monolith.app import create_app
from monolith.database import db, User, Story, Like, Dislike

class TestLikeCelery(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.app = self.app.test_client()
        
    
    def tearDown(self):
        with self.context:
            db.drop_all()
    
    def test_like_remove_like(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/story/1/like')
        #self.assertEqual(reply.status_code, 200)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 43)
        reply = self.app.get('/story/1/remove_like')
        #self.assertEqual(reply.status_code, 200)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 42)
            
    def test_dislike_remove_dislike(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/story/1/dislike')
        #self.assertEqual(reply.status_code, 200)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.dislikes, 6)
            
        reply = self.app.get('/story/1/remove_dislike')
        #self.assertEqual(reply.status_code, 200)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.dislikes, 5)
            
    def test_like_dislike(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/story/1/like')
        #self.assertEqual(reply.status_code, 200)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 43)
            self.assertEqual(s.dislikes, 5)
            
        reply = self.app.get('/story/1/dislike')
        #self.assertEqual(reply.status_code, 200)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 42)
            self.assertEqual(s.dislikes, 6)

        
