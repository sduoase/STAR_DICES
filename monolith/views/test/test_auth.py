from monolith.views.test.TestHelper import TestHelper
from sqlalchemy.exc import IntegrityError
from monolith.database import db, User
from flask_login import current_user

class TestAuth(TestHelper):


    def test_login(self):
        
        # error:wrong pass
        reply = self._login("example@example.com", "42")
        self.assert_context("notlogged", True)
        with self.context:
            q = User.query.filter_by(email="example@example.com")
            self.assertNotEqual(q.first(), current_user)

        # success: logged in
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)
        with self.context:
            q = User.query.filter_by(email="example@example.com").first()
            #self.assertEqual(current_user.id, q.id) # current_user anonymous?
        
    def test_login_redir(self):
    
        # success: logged in, redirected
        reply = self._login("example@example.com", "admin", True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("home.html")
        
    def test_logout(self):
    
        # error:not logged in
        reply = self._logout()
        self.assertEqual(reply.status_code, 401)
        
        # success:logged out, no redir
        reply = self._login("example@example.com", "admin")
        reply = self._logout()
        self.assertEqual(reply.status_code, 302)
        
        # success:logged out, redirected
        reply = self._login("example@example.com", "admin")
        reply = self._logout(True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("login.html")
        
    def test_signup(self):
    
        # error:same email
        reply = self._signup('example@example.com', 'admin', 'admin', 'giacobbe', '01/04/1006')
        self.assertRaises(IntegrityError)
        
        # error:signup while logged in
        reply = self._login('example@example.com', 'admin')
        self.assertEqual(reply.status_code, 302)
        reply = self._signup('example2@example.com', 'not10char', 'admin', 'giacobbe', '01/04/1006')
        self.assertEqual(reply.status_code, 302)
        with self.context:
            q = User.query.filter_by(email='example3@example.com').first()
            self.assertIsNone(q)
        
        # error:not enough char in password
        self._logout()
        reply = self._signup('example2@example.com', 'not10char', 'admin', 'giacobbe', '01/04/1006')
        self.assertEqual(reply.status_code, 200)
        with self.context:
            q = User.query.filter_by(email='example3@example.com').first()
            self.assertIsNone(q)
        
        # success:register user
        self._signup('example3@example.com', 'holy10characterspls', 'admin', 'giacobbe', '01/04/2006', True)
        self._login('example3@example.com', 'admin')
        with self.context:
            q = User.query.filter_by(email='example3@example.com').first()
            self.assertIsNotNone(q)
            
                

        
        
