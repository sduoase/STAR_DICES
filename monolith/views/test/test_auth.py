from monolith.views.test.TestHelper import TestHelper
from sqlalchemy.exc import IntegrityError

class TestAuth(TestHelper):

    def test_login(self):
        reply = self._login("example@example.com", "42")
        self.assert_context("notlogged", True)
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)
        
    def test_login_redir(self):
        reply = self._login("example@example.com", "admin", True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("stories.html")
        
    def test_logout(self):
        reply = self._logout()
        self.assertEqual(reply.status_code, 401)
        reply = self._login("example@example.com", "admin")
        reply = self._logout()
        self.assertEqual(reply.status_code, 302)
        reply = self._login("example@example.com", "admin")
        reply = self._logout(True)
        self.assertEqual(reply.status_code, 200)
        
    def test_signup(self):
        reply = self._signup('example@example.com', 'admin', 'admin', 'giacobbe', '01/04/06')
        self.assertRaises(IntegrityError)
        
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)
        reply = self._signup('example2@example.com', 'admin', 'admin', 'giacobbe', '01/04/06')
        self.assertEqual(reply.status_code, 302)

        
        
