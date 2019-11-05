import unittest
from monolith.app import create_app
from monolith.database import db, User, Story, Like, Dislike

class TestAuth(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.app = self.app.test_client()
         
    def tearDown(self):
        with self.context:
            db.drop_all()
    
    def test_login(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
    
    def test_login_not_valid(self):
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'pippo'})
        self.assertEqual(reply.status_code, 302)
        
    def test_actions_without_login(self):
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 42)
        reply = self.app.get('/story/1/like')
        self.assertEqual(reply.status_code, 401)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 42)
        reply = self.app.get('/story/1/remove_like')
        self.assertEqual(reply.status_code, 401)
        reply = self.app.get('/story/1/dislike')
        self.assertEqual(reply.status_code, 401)
        reply = self.app.get('/story/1/remove_dislike')
        self.assertEqual(reply.status_code, 401)
        
    def test_wall(self):
        reply = self.app.get('/my_wall')
        self.assertEqual(reply.status_code, 401)
        reply = self.app.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.app.get('/my_wall')
        self.assertEqual(reply.status_code, 200)
        
        reply = self.app.get('/wall/1')
        self.assertEqual(reply.status_code, 200)
        
        reply = self.app.get('/wall/5')
        self.assertEqual(reply.status_code, 404)
        
        
            
        
        
    
    
    
        
