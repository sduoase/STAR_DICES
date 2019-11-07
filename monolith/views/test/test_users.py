from monolith.views.test.TestHelper import TestHelper
from sqlalchemy.exc import IntegrityError
from monolith.database import db, User
from flask_login import current_user

class TestAuth(TestHelper):

    def test_login_required_my_wall(self):
        reply = self.client.get('/my_wall')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/my_wall')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("mywall.html")

    def test_login_required_users(self):
        reply = self.client.get('/users')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/users')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("users.html")

        
    def test_login_required_public_wall(self):
        reply = self.client.get('/wall/1')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/1')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("wall.html")

    def test_login_required_follow(self):
        reply = self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")

    def test_login_required_unfollow(self):
        reply = self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")

    def test_login_required_my_followers(self):
        reply = self.client.get('/my_wall/followers')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/my_wall/followers')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("myfollowers.html")
