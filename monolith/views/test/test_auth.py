from monolith.views.test.TestHelper import TestHelper

class TestAuth(TestHelper):

    def test_login(self):
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)
        
    def test_login_redir(self):
        reply = self._login("example@example.com", "admin", True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("stories.html")
