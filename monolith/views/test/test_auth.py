import unittest
from monolith.app import create_app
from monolith.database import db, User, Story, Like, Dislike
from sqlalchemy.exc import IntegrityError
from flask import Flask
from flask_testing import TestCase

class TestAuth(TestCase):
    
    def create_app(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.client = self.app.test_client()
        return self.app
         
    def tearDown(self):
        with self.context:
            db.drop_all()
    
    def test_login(self):
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'admin'},  follow_redirects=True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used('stories.html')
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        self.assert_template_used('stories.html')
        reply = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used('login.html')
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'caio'}, follow_redirects=True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used('login.html')
        self.assert_context("notlogged", True)
        
    def test_signup(self):
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.client.get('/logout')
        self.assertEqual(reply.status_code, 302)
        reply = self.client.post('/signup', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertRaises(IntegrityError)
        
        reply = self.client.post('/signup', data={'email': 'example2@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 200)
        reply = self.client.get('/story/1/like')
        self.assertEqual(reply.status_code, 401)
        
        reply = self.client.post('/login', data={'email': 'example2@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        
        #reply = self.app.get('/story/1/like')
        #self.assertEqual(reply.status_code, 200)
        
    
    def test_login_not_valid(self):
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'pippo'})
        self.assertEqual(reply.status_code, 302)
        
    def test_actions_without_login(self):
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 42)
        reply = self.client.get('/story/1/like')
        self.assertEqual(reply.status_code, 401)
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertEqual(s.likes, 42)
        reply = self.client.get('/story/1/remove_like')
        self.assertEqual(reply.status_code, 401)
        reply = self.client.get('/story/1/dislike')
        self.assertEqual(reply.status_code, 401)
        reply = self.client.get('/story/1/remove_dislike')
        self.assertEqual(reply.status_code, 401)
        
    def test_wall(self):
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.client.get('/my_wall')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used('mywall.html')
        
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.client.get('/my_wall')
        self.assertEqual(reply.status_code, 200)
        
        reply = self.client.get('/wall/1')
        self.assertEqual(reply.status_code, 200)
        
        reply = self.client.get('/wall/5')
        self.assertEqual(reply.status_code, 404)
        
    def test_message(self):
        reply = self.client.post('/login', data={'email': 'example@example.com', 'password': 'admin'})
        self.assertEqual(reply.status_code, 302)
        reply = self.client.get('/story/1/like')
        self.assert_context('message', 'Like added!')
        reply = self.client.get('/story/1/like')
        self.assert_context("message", 'You\'ve already liked this story!')
        
        
        
            
        
        
    
    
    
        
